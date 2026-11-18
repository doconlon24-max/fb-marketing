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
SO_LAN = {"truc": 2, "laptop": 1}  # 15/11 sếp cần tốc độ: PC trực 2 làn dựng/sửa song song (video độc lập), mỗi làn 1 video
TEN_MAY = {"truc": "PC TRỰC", "laptop": "LAPTOP"}
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


HAN = {"tai": 40, "dung": 65, "app": 45}         # phút: khoá luồng quá hạn coi như treo (máy tắt giữa chừng)
GIOI_HAN = {"tai": 35, "dung": 60, "app": 40}    # phút: thời gian tối đa 1 lượt Claude (1 video ~10–15 phút)


def _loai(luong):
    return re.sub(r"\d+$", "", luong)  # dung1, dung2 → dung


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
    return any(os.path.exists(f) and time.time() - os.path.getmtime(f) < HAN[_loai(luong)] * 60 for f in ds)


def gio_vn():
    return time.strftime("%d/%m %H:%M")


def gianh(tab, cot_khoa, khoa_dong, cot, regex, gia_tri):
    """Giành việc nguyên tử trên Sheet qua Apps Script (chống 2 máy/đám mây nhận trùng). Không có Sheet API → coi như giành được."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import sheet_api
        if not sheet_api.co_cau_hinh():
            return True
        return sheet_api.claim(tab, cot_khoa, khoa_dong, cot, regex, gia_tri)
    except Exception as e:
        log(f"giành việc lỗi ({khoa_dong}): {e}")
        return True


def canh_bao_dang_nhap(may, chi_tiet):
    """Claude CLI hết đăng nhập → báo sếp 1 dòng trong app (tab HOI-SEP), tối đa 6 tiếng/lần mỗi máy."""
    mk = os.path.join(TMP, "canh_bao_dang_nhap")
    if os.path.exists(mk) and time.time() - os.path.getmtime(mk) < 6 * 3600:
        return
    open(mk, "w").write(chi_tiet)
    ten = "PC TRỰC" if may == "truc" else "LAPTOP"
    log(f"CẢNH BÁO: Claude CLI trên máy {ten} chưa đăng nhập – đã báo sếp")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import sheet_api
        if sheet_api.co_cau_hinh():
            sheet_api.append("HOI-SEP", [[
                "HS-%s-CLI-%s" % (time.strftime("%Y%m%d%H%M"), may.upper()), time.strftime("%d/%m/%Y"), "Máy " + ten,
                f"⚠️ Claude trên máy {ten} bị đăng xuất nên KHÔNG tải/dựng video được. Sếp mở Terminal trên máy {ten}, "
                f"chạy: claude setup-token (hoặc claude auth login) rồi đăng nhập trên trình duyệt. Xong thì máy tự chạy lại.",
                "", "Cảnh báo tự động từ máy (không cần trả lời)", ""]])
    except Exception as e:
        log(f"không gửi được cảnh báo lên Sheet: {e}")


def chay_claude(may, luong, tep):
    """Tiến trình con chạy tách rời: gọi Claude CLI, ghi nhật ký, gỡ khoá."""
    prompt = io.open(tep, encoding="utf-8").read()
    try:
        cl = shutil.which("claude") or os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd")
        c = tim_cfg()
        r = subprocess.run([cl, "-p", prompt, "--chrome", "--permission-mode", "auto"],
                           cwd=KHO, env=dict(os.environ, **({"RCLONE_CONFIG": c} if c else {})), capture_output=True, text=True,
                           encoding="utf-8", timeout=GIOI_HAN[_loai(luong)] * 60, shell=(os.name == "nt"),
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        out = (r.stdout or r.stderr or "").strip()
        log("Claude xong (%s): " % luong + out.replace("\n", " ")[:800])
        if re.search(r"Not logged in|/login|OAuth token has expired|authentication_error|Invalid API key|401", out[:600], re.I):
            canh_bao_dang_nhap(may, out[:200])
    except Exception as e:
        log("lỗi gọi Claude (%s): %s" % (luong, e))
    finally:
        for f in (khoa(luong), tep):
            try:
                os.remove(f)
            except OSError:
                pass


def tai_code(may, tep):
    """15/11: TẢI SPY BẰNG CODE (yt-dlp/curl qua spy_tai_ve.py) – không tốn token. Lỗi thì trả dòng về 'Chờ máy tải'
    + ghi chú H để lượt sau gọi Claude (Chrome) tải theo cách khác."""
    viec = json.load(io.open(tep, encoding="utf-8"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sheet_api
    try:
        for v in viec:
            k = v["k"]
            try:
                r = subprocess.run([sys.executable.replace("pythonw.exe", "python.exe"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "spy_tai_ve.py"),
                                    "--key", k, "--who", v["who"], "--url", v["url"], "--date", v["ngay"], "--ytdlp"],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, cwd=KHO,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                kq = json.loads((r.stdout or "").strip().splitlines()[-1])
            except Exception as e:
                kq = {"ok": False, "loi": str(e)[:200]}
            h = v["h"]
            if kq.get("ok"):
                h2 = f"{h} · File: {kq['file']} ({kq.get('giay')} giây) · Drive: SPY/{kq['ngay']}"
                sheet_api.set_key(TAB, "J", k, {"I": f"Đã tải về SPY {kq['ngay']}", "H": h2})
                log(f"TẢI bằng code OK ({k}): {kq['file']}")
            else:
                sheet_api.set_key(TAB, "J", k, {"I": "Chờ máy tải", "H": f"{h} · Máy tải bằng code lỗi {gio_vn()} ({kq.get('loi', '')[:120]}) – chuyển Claude/Chrome"})
                log(f"TẢI bằng code lỗi ({k}): {kq.get('loi', '')[:200]}")
    finally:
        for f in (khoa("tai"), tep):
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
    ap.add_argument("--chay")
    ap.add_argument("--tep")
    a = ap.parse_args()
    os.makedirs(TMP, exist_ok=True)
    if a.chay == "tai_code":
        return tai_code(a.may, a.tep)
    if a.chay:
        return chay_claude(a.may, a.chay, a.tep)
    # NHỊP SỐNG (15/11): 3 phút ghi tab MAY-TRUC 1 lần → Apps Script thấy máy sống thì KHÔNG gọi đám mây cho việc máy tự làm
    # (duyệt/đăng, yêu cầu sửa, HOI-SEP) → đám mây chỉ chạy khi máy tắt = bớt token
    nh = os.path.join(TMP, "nhip_song")
    if not a.thu and (not os.path.exists(nh) or time.time() - os.path.getmtime(nh) > 180):
        open(nh, "w").write("")
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import sheet_api
            if sheet_api.co_cau_hinh():
                sheet_api.set_("MAY-TRUC!B%d:C%d" % ((2, 2) if a.may == "truc" else (3, 3)), [[int(time.time()), gio_vn()]])
        except Exception as e:
            log(f"ghi nhịp sống lỗi: {e}")
    # KIỂM DUYỆT BÌNH LUẬN (16/11): máy trực, 10 phút/lần, chạy tách rời (quét không tốn token; AI chỉ gọi khi có bình luận mới)
    bl = os.path.join(TMP, "kiem_duyet_bl.lock")
    if not a.thu and a.may == "truc" and (not os.path.exists(bl) or time.time() - os.path.getmtime(bl) > 600):
        open(bl, "w").write(str(time.time()))
        py = sys.executable
        if py.lower().endswith("python.exe") and os.path.exists(py[:-10] + "pythonw.exe"):
            py = py[:-10] + "pythonw.exe"
        try:
            subprocess.Popen([py, os.path.join(os.path.dirname(os.path.abspath(__file__)), "kiem_duyet_bl.py"), "chay"], cwd=KHO, close_fds=True,
                             creationflags=0x00000008 | 0x00000200 | 0x08000000)
        except OSError as e:
            log(f"kiểm duyệt bình luận: không chạy được ({e})")
    cho = a.cho if a.cho is not None else (0 if a.may == "truc" else 3)
    lan_dung = ["dung%d" % n for n in range(1, SO_LAN[a.may] + 1)]
    lan_ranh = [l for l in lan_dung if not ban(l)]
    ban_tai, ban_app = ban("tai"), ban("app")
    if ban_tai and ban_app and not lan_ranh and not a.thu:
        return

    # 15 phút kéo kho 1 lần để máy luôn có script/quy trình mới nhất
    mk = os.path.join(TMP, "lan_pull")
    if not os.path.exists(mk) or time.time() - os.path.getmtime(mk) > 15 * 60:
        open(mk, "w").write("")
        subprocess.run(["git", "pull", "-q", "--rebase", "--autostash", "origin", "main"], cwd=KHO, capture_output=True, timeout=120,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    xlsx = tai_sheet()
    rows = doc_tab(xlsx, TAB)
    now = time.time()
    viec = []  # (khoá, loại 'tai'|'dung'|'sua'|'page'|'hoi'), theo thứ tự Sheet = cũ trước
    dong_tai = {}
    for r in rows[1:]:
        k, i, h = r.get("J", "").strip(), r.get("I", "").strip(), r.get("H", "")
        if not k:
            continue
        # Nút "Xử lý" trong app ghi 4 kiểu (LK_ACT trong merah-studio/src.html), có thể kèm ": <lệnh>":
        #   'Chờ máy tải[: lệnh]' · 'Sếp cho dựng – chờ EDIT[: lệnh]' · 'Sếp yêu cầu – chờ xử lý: lệnh' · 'Bỏ hẳn (...)'
        # → luôn so bằng startswith, KHÔNG so ==, kẻo dòng kẹt (lỗi 15/11).
        if i.startswith("Sếp yêu cầu"):
            if "Drive: SPY/" in h:
                viec.append((k, "dung"))  # đã có tư liệu → làn DỰNG làm đúng lệnh (lệnh nằm ở cột H 'Sếp xử lý …')
            else:
                dong_tai[k] = r
                viec.append((k, "tai"))
            continue
        if i.startswith("Chờ máy tải"):
            dong_tai[k] = r
            # chưa thử tải bằng code (H chưa có "Máy tải bằng code lỗi") → làn TẢI CODE, không gọi Claude
            viec.append((k, "tai" if "Máy tải bằng code lỗi" in h or not r.get("F", "").strip().startswith("http") else "tai_code"))
        elif i.startswith("Đang tải (máy") and khoa_cu(i.replace("Đang tải", "Đang edit", 1), now):
            dong_tai[k] = r
            viec.append((k, "tai"))  # lượt tải code/Claude chết giữa chừng quá 3 tiếng → Claude tải lại
        elif (("Drive: SPY/" in h) or ("File: SPY_" in h and ngay_iso(r.get("A", "")) >= MOC_CHAT)) and (i.startswith("Đã tải về SPY") or i.startswith("Sếp cho dựng") or khoa_cu(i, now)):
            # 'Sếp cho dựng – chờ EDIT' = sếp bấm Xử lý → Vẫn dựng trong app (lỗi 15/11: trước bỏ sót, video kẹt)
            viec.append((k, "dung"))
    # LƯỚI AN TOÀN: dòng link sếp gửi / sếp đã bấm Xử lý mà cột I là trạng thái máy không biết → ghi cảnh báo (6 tiếng/lần/dòng)
    BIET = ("Chờ máy tải", "Đang tải", "Đã tải về SPY", "Sếp cho dựng", "Sếp yêu cầu", "Đang edit", "Chờ Sếp duyệt",
            "Đã dựng", "Bỏ", "Không tải được", "Lỗi dựng", "Không dựng", "Đề xuất bỏ", "Đã giao")
    for r in rows[1:]:
        k, i, h = r.get("J", "").strip(), r.get("I", "").strip(), r.get("H", "")
        if k and ("LINK SẾP GỬI" in h or "Sếp xử lý" in h) and i and not i.startswith(BIET):
            mk2 = os.path.join(TMP, "la_" + re.sub(r"[^\w-]", "_", k))
            if not os.path.exists(mk2) or time.time() - os.path.getmtime(mk2) > 6 * 3600:
                open(mk2, "w").write(i)
                log(f"CẢNH BÁO trạng thái lạ – máy không tự làm: {k} I='{i[:80]}' (thêm vào canh_spy.py nếu cần xử lý)")
    # yêu cầu sửa video quảng cáo (QUANG-CAO 'Cần sửa') – ưu tiên trước video mới
    sua = []
    try:
        for r in doc_tab(xlsx, "QUANG-CAO")[1:]:
            ma, i = r.get("A", "").strip(), r.get("I", "").strip()
            if not (ma.startswith("QC-") and "-VD" in ma):
                continue
            if i.startswith("Cần sửa"):
                sua.append((ma, "sua"))
            elif i == "Đang sửa" and re.search(r"(Cần|cần) dựng trên máy|không render được", (r.get("N", "") + r.get("K", ""))[-600:]):
                sua.append((ma, "sua"))  # đám mây đã nhận nhưng ghi rõ phải dựng trên máy → nhận ngay
            elif i == "Đang sửa" or (i.startswith("Đang sửa (máy") and khoa_cu(i.replace("Đang sửa", "Đang edit", 1), now)):
                sua.append((ma, "sua_treo"))  # lượt khác (đám mây/máy) đã nhận – chỉ tiếp quản nếu kẹt quá 90 phút
    except Exception as e:
        log(f"không đọc được tab QUANG-CAO: {e}")
    # LÀN APP (15/11): bài fanpage 'Cần sửa' + câu trả lời HOI-SEP chưa xử lý → nhận ngay, không chờ lượt đám mây 15 phút
    app = []
    try:
        for r in doc_tab(xlsx, "Untitled")[1:]:
            ma, i, k = r.get("A", "").strip(), r.get("I", "").strip(), r.get("K", "")
            if re.fullmatch(r"\d{8}-\d{4}", ma) and i == "Cần sửa" and not k.startswith("TRÙNG"):
                app.append((ma, "page"))
        for r in doc_tab(xlsx, "HOI-SEP")[1:]:
            ma, e_, f_ = r.get("A", "").strip(), r.get("E", "").strip(), r.get("F", "").strip()
            if ma and e_ and not f_:
                app.append((ma, "hoi"))
    except Exception as e:
        log(f"không đọc được tab bài page/HOI-SEP: {e}")
    viec = sua + viec + app
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    keys = {k + "|" + t for k, t in viec}
    st = {k: v for k, v in st.items() if k in keys}  # dòng đã xử lý xong thì bỏ khỏi sổ
    can = []
    for k, t in viec:
        e = st.setdefault(k + "|" + t, {"thay": now, "goi": 0})
        if (t in ("tai", "tai_code") and ban_tai) or (t in ("page", "hoi") and ban_app):
            continue
        if t == "tai_code" and any(x == "tai_code" for _, x in can):
            continue  # 1 lượt tải code / phút
        if now - e["thay"] < cho * 60:
            continue  # laptop nhường máy trực
        if t == "sua_treo" and now - e["thay"] < 90 * 60:
            continue  # "Đang sửa" của lượt khác: chờ 90 phút mới coi là kẹt
        if e["goi"] and now - e["goi"] < {"tai": 30, "tai_code": 20, "page": 40, "hoi": 40}.get(t, 120) * 60:
            continue  # đã gọi Claude cho dòng này gần đây
        if t in ("dung", "sua", "sua_treo") and sum(1 for _, x in can if x in ("dung", "sua", "sua_treo")) >= len(lan_ranh) * TOI_DA[a.may]:
            continue  # mỗi làn rảnh nhận 1 video, còn lại lượt sau
        can.append((k, t))
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)

    if a.thu:
        print(json.dumps({"ban": {"tai": ban_tai, "app": ban_app, "lan_dung_ranh": lan_ranh}, "viec": viec, "se_goi": can}, ensure_ascii=False, indent=1))
        return
    if not can:
        return

    may = TEN_MAY[a.may]
    chung = "Không vượt đăng nhập/captcha, không in token, không đăng bài hay bật quảng cáo. Trả lời ngắn gọn bằng tiếng Việt."
    # giành việc trên Sheet NGAY (nguyên tử) để máy kia/đám mây không nhận trùng
    nhan = []
    for k, t in can:
        ok = True
        if t in ("sua", "sua_treo"):
            ok = gianh("QUANG-CAO", "A", k, "I", r"^(Cần sửa|Đang sửa)", f"Đang sửa (máy {may} {gio_vn()})")
        elif t == "dung":
            ok = gianh("SPY-ADS", "J", k, "I", r"^(Đã tải về SPY|Sếp cho dựng|Sếp yêu cầu|Đang edit)", f"Đang edit (máy {may} {gio_vn()})")
        elif t == "tai_code":
            ok = gianh("SPY-ADS", "J", k, "I", r"^Chờ máy tải", f"Đang tải (máy {may} {gio_vn()})")
        elif t == "page":
            ok = gianh("Untitled", "A", k, "I", r"^Cần sửa$", "Đang sửa")
        elif t == "hoi":
            ok = gianh("HOI-SEP", "A", k, "F", r"^$", f"Đang xử lý (máy {may} {gio_vn()})")
        if ok:
            nhan.append((k, t))
            st[k + "|" + t]["goi"] = now
        else:
            log(f"bỏ {k} ({t}): máy/lượt khác đã nhận")
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)

    tc = [k for k, t in nhan if t == "tai_code"]
    if tc:
        import datetime
        hom_nay = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%d-%m-%Y")
        ds = []
        for k in tc:
            r = dong_tai[k]
            iso = ngay_iso(r.get("A", ""))
            ngay = f"{iso[8:10]}-{iso[5:7]}-{iso[:4]}" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso) and "LINK SẾP GỬI" in r.get("H", "") else hom_nay
            ds.append({"k": k, "who": r.get("D", "").strip(), "url": r.get("F", "").strip().split()[0], "ngay": ngay, "h": r.get("H", "")})
        log("TẢI bằng code (không token): " + ", ".join(tc))
        tep = os.path.join(TMP, "tai_code.json")
        json.dump(ds, io.open(tep, "w", encoding="utf-8"), ensure_ascii=False)
        open(khoa("tai"), "w").write(str(time.time()))
        py = sys.executable
        if py.lower().endswith("python.exe"):
            py = py[:-10] + "pythonw.exe"
        base = 0x00000008 | 0x00000200 | 0x08000000
        try:
            subprocess.Popen([py, os.path.abspath(__file__), "--may", a.may, "--chay", "tai_code", "--tep", tep], cwd=KHO, close_fds=True, creationflags=base | 0x01000000)
        except OSError:
            subprocess.Popen([py, os.path.abspath(__file__), "--may", a.may, "--chay", "tai_code", "--tep", tep], cwd=KHO, close_fds=True, creationflags=base)

    tai = [k for k, t in nhan if t == "tai"]
    if tai and not tc:  # cùng khoá làn TẢI: phút này đã chạy tải code thì Claude chờ phút sau
        log("gọi Claude TẢI: " + ", ".join(tai))
        tach_roi(a.may, "tai", (
            f"Canh SPY (máy {may}) – luồng TẢI. Tab SPY-ADS có dòng 'Chờ máy tải': {', '.join(tai)}. Làm ngay theo tac-vu/spy-tai-video-may.md: "
            f"chọn Chrome máy này bằng select_browser {CHROME[a.may]} (không có thì list_connected_browsers chọn cái còn kết nối), "
            f"đổi I sang 'Đang tải' trước khi tải để máy kia không làm trùng, tải video (yt-dlp trước nếu hợp), đẩy Drive TƯ LIỆU QUẢNG CÁO/SPY/<ngày>, "
            f"cập nhật Sheet (I = 'Đã tải về SPY <ngày>', H giữ 'Drive: SPY/<ngày>'), xoá hẳn tệp tạm + thùng rác. CHỈ TẢI, KHÔNG dựng: "
            f"luồng DỰNG của máy sẽ tự nhận video ở phút kế tiếp. Đóng tab Chrome đã mở. {chung}"))

    # mỗi video 1 làn dựng riêng, chạy song song (video độc lập nhau)
    video = [(k, "sua" if t == "sua_treo" else t) for k, t in nhan if t in ("sua", "sua_treo", "dung")]
    for (k, t), lan in zip(video, lan_ranh):
        log(f"gọi Claude {'SỬA' if t == 'sua' else 'DỰNG'} ({lan}): {k}")
        if t == "sua":
            p = (f"Canh việc (máy {may}, làn {lan}) – SỬA video quảng cáo {k} theo yêu cầu Sếp (tab QUANG-CAO, cột J = yêu cầu, cột N/K = lịch sử). "
                 f"Dòng đã được giành: I = 'Đang sửa (máy {may} …)'. Thêm 1 dòng cột N '<giờ> – Video – đã tiếp nhận', "
                 f"tải bản cũ + tư liệu gốc, sửa ĐÚNG yêu cầu cột J (xem ảnh khoanh lỗi nếu có link), PC07 HyperFrames, kiem_tra_muot, GIỮ NGUYÊN mã/tên file/thư mục/dòng Sheet "
                 f"(ghi đè file trên Drive cùng tên, bản cũ vào Thùng rác, tạo lại bản xem nhẹ tao_ban_xem.py), ghi I = 'Chờ duyệt đăng', thêm dòng N '<giờ> – Video – sửa xong (vN): <đã sửa gì> – chờ Sếp duyệt'. "
                 f"Không sửa được thì I = 'Cần sửa' + ghi lý do cột K. Máy có thể đang render 1 video khác song song – dùng thư mục làm việc riêng tên theo mã {k}. "
                 f"TRƯỚC khi sửa đọc skill .claude/skills/merah-video-qc-bai-hoc (SKILL.md + bai-hoc.md) và tự soát mục B; SỬA XONG BẮT BUỘC ghi bài học vào bai-hoc.md + thêm/sửa luật mục B theo mục C của skill, commit cùng bản sửa. ")
        else:
            p = (f"Canh việc (máy {may}, làn {lan}) – DỰNG video SPY {k}: làm mục 'DỰNG LUÔN TRÊN MÁY' trong tac-vu/spy-tai-video-may.md cho ĐÚNG video này "
                 f"(KHÔNG giao đám mây). Dòng SPY-ADS đã được giành: I = 'Đang edit (máy {may} …)'. PC07 HyperFrames theo .claude/agents/merah-ads-video.md, up THÀNH PHẨM QUẢNG CÁO, "
                 f"ĐẶT MÃ: ngày = ngày thư mục tư liệu (SPY/<ngày>, KHÔNG phải hôm nay); trước khi đặt mã TÌM dòng QUANG-CAO cũ cùng khoá nguồn (cột G/K) – có thì ghi đè dòng + giữ mã/tên file cũ, không có mới lấy VDn kế tiếp của ngày tư liệu "
                 f"(làn khác có thể đang dựng video khác cùng ngày: đọc lại Sheet ngay trước khi thêm dòng để không trùng mã). "
                 f"Ghi dòng QUANG-CAO 'Chờ duyệt đăng' + caption M, SPY-ADS I = 'Chờ Sếp duyệt (<mã QC>)', lỗi thì I = 'Lỗi dựng (<lý do>)'. "
                 f"Dùng thư mục làm việc riêng tên theo khoá {k}. Xoá hẳn tệp tạm trên máy và thùng rác. "
                 f"TRƯỚC khi dựng đọc skill .claude/skills/merah-video-qc-bai-hoc (SKILL.md + bai-hoc.md) và tự soát toàn bộ mục B trên bản render trước khi nộp. ")
        tach_roi(a.may, lan, p + chung)

    pg = [k for k, t in nhan if t == "page"]
    hoi = [k for k, t in nhan if t == "hoi"]
    if pg or hoi:
        log("gọi Claude APP: " + ", ".join(pg + hoi))
        tach_roi(a.may, "app", (
            f"Canh việc (máy {may}) – làn APP, làm NGAY theo tac-vu/nhan-vien-truc.md (bước 1 HOI-SEP và mục Yêu cầu sửa) cho đúng các việc sau, việc độc lập thì làm luôn trong lượt này: "
            + (f"(1) Bài fanpage Sếp yêu cầu sửa (tab Untitled, I đã giành = 'Đang sửa'): {', '.join(pg)} – đọc ghi chú cột J + lịch sử cột L + ảnh khoanh (ẢNH YÊU CẦU SỬA), "
               f"ghi L '<giờ> – Media – đã tiếp nhận', sửa đúng yêu cầu (ảnh: Higgsfield/code theo luật ảnh; caption tiếng Anh), up Drive bản mới, cập nhật G/H, bản cũ vào Thùng rác Drive, I = 'Chờ duyệt', L '<giờ> – Media – sửa xong (vN) – chờ Sếp duyệt'. " if pg else "")
            + (f"(2) Câu trả lời HOI-SEP chưa xử lý (cột F đã giành 'Đang xử lý (máy …)'): {', '.join(hoi)} – làm theo câu trả lời của Sếp, xong ghi F = 'Đã xử lý <giờ> – <đã làm gì>'. " if hoi else "")
            + "Không đăng bài/quảng cáo khi Sếp chưa duyệt. " + chung))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"lỗi: {e}")
        if "--thu" in sys.argv:
            raise
