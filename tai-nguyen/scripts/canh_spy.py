"""Canh SPY miễn phí: 1 phút/lần xem tab SPY-ADS có dòng "Chờ máy tải" không.
Không tốn hạn mức Claude khi không có việc. Có việc mới gọi Claude (claude -p --chrome) tải video.

Chạy: python canh_spy.py --may truc        (máy trực: làm ngay)
      python canh_spy.py --may laptop      (laptop: chỉ làm khi dòng đã chờ >= 3 phút mà máy trực chưa nhận)
      python canh_spy.py --may truc --thu  (chỉ in danh sách, không gọi Claude)
Đặt lịch Windows 1 phút/lần (xem tac-vu/spy-tai-video-may.md, mục "Canh SPY miễn phí").
"""
import argparse, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import xml.etree.ElementTree as ET

SHEET_ID = "{{ID_DRIVE}}"
TAB = "SPY-ADS"
KHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.join(tempfile.gettempdir(), "merah-canh-spy")
STATE = os.path.join(TMP, "da_goi.json")
LOCK = os.path.join(TMP, "dang_chay.lock")
LOG = os.path.join(TMP, "nhat_ky.txt")
MOC_CHAT = "2026-11-15"  # video sếp gửi trong chat (H "File: SPY_…") từ ngày này tự dựng; cũ hơn chờ sếp quyết
TOI_DA = {"truc": 1, "laptop": 1}  # 15/11 sếp: 1 video/lượt, xong cái nào lịch 1 phút nhận ngay cái kế (không ôm lô, máy kia rảnh được chia việc)
CHROME = {"truc": "{{ID_KET_NOI}}", "laptop": "{{ID_KET_NOI}}"}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def log(s):
    os.makedirs(TMP, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + s + "\n")


def tim_cfg():
    """rclone.conf thật; nếu chỉ có bản trong thư mục ảo của app Claude (gói MSIX) thì trả đường dẫn đó."""
    if os.path.exists(os.path.join(os.environ.get("APPDATA", ""), "rclone", "rclone.conf")):
        return None
    import glob
    g = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Packages", "Claude_*", "LocalCache", "Roaming", "rclone", "rclone.conf"))
    return g[0] if g else None


def tai_sheet():
    d = os.path.join(TMP, "sheet")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    rc = shutil.which("rclone")
    if not rc:  # lịch Windows có thể thiếu PATH của winget
        import glob
        g = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages", "Rclone.Rclone*", "*", "rclone.exe"))
        rc = g[0] if g else "rclone"
    c = tim_cfg()
    cfg = ["--config", c] if c else []
    p = subprocess.run([rc] + cfg + ["backend", "copyid", "merah:", SHEET_ID, d + os.sep, "--drive-export-formats", "xlsx"],
                   capture_output=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    fs = [f for f in os.listdir(d) if f.endswith(".xlsx")]
    if not fs:
        raise RuntimeError("không tải được Sheet bằng rclone (%s): %s" % (rc, (p.stderr or b"")[-300:].decode("utf-8", "replace")))
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


def ngay_iso(v):
    """Ô ngày trong xlsx có thể là số (ngày Excel) hoặc chuỗi yyyy-mm-dd / dd/mm/yyyy."""
    v = (v or "").strip()
    try:
        import datetime
        if re.fullmatch(r"\d+(\.\d+)?", v):
            return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(v)))).isoformat()
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", v)
        if m:
            return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1)))
    except Exception:
        pass
    return v[:10]


def khoa_cu(i, now):
    """'Đang edit' không khoá máy, hoặc khoá 'Đang edit (máy … dd/MM HH:mm)' cũ hơn 3 tiếng."""
    if not i.startswith("Đang edit"):
        return False
    m = re.search(r"(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2})", i)
    if "(máy" not in i or not m:
        return True
    d, mo, hh, mm = map(int, m.groups())
    t = time.localtime(now)
    try:
        ts = time.mktime((t.tm_year, mo, d, hh, mm, 0, 0, 0, -1))
    except (OverflowError, ValueError):
        return True
    if ts > now + 86400:  # khoá ghi tháng 12 năm ngoái
        ts = time.mktime((t.tm_year - 1, mo, d, hh, mm, 0, 0, 0, -1))
    return now - ts > 3 * 3600


HAN = {"tai": 40, "dung": 65}         # phút: khoá luồng quá hạn coi như treo (máy tắt giữa chừng)
GIOI_HAN = {"tai": 35, "dung": 60}    # phút: thời gian tối đa 1 lượt Claude (1 video ~10–15 phút)


def khoa(luong):
    return os.path.join(TMP, "dang_chay_%s.lock" % luong)


def ban(luong):
    """Luồng đang có lượt Claude chạy?"""
    ds = [khoa(luong)]  # 15/11: bỏ khoá cũ dang_chay.lock (bản 1 luồng) – từng làm laptop tưởng đang bận, không nhận dựng
    try:
        if os.path.exists(LOCK):
            os.remove(LOCK)
    except OSError:
        pass
    return any(os.path.exists(f) and time.time() - os.path.getmtime(f) < HAN[luong] * 60 for f in ds)


def chay_claude(may, luong, tep):
    """Tiến trình con chạy tách rời: gọi Claude CLI, ghi nhật ký, gỡ khoá."""
    prompt = io.open(tep, encoding="utf-8").read()
    try:
        cl = shutil.which("claude") or os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd")
        c = tim_cfg()
        r = subprocess.run([cl, "-p", prompt, "--chrome", "--permission-mode", "auto"],
                           cwd=KHO, env=dict(os.environ, **({"RCLONE_CONFIG": c} if c else {})), capture_output=True, text=True,
                           encoding="utf-8", timeout=GIOI_HAN[luong] * 60, shell=(os.name == "nt"),
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        log("Claude xong (%s): " % luong + (r.stdout or r.stderr or "").strip().replace("\n", " ")[:800])
    except Exception as e:
        log("lỗi gọi Claude (%s): %s" % (luong, e))
    finally:
        for f in (khoa(luong), tep):
            try:
                os.remove(f)
            except OSError:
                pass


def tach_roi(may, luong, prompt):
    """Khởi chạy lượt Claude tách rời để lịch 1 phút vẫn chạy tiếp (đang dựng vẫn tải được link mới)."""
    tep = os.path.join(TMP, "prompt_%s.txt" % luong)
    io.open(tep, "w", encoding="utf-8").write(prompt)
    open(khoa(luong), "w").write(str(time.time()))
    py = sys.executable
    if py.lower().endswith("python.exe") and os.path.exists(py[:-10] + "pythonw.exe"):
        py = py[:-10] + "pythonw.exe"
    cmd = [py, os.path.abspath(__file__), "--may", may, "--chay", luong, "--tep", tep]
    base = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED_PROCESS | NEW_PROCESS_GROUP | NO_WINDOW
    try:
        subprocess.Popen(cmd, cwd=KHO, close_fds=True, creationflags=base | 0x01000000)  # + BREAKAWAY_FROM_JOB
    except OSError:
        subprocess.Popen(cmd, cwd=KHO, close_fds=True, creationflags=base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--may", choices=["truc", "laptop"], required=True)
    ap.add_argument("--cho", type=float, default=None, help="phút chờ trước khi nhận việc (mặc định: trực 0, laptop 3)")
    ap.add_argument("--thu", action="store_true")
    ap.add_argument("--chay", choices=["tai", "dung"])
    ap.add_argument("--tep")
    a = ap.parse_args()
    os.makedirs(TMP, exist_ok=True)
    if a.chay:
        return chay_claude(a.may, a.chay, a.tep)
    cho = a.cho if a.cho is not None else (0 if a.may == "truc" else 3)
    ban_tai, ban_dung = ban("tai"), ban("dung")
    if ban_tai and ban_dung and not a.thu:
        return

    # 15 phút kéo kho 1 lần để máy luôn có script/quy trình mới nhất
    mk = os.path.join(TMP, "lan_pull")
    if not os.path.exists(mk) or time.time() - os.path.getmtime(mk) > 15 * 60:
        open(mk, "w").write("")
        subprocess.run(["git", "pull", "-q", "--ff-only", "origin", "main"], cwd=KHO, capture_output=True, timeout=120,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    rows = doc_tab(tai_sheet(), TAB)
    now = time.time()
    viec = []  # (khoá, loại 'tai'|'dung'), theo thứ tự Sheet = cũ trước
    for r in rows[1:]:
        k, i, h = r.get("J", "").strip(), r.get("I", "").strip(), r.get("H", "")
        if not k:
            continue
        if i == "Chờ máy tải":
            viec.append((k, "tai"))
        elif (("Drive: SPY/" in h) or ("File: SPY_" in h and ngay_iso(r.get("A", "")) >= MOC_CHAT)) and (i.startswith("Đã tải về SPY") or khoa_cu(i, now)):
            viec.append((k, "dung"))
    # 15/11: yêu cầu sửa video quảng cáo (tab QUANG-CAO cột I 'Cần sửa') – máy nhận và sửa ngay, đi chung luồng DỰNG, ưu tiên trước video mới
    try:
        qc = doc_tab(tai_sheet(), "QUANG-CAO")
    except Exception as e:
        qc = []
        log(f"không đọc được tab QUANG-CAO: {e}")
    sua = []
    for r in qc[1:]:
        ma, i = r.get("A", "").strip(), r.get("I", "").strip()
        if ma.startswith("QC-") and "-VD" in ma and (i.startswith("Cần sửa") or (i.startswith("Đang sửa") and khoa_cu(i.replace("Đang sửa", "Đang edit", 1), now))):
            sua.append((ma, "sua"))
    viec = sua + viec
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    keys = {k + "|" + t for k, t in viec}
    st = {k: v for k, v in st.items() if k in keys}  # dòng đã xử lý xong thì bỏ khỏi sổ
    can = []
    for k, t in viec:
        e = st.setdefault(k + "|" + t, {"thay": now, "goi": 0})
        if (t == "tai" and ban_tai) or (t in ("dung", "sua") and ban_dung):
            continue  # luồng đó đang bận, lượt sau
        if now - e["thay"] < cho * 60:
            continue  # laptop nhường máy trực
        if e["goi"] and now - e["goi"] < (30 if t == "tai" else 120) * 60:
            continue  # đã gọi Claude cho dòng này gần đây
        if t in ("dung", "sua") and sum(1 for _, x in can if x in ("dung", "sua")) >= TOI_DA[a.may]:
            continue  # giới hạn video dựng/lượt (dựng lần lượt), còn lại lượt sau
        can.append((k, t))
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)

    if a.thu:
        print(json.dumps({"ban": {"tai": ban_tai, "dung": ban_dung}, "viec": viec, "se_goi": can}, ensure_ascii=False, indent=1))
        return
    if not can:
        return
    for k, t in can:
        st[k + "|" + t]["goi"] = now
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)

    may = "PC TRỰC" if a.may == "truc" else "LAPTOP"
    chung = "Không vượt đăng nhập/captcha, không in token, không đăng bài hay bật quảng cáo. Trả lời ngắn gọn bằng tiếng Việt."
    tai = [k for k, t in can if t == "tai"]
    dung = [k for k, t in can if t == "dung"]
    sua = [k for k, t in can if t == "sua"]
    if tai:
        log("gọi Claude TẢI: " + ", ".join(tai))
        tach_roi(a.may, "tai", (
            f"Canh SPY (máy {may}) – luồng TẢI. Tab SPY-ADS có dòng 'Chờ máy tải': {', '.join(tai)}. Làm ngay theo tac-vu/spy-tai-video-may.md: "
            f"chọn Chrome máy này bằng select_browser {CHROME[a.may]} (không có thì list_connected_browsers chọn cái còn kết nối), "
            f"đổi I sang 'Đang tải' trước khi tải để máy kia không làm trùng, tải video (yt-dlp trước nếu hợp), đẩy Drive TƯ LIỆU QUẢNG CÁO/SPY/<ngày>, "
            f"cập nhật Sheet (I = 'Đã tải về SPY <ngày>', H giữ 'Drive: SPY/<ngày>'), xoá hẳn tệp tạm + thùng rác. CHỈ TẢI, KHÔNG dựng: "
            f"luồng DỰNG của máy sẽ tự nhận video ở phút kế tiếp. {chung}"))
    if dung or sua:
        log("gọi Claude DỰNG/SỬA: " + ", ".join(sua + dung))
        phan_sua = (f"TRƯỚC TIÊN SỬA các video quảng cáo Sếp yêu cầu sửa: {', '.join(sua)} (tab QUANG-CAO, cột J = yêu cầu của Sếp, cột N/K = lịch sử). "
                    f"Mỗi video: đổi I = 'Đang sửa (máy {may} <dd/MM HH:mm>)' (= ĐÃ TIẾP NHẬN, app hiện bước 2–3) và thêm 1 dòng cột N '<giờ> – Video – đã tiếp nhận', "
                    f"tải bản cũ + tư liệu gốc, sửa ĐÚNG yêu cầu cột J (xem ảnh khoanh lỗi nếu có link), PC07 HyperFrames, kiem_tra_muot, GIỮ NGUYÊN mã/tên file/thư mục/dòng Sheet "
                    f"(ghi đè file trên Drive cùng tên, bản cũ vào Thùng rác, tạo lại bản xem nhẹ tao_ban_xem.py), ghi I = 'Chờ duyệt đăng', thêm dòng N '<giờ> – Video – sửa xong (vN): <đã sửa gì> – chờ Sếp duyệt'. "
                    f"Không sửa được thì I = 'Cần sửa' + ghi lý do cột K. ") if sua else ""
        tach_roi(a.may, "dung", phan_sua + (
            (f"Canh SPY (máy {may}) – luồng DỰNG. Làm mục 'DỰNG LUÔN TRÊN MÁY' trong tac-vu/spy-tai-video-may.md cho ĐÚNG các video: {', '.join(dung)} " if dung else "") + (
            f"(KHÔNG giao đám mây). Trước mỗi video khoá dòng I = 'Đang edit (máy {may} <dd/MM HH:mm>)' (dòng đã bị máy khác khoá còn mới thì bỏ qua), "
            f"dựng LẦN LƯỢT từng video, không song song, PC07 HyperFrames theo .claude/agents/merah-ads-video.md, up THÀNH PHẨM QUẢNG CÁO, "
            f"ĐẶT MÃ: ngày = ngày thư mục tư liệu (SPY/<ngày>, KHÔNG phải hôm nay); trước khi đặt mã TÌM dòng QUANG-CAO cũ cùng khoá nguồn (cột G/K) – có thì ghi đè dòng + giữ mã/tên file cũ (dựng lại), không có mới lấy VDn kế tiếp của ngày tư liệu. "
            f"Ghi dòng QUANG-CAO 'Chờ duyệt đăng' + caption M, SPY-ADS I = 'Chờ Sếp duyệt (<mã QC>)', lỗi thì I = 'Lỗi dựng (<lý do>)'. "
            f"Xoá hẳn tệp tạm trên máy và thùng rác. " if dung else "") + chung))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"lỗi: {e}")
        if "--thu" in sys.argv:
            raise
