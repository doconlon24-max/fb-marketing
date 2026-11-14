"""Canh SPY miễn phí: 1 phút/lần xem tab SPY-ADS có dòng "Chờ máy tải" không.
Không tốn hạn mức Claude khi không có việc. Có việc mới gọi Claude (claude -p --chrome) tải video.

Chạy: python canh_spy.py --may truc        (máy trực: làm ngay)
      python canh_spy.py --may laptop      (laptop: chỉ làm khi dòng đã chờ >= 3 phút mà máy trực chưa nhận)
      python canh_spy.py --may truc --thu  (chỉ in danh sách, không gọi Claude)
Đặt lịch Windows 1 phút/lần (xem tac-vu/spy-tai-video-may.md, mục "Canh SPY miễn phí").
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, zipfile
import xml.etree.ElementTree as ET

SHEET_ID = "{{ID_DRIVE}}"
TAB = "SPY-ADS"
KHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(tempfile.gettempdir(), "merah-canh-spy")
STATE = os.path.join(TMP, "da_goi.json")
LOCK = os.path.join(TMP, "dang_chay.lock")
LOG = os.path.join(TMP, "nhat_ky.txt")
CHROME = {"truc": "{{ID_KET_NOI}}", "laptop": "{{ID_KET_NOI}}"}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def log(s):
    os.makedirs(TMP, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + s + "\n")


def tai_sheet():
    d = os.path.join(TMP, "sheet")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    subprocess.run(["rclone", "backend", "copyid", "merah:", SHEET_ID, d + os.sep, "--drive-export-formats", "xlsx"],
                   capture_output=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    fs = [f for f in os.listdir(d) if f.endswith(".xlsx")]
    if not fs:
        raise RuntimeError("không tải được Sheet bằng rclone")
    return os.path.join(d, fs[0])


def doc_tab(path, tab):
    """Đọc 1 tab xlsx bằng thư viện chuẩn (không cần openpyxl). Trả list hàng, mỗi hàng là dict cột->chuỗi."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    target = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == tab:
            target = rmap[s.get(RID)]
    if not target:
        return []
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    out = []
    for row in ET.fromstring(z.read(target)).iter("{%s}row" % NS["m"]):
        r = {}
        for c in row.findall("m:c", NS):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", NS)
            if c.get("t") == "s" and v is not None:
                val = ss[int(v.text)]
            elif c.get("t") == "inlineStr":
                val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
            else:
                val = v.text if v is not None else ""
            r[col] = val or ""
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--may", choices=["truc", "laptop"], required=True)
    ap.add_argument("--cho", type=float, default=None, help="phút chờ trước khi nhận việc (mặc định: trực 0, laptop 3)")
    ap.add_argument("--thu", action="store_true")
    a = ap.parse_args()
    cho = a.cho if a.cho is not None else (0 if a.may == "truc" else 3)
    os.makedirs(TMP, exist_ok=True)

    # đang có lượt Claude chạy thì thôi (khoá quá 40 phút coi như treo)
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 40 * 60:
        return

    rows = doc_tab(tai_sheet(), TAB)
    cho_tai = [(r.get("J", ""), r.get("F", "")) for r in rows[1:] if r.get("I", "").strip() == "Chờ máy tải" and r.get("J")]
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    now = time.time()
    keys = {k for k, _ in cho_tai}
    st = {k: v for k, v in st.items() if k in keys}  # dòng đã xử lý xong thì bỏ khỏi sổ
    can = []
    for k, link in cho_tai:
        e = st.setdefault(k, {"thay": now, "goi": 0})
        if now - e["thay"] < cho * 60:
            continue  # laptop nhường máy trực
        if e["goi"] and now - e["goi"] < 30 * 60:
            continue  # đã gọi Claude cho dòng này trong 30 phút qua
        can.append((k, link))
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)

    if a.thu:
        print(json.dumps({"cho_may_tai": cho_tai, "se_goi": can}, ensure_ascii=False, indent=1))
        return
    if not can:
        return

    for k, _ in can:
        st[k]["goi"] = now
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)
    ds = "; ".join(k for k, _ in can)
    prompt = (
        f"Canh SPY ({a.may}) thấy dòng 'Chờ máy tải' ở tab SPY-ADS: {ds}. "
        f"Làm ngay theo tac-vu/spy-tai-video-may.md (Bước 2 trở đi) cho các dòng 'Chờ máy tải': "
        f"chọn Chrome máy này bằng select_browser {CHROME[a.may]} (nếu không có thì list_connected_browsers chọn cái còn kết nối), "
        f"đổi cột I sang 'Đang tải' trước khi tải để máy kia không làm trùng, tải video, đẩy Drive TƯ LIỆU QUẢNG CÁO/SPY/<ngày>, "
        f"cập nhật Sheet, rồi chạy routine Quét chính như quy định. Không vượt đăng nhập/captcha, không in token. Trả lời ngắn gọn bằng tiếng Việt."
    )
    log(f"gọi Claude cho: {ds}")
    open(LOCK, "w").write(str(now))
    try:
        r = subprocess.run(["claude", "-p", prompt, "--chrome", "--permission-mode", "auto"],
                           cwd=KHO, capture_output=True, text=True, encoding="utf-8", timeout=35 * 60, shell=(os.name == "nt"),
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        log("Claude xong: " + (r.stdout or r.stderr or "").strip().replace("\n", " ")[:800])
    except Exception as e:
        log(f"lỗi gọi Claude: {e}")
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"lỗi: {e}")
        if "--thu" in sys.argv:
            raise
