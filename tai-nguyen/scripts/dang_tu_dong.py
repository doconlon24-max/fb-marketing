"""HÀNG ĐĂNG BÀI KHÔNG TỐN TOKEN (sếp chốt 15/11/2026) – lịch Windows 1 phút/lần gọi file này.
Làm bằng code thuần (không gọi Claude):
  A. Tab bài page (Untitled): I = `Đã duyệt`, G có link, E ≠ `Ý tưởng` → tải ảnh/video từ Drive → đăng "all" (10 page)
     giờ đăng (B + C giờ PH) còn > 15 phút → HẸN GIỜ (I `Đã lên lịch`), còn lại → ĐĂNG NGAY (I `Đã đăng`, đăng bù nếu trễ) + Tin 24h.
  B. Bài `Đã lên lịch`/`Đã đăng` đã qua giờ, K chưa có `TIN 24H: đã đăng` → kiểm tra bài đã lên → I `Đã đăng` + đăng Tin 24h.
  C. Tab QUANG-CAO: I = `Đã duyệt`, có F (video) + H (page) + M (caption) → reel lên ĐÚNG page H (không bao giờ all) + Tin 24h page đó,
     L = Post ID, I = `Đã đăng page`. Dòng `Đã đăng page` thiếu Tin → đăng Tin.
Chống trùng 3 lớp: K `Đang đăng <giờ> (máy …)` ghi trước khi đăng (lượt khác thấy < 30 phút thì bỏ qua) · khoá Drive trong fb_api
(mọi máy + đám mây) · fb_api kiểm tra page đã có bài cùng caption.
  D. SEEDING (sếp hỏi 15/11): dòng QUANG-CAO `Đã đăng page` + L, K chưa có `Seeding: đã bình luận` → chính page H bình luận
     10 ảnh Maxfill ngẫu nhiên (Drive ẢNH SEEDING QUẢNG CÁO) + câu tiếng Anh; đếm bình luận ảnh page đã có để không trùng.
     Bài dịch vụ khác Maxfill → ghi `Seeding: lỗi` để Claude chọn ảnh đúng dịch vụ.
Không làm (để Claude/đám mây): bài thiếu caption, sửa bài, làm ảnh.

python dang_tu_dong.py --may truc --thu    # chỉ in việc sẽ làm
python dang_tu_dong.py --may truc          # làm thật
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sheet_api as S  # noqa: E402
import fb_api as F  # noqa: E402

PH = datetime.timezone(datetime.timedelta(hours=8))
VN = datetime.timezone(datetime.timedelta(hours=7))
TAB_PAGE, TAB_QC = "Untitled", "QUANG-CAO"
CAM = ("beauty jobs makati", "beauty jobs manila", "fine beauty clinic")  # page cấm
TMP = os.path.join(tempfile.gettempdir(), "merah-dang-bai")
LOG = os.path.join(tempfile.gettempdir(), "merah-canh-spy", "dang_bai.txt")
TEN_MAY = {"truc": "PC TRỰC", "laptop": "LAPTOP"}


def log(s):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + s + "\n")


def vn():
    return datetime.datetime.now(VN).strftime("%d/%m %H:%M")


def them(k, dong):
    return (k.rstrip() + "\n" if k and k.strip() else "") + dong


def gio_ph(ngay, gio):
    try:
        return datetime.datetime.strptime(f"{ngay.strip()} {gio.strip()}", "%Y-%m-%d %H:%M").replace(tzinfo=PH)
    except Exception:
        return None


def dang_dang_gan(k, phut=30):
    """K có dòng 'Đang đăng dd/mm HH:MM' (giờ VN) trong `phut` phút → True. Tương tự 'Lỗi đăng'."""
    now = datetime.datetime.now(VN)
    for m in re.finditer(r"(Đang đăng|Lỗi đăng|Lỗi Tin) (\d{2})/(\d{2}) (\d{2}):(\d{2})", k or ""):
        try:
            t = now.replace(month=int(m.group(3)), day=int(m.group(2)), hour=int(m.group(4)), minute=int(m.group(5)), second=0)
            if 0 <= (now - t).total_seconds() < phut * 60:
                return True
        except ValueError:
            pass
    return False


def drive_ids(txt):
    return [a or b for a, b in re.findall(r"/d/([\w-]{20,})|[?&]id=([\w-]{20,})", txt or "")]


def tai(fid, thu_muc):
    os.makedirs(thu_muc, exist_ok=True)
    truoc = set(os.listdir(thu_muc))
    r = subprocess.run(["rclone", "backend", "copyid", "merah:", fid, thu_muc + os.sep], capture_output=True, text=True,
                       timeout=900, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    moi = [f for f in os.listdir(thu_muc) if f not in truoc]
    if r.returncode != 0 or not moi:
        raise RuntimeError("không tải được tệp Drive " + fid + ": " + (r.stderr or "")[-200:])
    return os.path.join(thu_muc, moi[0])


def la_video(p):
    return os.path.splitext(p)[1].lower() in (".mp4", ".mov", ".m4v", ".webm")


def da_len(post_id, pid):
    """Bài hẹn giờ đã hiển thị chưa (photo/feed: is_published; reel: published)."""
    import requests
    P = json.load(open(F.PAGES, encoding="utf-8")) if os.path.exists(F.PAGES) else {}
    tok = (P.get(pid) or {}).get("token")
    if not tok or not post_id:
        return None
    for oid, field in ((post_id, "is_published"), (post_id.split("_")[-1], "published")):
        try:
            r = requests.get(f"{F.G}/{oid}", params={"fields": field, "access_token": tok}, timeout=30)
            if r.ok and field in r.json():
                return bool(r.json()[field])
        except Exception:
            pass
    return None


def tin_xong(ok, bo):
    """Tin coi là xong khi đăng được, hoặc khoá Drive báo đã đăng Tin này trong 24h.
    Bỏ qua vì 'page vừa có Tin trong 15 phút' KHÔNG phải xong – lượt sau thử lại."""
    return bool(ok) or any("đã đăng trong 24h" in k["ghi_chu"] for k in bo)


def tom_tat(kq):
    ok = [k for k in kq if k["tt"] == "ok"]
    bo = [k for k in kq if k["tt"] == "bo_qua"]
    loi = [k for k in kq if k["tt"] == "loi"]
    khac_dang = [k for k in bo if "đang đăng" in k["ghi_chu"] or "nhận đăng trước" in k["ghi_chu"]]
    return ok, bo, loi, khac_dang


# ------------------------------------------------------------------ đọc việc
def viec_page(rows, now):
    out = []
    for i, r in enumerate(rows[1:], start=2):
        r = (r + [""] * 12)[:12]
        A, B, C, D, E, Fc, G, H, I, J, K, L = r
        if not A or K.startswith("TRÙNG"):
            continue
        t = gio_ph(B, C)
        if I == "Đã duyệt" and G and E != "Ý tưởng":
            if dang_dang_gan(K):
                continue
            if not H.strip():
                out.append(("page_thieu", i, A, "thiếu caption")); continue
            hen = t and t > now + datetime.timedelta(minutes=15)
            out.append(("page_dang", i, A, "hẹn giờ " + t.strftime("%d/%m %H:%M PH") if hen else "đăng ngay" + (" (bù)" if t and t < now - datetime.timedelta(minutes=10) else "")))
        elif I in ("Đã đăng", "Đã lên lịch") and "TIN 24H: đã đăng" not in K and t and now - datetime.timedelta(hours=24) < t <= now - datetime.timedelta(minutes=2):
            if not dang_dang_gan(K):
                out.append(("page_tin", i, A, "Tin 24h" + (" (kiểm tra bài hẹn đã lên)" if I == "Đã lên lịch" else "")))
    return out


def viec_qc(rows):
    out = []
    for i, r in enumerate(rows[1:], start=2):
        r = (r + [""] * 14)[:14]
        A, B, C, D, E, Fc, G, H, I, J, K, L, M, N = r
        if not A or not A.startswith("QC-"):
            continue
        if I == "Đã duyệt" and Fc and H:
            if dang_dang_gan(K):
                continue
            if H.strip().lower() in CAM or H.strip().lower() in ("all", "tất cả"):
                out.append(("qc_sai_page", i, A, "page cấm/không hợp lệ: " + H)); continue
            if not M.strip():
                out.append(("qc_thieu", i, A, "thiếu caption cột M")); continue
            out.append(("qc_dang", i, A, "reel → " + H))
        elif I == "Đã đăng page" and L and "TIN 24H: đã đăng" not in K and not dang_dang_gan(K):
            out.append(("qc_tin", i, A, "Tin 24h → " + H))
    return out


# ------------------------------------------------------------------ làm việc
def ghi(tab, i, dong, trang_thai=None, cot_l=None):
    """Đọc lại cột K NGAY trước khi ghi rồi nối thêm dòng (không đè dòng lượt khác vừa ghi)."""
    k = (S.get(f"{tab}!K{i}") or [[""]])
    k = (k[0] + [""])[0] if k else ""
    ops = [{"op": "set", "range": f"{tab}!K{i}", "values": [[them(k, dong)]]}]
    if trang_thai:
        ops.append({"op": "set", "range": f"{tab}!I{i}", "values": [[trang_thai]]})
    if cot_l is not None:
        ops.append({"op": "set", "range": f"{tab}!L{i}", "values": [[cot_l]]})
    S.goi(ops)


def dang_tin(tab, i, sel, tep, nhan):
    cmd = "story-video" if la_video(tep) else "story-photo"
    ok, bo, loi, khac = tom_tat(F.chay(cmd, sel, tep))
    if tin_xong(ok, bo):
        ghi(tab, i, f"TIN 24H: đã đăng {vn()} ({nhan if sel != 'all' else str(len(ok) + len(bo)) + ' page'})")
    elif loi and not ok:
        ghi(tab, i, f"Lỗi Tin {vn()}: {loi[0]['ghi_chu'][:120]}")


def lam_page(i, may, now):
    r = (S.get(f"{TAB_PAGE}!A{i}:L{i}")[0] + [""] * 12)[:12]
    A, B, C, D, E, Fc, G, H, I, J, K, L = r
    t = gio_ph(B, C)
    if I != "Đã duyệt" or dang_dang_gan(K):
        return
    ghi(TAB_PAGE, i, f"Đang đăng {vn()} (máy {TEN_MAY[may]})")
    d = os.path.join(TMP, f"page_{A}_{int(time.time())}")
    try:
        files = [tai(fid, d) for fid in drive_ids(G)]
        if not files:
            raise RuntimeError("cột G không có link Drive")
        cmd = "carousel" if len(files) > 1 else ("reel" if la_video(files[0]) else "photo")
        hen = bool(t and t > now + datetime.timedelta(minutes=15))
        at = t.strftime("%Y-%m-%d %H:%M") if hen else None
        ok, bo, loi, khac = tom_tat(F.chay(cmd, "all", files if cmd == "carousel" else files[0], H, at))
        log(f"page {A}: {cmd} at={at} ok={len(ok)} bo={len(bo)} loi={len(loi)}")
        if khac and not ok:
            return  # lượt/máy khác đang đăng bài này
        if not ok and not bo:
            ghi(TAB_PAGE, i, f"Lỗi đăng {vn()}: {loi[0]['ghi_chu'][:150] if loi else '?'} – thử lại sau 30 phút")
            return
        n = len(ok) + len(bo)
        pid0 = next((k for k in ok if k["post_id"]), None)
        ghi_id = f" Post ID {pid0['page']}: {pid0['post_id']}" if pid0 else ""
        if loi:
            ghi_id += f" · lỗi {len(loi)} page: " + ", ".join(k["page"] for k in loi)
        if hen:
            ghi(TAB_PAGE, i, f"Đã hẹn giờ {vn()} ({n} page) cho {t.strftime('%d/%m %H:%M')} PH.{ghi_id}", "Đã lên lịch")
            return
        bu = ", đăng bù – trễ giờ" if t and t < now - datetime.timedelta(minutes=10) else ""
        ghi(TAB_PAGE, i, f"Đã đăng {vn()} ({n} page{bu}).{ghi_id}", "Đã đăng")
        dang_tin(TAB_PAGE, i, "all", files[0], "")
    except Exception as e:
        log(f"page {A} lỗi: {e}")
        ghi(TAB_PAGE, i, f"Lỗi đăng {vn()}: {str(e)[:150]} – thử lại sau 30 phút")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def lam_page_tin(i, may):
    r = (S.get(f"{TAB_PAGE}!A{i}:L{i}")[0] + [""] * 12)[:12]
    A, B, C, D, E, Fc, G, H, I, J, K, L = r
    if I not in ("Đã đăng", "Đã lên lịch") or "TIN 24H: đã đăng" in K or dang_dang_gan(K):
        return
    if I == "Đã lên lịch":
        m = re.search(r"Post ID [^:]+: (\d+_\d+)", K)
        if m and da_len(m.group(1), m.group(1).split("_")[0]) is False:
            return  # bài hẹn chưa lên, đợi lượt sau
        ghi(TAB_PAGE, i, f"Đã đăng {vn()} (đúng giờ hẹn, máy {TEN_MAY[may]} kiểm tra).", "Đã đăng")
    ids = drive_ids(G)
    if not ids:
        return
    d = os.path.join(TMP, f"tin_{A}_{int(time.time())}")
    try:
        dang_tin(TAB_PAGE, i, "all", tai(ids[0], d), "")
    except Exception as e:
        log(f"tin {A} lỗi: {e}")
        ghi(TAB_PAGE, i, f"Lỗi Tin {vn()}: {str(e)[:120]}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def lam_qc(i, may, chi_tin=False):
    r = (S.get(f"{TAB_QC}!A{i}:N{i}")[0] + [""] * 14)[:14]
    A, B, C, D, E, Fc, G, H, I, J, K, L, M, N = r
    pg = H.strip()
    if dang_dang_gan(K) or pg.lower() in CAM or pg.lower() in ("all", "tất cả"):
        return
    if chi_tin and not (I == "Đã đăng page" and "TIN 24H: đã đăng" not in K):
        return
    if not chi_tin and (I != "Đã duyệt" or not M.strip()):
        return
    if not chi_tin:
        ghi(TAB_QC, i, f"Đang đăng {vn()} (máy {TEN_MAY[may]})")
    d = os.path.join(TMP, f"qc_{A}_{int(time.time())}")
    try:
        ids = drive_ids(Fc)
        if not ids:
            raise RuntimeError("cột F không có link Drive")
        vid = tai(ids[0], d)
        if not chi_tin:
            ok, bo, loi, khac = tom_tat(F.chay("reel", pg, vid, M))
            log(f"qc {A}: ok={len(ok)} bo={len(bo)} loi={len(loi)}")
            if khac and not ok:
                return
            if not ok and not bo:
                ghi(TAB_QC, i, f"Lỗi đăng {vn()}: {loi[0]['ghi_chu'][:150] if loi else '?'} – thử lại sau 30 phút")
                return
            pidv = ok[0]["post_id"] if ok else ""
            ghi(TAB_QC, i, f"Đã đăng {vn()} ({pg}). Post ID: {pidv or 'đã có trên page'}", "Đã đăng page", (pidv.split('_')[-1] if pidv else None))
        dang_tin(TAB_QC, i, pg, vid, pg)
    except Exception as e:
        log(f"qc {A} lỗi: {e}")
        ghi(TAB_QC, i, f"Lỗi đăng {vn()}: {str(e)[:150]} – thử lại sau 30 phút")
    finally:
        shutil.rmtree(d, ignore_errors=True)


SEED_N = 10
SEED_CAU = [
    "Real results from our lovely client 💕 Message us to book your session!",
    "Another happy glow-up at MERAH Beauty Makati ✨ Send us a message to book!",
    "Our client's fresh new look 😍 Message us for your free consultation!",
    "Natural, refreshed and confident 💫 Book your Maxfill session today!",
    "Loving these results from our client 💖 Message MERAH Beauty to learn more!",
    "Glowing and happy – thank you for trusting MERAH Beauty 🥰 Message us to book!",
    "Real client, real smile ✨ Chat with us to reserve your slot!",
    "Fresh, youthful glow from our lovely client 🌸 Message us now!",
    "Thank you for choosing MERAH Beauty Makati 💕 Book your glow-up today!",
    "Your turn to glow ✨ Message us to book your Maxfill consultation!",
    "So happy with how she looks 😊 Message us for our Christmas Deal!",
    "Results our clients love 💖 Send us a message to get started!",
]
SEED_ROOT_ID = "{{ID_DRIVE}}"  # Drive MERAH/ẢNH SEEDING QUẢNG CÁO
SEED_THU_MUC = "MAXFILL COLLAGEN (filler-botox)"
SEED_DICH_VU_KHAC = ("stemcell", "cryo", "giảm cân", "weight loss", "body sculpt")


def viec_seed(rows):
    out = []
    for i, r in enumerate(rows[1:], start=2):
        r = (r + [""] * 14)[:14]
        A, I, K, L, M = r[0], r[8], r[10], r[11], r[12]
        if not (A.startswith("QC-") and I == "Đã đăng page" and L.strip()):
            continue
        if "Seeding: đã bình luận" in K or "Seeding: lỗi" in K:
            continue  # xong rồi, hoặc lỗi chờ sếp/Claude xem (xoá dòng lỗi để thử lại)
        if "Đang seeding" in K and not dang_seed_cu(K):
            continue
        out.append(("qc_seed", i, A, "seeding 10 ảnh"))
    return out


def dang_seed_cu(k):
    """'Đang seeding' quá 40 phút (lượt trước chết giữa chừng) → làm tiếp."""
    m = None
    for m in re.finditer(r"Đang seeding (\d{2})/(\d{2}) (\d{2}):(\d{2})", k or ""):
        pass
    if not m:
        return False
    now = datetime.datetime.now(VN)
    try:
        t = now.replace(month=int(m.group(2)), day=int(m.group(1)), hour=int(m.group(3)), minute=int(m.group(4)), second=0)
    except ValueError:
        return False
    return (now - t).total_seconds() > 40 * 60


def lam_seed(i, may):
    import random, requests
    r = (S.get(f"{TAB_QC}!A{i}:N{i}")[0] + [""] * 14)[:14]
    A, H, I, K, L, M = r[0], r[7], r[8], r[10], r[11], r[12]
    if I != "Đã đăng page" or not L.strip() or "Seeding: đã bình luận" in K:
        return
    if "Seeding: lỗi" in K or ("Đang seeding" in K and not dang_seed_cu(K)):
        return
    if any(w in (M + " " + r[6]).lower() for w in SEED_DICH_VU_KHAC):
        ghi(TAB_QC, i, f"Seeding: lỗi – bài không phải Maxfill, cần Claude chọn ảnh đúng dịch vụ ({vn()})")
        return
    (pid, p), = F.load_pages(H.strip())
    post = f"{pid}_{L.strip().split('_')[-1]}"
    ok_k, ten = F.giu_khoa("SEED_" + post.replace("_", "-"))
    if not ok_k:
        return
    ghi(TAB_QC, i, f"Đang seeding {vn()} (máy {TEN_MAY[may]})")
    d = os.path.join(TMP, f"seed_{A}_{int(time.time())}")
    xong = False
    try:
        # đã có bao nhiêu bình luận ảnh của chính page → chỉ đăng phần còn thiếu (không trùng)
        co = 0
        rr = requests.get(f"{F.G}/{post}/comments", params={"fields": "from{id},attachment", "limit": 100,
                                                            "filter": "stream", "access_token": p["token"]}, timeout=60)
        if rr.ok:
            co = sum(1 for c in rr.json().get("data", []) if (c.get("from") or {}).get("id") == pid and c.get("attachment"))
        can = SEED_N - co
        if can > 0:
            src, goc_id = f"merah:{SEED_THU_MUC}", ["--drive-root-folder-id", SEED_ROOT_ID]
            ls = F._rc("lsf", src, "--files-only", *goc_id, timeout=120)
            anh = [x for x in (ls.stdout.splitlines() if ls and ls.returncode == 0 else [])
                   if os.path.splitext(x)[1].lower() in (".jpg", ".jpeg", ".png", ".webp")]
            if len(anh) < can:
                raise RuntimeError(f"thư mục ảnh Maxfill chỉ có {len(anh)} ảnh")
            chon = random.sample(anh, can)
            cau = random.sample(SEED_CAU, len(SEED_CAU))
            os.makedirs(d, exist_ok=True)
            ds = os.path.join(TMP, f"seed_ds_{int(time.time())}.txt")
            open(ds, "w", encoding="utf-8").write("\n".join(chon))
            F._rc("copy", src, d, "--files-from", ds, *goc_id, timeout=600)  # tải cả lô 1 lệnh (nhanh hơn từng ảnh)
            os.remove(ds)
            for n, ten_anh in enumerate(chon):
                if not os.path.exists(os.path.join(d, ten_anh)):
                    raise RuntimeError("không tải được ảnh " + ten_anh)
                with open(os.path.join(d, ten_anh), "rb") as fh:
                    rp = requests.post(f"{F.G}/{post}/comments", data={"message": cau[n % len(cau)], "access_token": p["token"]},
                                       files={"source": fh}, timeout=120)
                if not rp.ok:
                    raise RuntimeError(F.err_text(rp)[:150])
                co += 1
                time.sleep(3)
        ghi(TAB_QC, i, f"Seeding: đã bình luận {datetime.datetime.now(PH).strftime('%d/%m %H:%M')} PH ({co} ảnh Maxfill, page {p['name']}, máy {TEN_MAY[may]})")
        xong = True
        log(f"seed {A}: {co} ảnh")
    except Exception as e:
        log(f"seed {A} lỗi: {e}")
        ghi(TAB_QC, i, f"Seeding: lỗi – {str(e)[:150]} ({vn()})")
    finally:
        F.tha_khoa(ten, xong)
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--may", choices=["truc", "laptop"], required=True)
    ap.add_argument("--thu", action="store_true")
    a = ap.parse_args()
    if not S.co_cau_hinh():
        log("chưa có Sheet API – bỏ qua"); return
    now = datetime.datetime.now(PH)
    data = S.goi([{"op": "get", "range": f"{TAB_PAGE}!A1:L"}, {"op": "get", "range": f"{TAB_QC}!A1:N"}])
    vp, vq = viec_page(data[0]["values"], now), viec_qc(data[1]["values"])
    vs = viec_seed(data[1]["values"])
    if a.thu:
        print(json.dumps({"page": vp, "qc": vq, "seed": vs}, ensure_ascii=False, indent=1)); return
    viec = vp + vq + vs
    if a.may == "laptop":  # laptop là dự phòng: chỉ nhận việc đã chờ >= 3 phút mà máy trực chưa làm
        stf = os.path.join(tempfile.gettempdir(), "merah-canh-spy", "dang_bai_thay.json")
        try:
            st = json.load(open(stf, encoding="utf-8"))
        except Exception:
            st = {}
        t = time.time()
        st = {k: st.get(k, t) for k in (f"{l}|{m}" for l, _, m, _ in viec)}
        json.dump(st, open(stf, "w", encoding="utf-8"))
        viec = [v for v in viec if t - st[f"{v[0]}|{v[2]}"] >= 180]
    for loai, i, ma, mo_ta in viec:
        try:
            if loai == "page_dang":
                lam_page(i, a.may, now)
            elif loai == "page_tin":
                lam_page_tin(i, a.may)
            elif loai == "qc_dang":
                lam_qc(i, a.may)
            elif loai == "qc_tin":
                lam_qc(i, a.may, chi_tin=True)
            elif loai == "qc_seed":
                lam_seed(i, a.may)
        except SystemExit as e:
            log(f"{ma}: fb_api dừng: {e}")
        except Exception as e:
            log(f"{ma}: lỗi {e}")


if __name__ == "__main__":
    lock = os.path.join(tempfile.gettempdir(), "merah-canh-spy", "dang_bai.lock")
    os.makedirs(os.path.dirname(lock), exist_ok=True)
    if "--thu" not in sys.argv and os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 45 * 60:
        sys.exit(0)  # lượt trước còn đang đăng
    try:
        if "--thu" not in sys.argv:
            open(lock, "w").write(str(time.time()))
        main()
    except Exception as e:
        log(f"lỗi: {e}")
        if "--thu" in sys.argv:
            raise
    finally:
        if "--thu" not in sys.argv:
            try:
                os.remove(lock)
            except OSError:
                pass
