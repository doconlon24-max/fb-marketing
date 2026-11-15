"""Đăng bài lên các page MERAH qua Facebook Graph API. KHÔNG bao giờ in token ra màn hình.
Token người dùng: C:\\MERAH\\.bao-mat\\facebook.txt (người dùng tự dán). Token page lưu ở C:\\MERAH\\.bao-mat\\pages.json.

python fb_api.py check                       # kiểm tra token, lấy token từng page, in tên page
python fb_api.py photo <page> <ảnh> <caption.txt> [--at "2026-11-10 07:00"]   # giờ PH; bỏ --at = đăng ngay
python fb_api.py carousel <page> <caption.txt> <ảnh1> <ảnh2> ... [--at ...]
python fb_api.py reel <page> <video.mp4> <caption.txt> [--at ...]
python fb_api.py story-photo <page> <ảnh>    # Tin 24h (API chỉ cho đăng ngay)
python fb_api.py story-video <page> <video>
<page> = page id, tên page, hoặc "all" (cả 10 page).
"""
import json, os, sys, time, datetime, hashlib, shutil, socket, subprocess
import requests
try:  # rclone chạy được cả khi gọi từ lịch Windows (cấu hình trong thư mục ảo app Claude)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from duong_dan_may import dat_rclone
    dat_rclone()
except Exception:
    pass

V = "v22.0"
G = f"https://graph.facebook.com/{V}"
# Trên máy: C:\MERAH\.bao-mat. Trên đám mây: token lấy từ biến bí mật FB_USER_TOKEN,
# pages.json lưu ở thư mục tạm (MERAH_SECRET_DIR hoặc ~/.merah-bao-mat). Không bao giờ đưa lên GitHub.
_LOCAL = r"C:\MERAH\.bao-mat"
SEC = os.environ.get("MERAH_SECRET_DIR") or (_LOCAL if os.path.isdir(_LOCAL) else os.path.join(os.path.expanduser("~"), ".merah-bao-mat"))
os.makedirs(SEC, exist_ok=True)
TOK = os.path.join(SEC, "facebook.txt")
PAGES = os.path.join(SEC, "pages.json")
PH = datetime.timezone(datetime.timedelta(hours=8))
# 10 page MERAH người dùng chốt (08/11/2026). "all" chỉ đăng lên đúng các page này.
MERAH10 = ["{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}",
           "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}"]


def die(msg):
    print("LỖI:", msg); sys.exit(1)


def err_text(r):
    try:
        e = r.json().get("error", {})
        return f"{e.get('type','')} {e.get('code','')}: {e.get('message','')}"
    except Exception:
        return r.text[:300]


def user_token():
    env = os.environ.get("FB_USER_TOKEN", "").strip()
    if env:
        return env
    if not os.path.exists(TOK):
        die("Chưa có file token " + TOK)
    t = open(TOK, encoding="utf-8").read().strip()
    if not t:
        die("File token đang trống. Người dùng cần dán token dài hạn vào " + TOK)
    return t


def check():
    t = user_token()
    r = requests.get(f"{G}/me", params={"fields": "id,name", "access_token": t}, timeout=30)
    if not r.ok:
        die("Token không dùng được – " + err_text(r))
    me = r.json()
    print("Token hợp lệ, tài khoản:", me.get("name"))
    pages, url, params = [], f"{G}/me/accounts", {"fields": "id,name,access_token,tasks", "limit": 100, "access_token": t}
    while url:
        r = requests.get(url, params=params, timeout=30)
        if not r.ok:
            die("Không lấy được danh sách page – " + err_text(r))
        d = r.json(); pages += d.get("data", []); url = d.get("paging", {}).get("next"); params = None
    out = {p["id"]: {"name": p["name"], "token": p["access_token"], "tasks": p.get("tasks", [])} for p in pages}
    with open(PAGES, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Lấy được {len(out)} page:")
    for pid, p in out.items():
        can = "đăng được" if ("CREATE_CONTENT" in p["tasks"] or "MANAGE" in p["tasks"]) else "THIẾU QUYỀN ĐĂNG"
        print(f"  - {p['name']} ({pid}) – {can}")
    # hạn token người dùng (nếu có app token thì debug_token; ở đây ước lượng bằng thông báo)
    print("Token page đã lưu vào", PAGES)


def load_pages(sel):
    if not os.path.exists(PAGES):
        if os.environ.get("FB_USER_TOKEN"):
            check()  # đám mây: tự lấy token page mỗi lần chạy
        else:
            die("Chưa có pages.json – chạy: python fb_api.py check")
    P = json.load(open(PAGES, encoding="utf-8"))
    if sel == "all":
        miss = [i for i in MERAH10 if i not in P]
        if miss:
            die("Token thiếu quyền page: " + ", ".join(miss))
        return [(i, P[i]) for i in MERAH10]
    for pid, p in P.items():
        if pid not in MERAH10:
            continue
        if sel == pid or sel.lower() == p["name"].lower():
            return [(pid, p)]
    die("Không thấy page: " + sel)


def ts(at):
    if not at:
        return None
    d = datetime.datetime.strptime(at, "%Y-%m-%d %H:%M").replace(tzinfo=PH)
    s = int(d.timestamp())
    if s < time.time() + 11 * 60:
        die("Giờ hẹn phải sau ít nhất 10 phút so với hiện tại")
    return s


def sched(data, at):
    s = ts(at)
    if s:
        data.update(published="false", scheduled_publish_time=str(s))
    return data


def photo(pid, p, img, cap, at):
    d = sched({"caption": cap, "access_token": p["token"]}, at)
    r = requests.post(f"{G}/{pid}/photos", data=d, files={"source": open(img, "rb")}, timeout=300)
    return r


def carousel(pid, p, cap, imgs, at):
    ids = []
    for im in imgs:
        r = requests.post(f"{G}/{pid}/photos", data={"published": "false", "temporary": "true" if at else "false", "access_token": p["token"]},
                          files={"source": open(im, "rb")}, timeout=300)
        if not r.ok:
            return r
        ids.append({"media_fbid": r.json()["id"]})
    d = sched({"message": cap, "attached_media": json.dumps(ids), "access_token": p["token"]}, at)
    return requests.post(f"{G}/{pid}/feed", data=d, timeout=120)


def reel(pid, p, vid, cap, at):
    tok = p["token"]
    r = requests.post(f"{G}/{pid}/video_reels", data={"upload_phase": "start", "access_token": tok}, timeout=60)
    if not r.ok:
        return r
    vid_id, up = r.json()["video_id"], r.json()["upload_url"]
    size = os.path.getsize(vid)
    r = requests.post(up, headers={"Authorization": f"OAuth {tok}", "offset": "0", "file_size": str(size)}, data=open(vid, "rb"), timeout=900)
    if not r.ok:
        return r
    d = {"upload_phase": "finish", "video_id": vid_id, "description": cap, "access_token": tok}
    s = ts(at)
    d.update({"video_state": "SCHEDULED", "scheduled_publish_time": str(s)} if s else {"video_state": "PUBLISHED"})
    r = requests.post(f"{G}/{pid}/video_reels", data=d, timeout=120)
    r.video_id = vid_id
    return r


def post_id(pid, r):
    """Lấy ID bài dạng <pageid>_<postid> (reel: <pageid>_<videoid>)."""
    try:
        j = r.json()
    except Exception:
        j = {}
    v = j.get("post_id") or j.get("id") or getattr(r, "video_id", "") or ""
    return v if (not v or "_" in str(v)) else f"{pid}_{v}"


def story_photo(pid, p, img):
    r = requests.post(f"{G}/{pid}/photos", data={"published": "false", "access_token": p["token"]}, files={"source": open(img, "rb")}, timeout=300)
    if not r.ok:
        return r
    return requests.post(f"{G}/{pid}/photo_stories", data={"photo_id": r.json()["id"], "access_token": p["token"]}, timeout=120)


def story_video(pid, p, vid):
    tok = p["token"]
    r = requests.post(f"{G}/{pid}/video_stories", data={"upload_phase": "start", "access_token": tok}, timeout=60)
    if not r.ok:
        return r
    vid_id, up = r.json()["video_id"], r.json()["upload_url"]
    r = requests.post(up, headers={"Authorization": f"OAuth {tok}", "file_url": ""} if False else {"Authorization": f"OAuth {tok}", "offset": "0", "file_size": str(os.path.getsize(vid))},
                      data=open(vid, "rb"), timeout=900)
    if not r.ok:
        return r
    return requests.post(f"{G}/{pid}/video_stories", data={"upload_phase": "finish", "video_id": vid_id, "access_token": tok}, timeout=120)


def _norm(s):
    return " ".join((s or "").split()).lower()[:80]


def da_co_bai(pid, p, cap, hours=12):
    """Chống đăng trùng (14/11/2026): page đã có bài (đã đăng / đã hẹn giờ / reel) cùng caption trong 12h → True."""
    key = _norm(cap)
    if not key:
        return False
    since = int(time.time() - hours * 3600)
    tok = p["token"]
    for edge, field in (("published_posts", "message"), ("scheduled_posts", "message"), ("video_reels", "description")):
        try:
            r = requests.get(f"{G}/{pid}/{edge}", params={"fields": field + ",created_time", "limit": 25, "access_token": tok}, timeout=30)
            for x in (r.json().get("data", []) if r.ok else []):
                ct = x.get("created_time", "")
                try:
                    t = datetime.datetime.strptime(ct[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp()
                except Exception:
                    t = time.time()
                if t >= since and _norm(x.get(field)) == key:
                    return True
        except Exception:
            pass
    return False


def da_co_video(pid, p, cap, hours=12):
    """Reel vừa tải lên còn đang xử lý / đã hẹn giờ chưa hiện ở video_reels → xem thêm /videos."""
    key = _norm(cap)
    if not key:
        return False
    since = time.time() - hours * 3600
    try:
        r = requests.get(f"{G}/{pid}/videos", params={"fields": "description,created_time", "limit": 25, "access_token": p["token"]}, timeout=30)
        for x in (r.json().get("data", []) if r.ok else []):
            try:
                t = datetime.datetime.strptime(x.get("created_time", "")[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp()
            except Exception:
                t = time.time()
            if t >= since and _norm(x.get("description")) == key:
                return True
    except Exception:
        pass
    return False


# ---- KHOÁ ĐĂNG BÀI dùng chung mọi máy + đám mây (15/11/2026, sếp yêu cầu chống đăng trùng tuyệt đối) ----
# Mỗi lần đăng 1 page tạo tệp trên Drive  merah:"KHÓA ĐĂNG BÀI"/<khoá>__<epoch>__<máy>__CHO.txt
# - đã có tệp ...__XONG trong 24h  -> bài này đã đăng, bỏ qua
# - đang có tệp ...__CHO < 20 phút của lượt khác -> lượt khác đang đăng, bỏ qua
# - 2 lượt tạo khoá cùng lúc -> chờ 4 giây, lượt có epoch nhỏ nhất thắng, lượt kia rút
# Không có rclone (hoặc Drive lỗi) -> vẫn chống trùng bằng kiểm tra trên Facebook như cũ.
KHOA_DIR = os.environ.get("MERAH_KHOA_DIR", "")  # tự dò: máy (gốc = thư mục MERAH) / đám mây (gốc = My Drive → MERAH/)
MAY = os.environ.get("MERAH_MAY") or socket.gethostname()


def _rc(*args, timeout=60):
    exe = shutil.which("rclone")
    if not exe:
        return None
    try:
        return subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8", timeout=timeout,
                              creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except Exception:
        return None


def _thu_muc_khoa():
    global KHOA_DIR
    if not KHOA_DIR:
        r = _rc("lsf", "merah:", "--dirs-only", "--max-depth", "1")
        goc_drive = r is not None and r.returncode == 0 and "MERAH/" in (r.stdout or "").split()
        KHOA_DIR = "merah:MERAH/KHÓA ĐĂNG BÀI" if goc_drive else "merah:KHÓA ĐĂNG BÀI"
    return KHOA_DIR


def _ds_khoa(key):
    _thu_muc_khoa()
    r = _rc("lsf", KHOA_DIR, "--files-only", "--include", key + "__*")
    if r is None or (r.returncode != 0 and "not found" not in (r.stderr or "")):
        return None
    out = []
    for n in (r.stdout or "").split():
        parts = n[:-4].split("__") if n.endswith(".txt") else []
        if len(parts) == 4 and parts[1].isdigit():
            out.append((int(parts[1]), n, parts[3]))
    return out


def khoa_key(pid, cmd, cap, media):
    if cmd.startswith("story"):
        try:
            sig = os.path.basename(media) + str(os.path.getsize(media))
        except Exception:
            sig = os.path.basename(media or "")
        raw = f"{pid}|tin|{sig}"
    else:
        raw = f"{pid}|bai|{' '.join((cap or '').split()).lower()}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def giu_khoa(key):
    """Trả (True, tên tệp khoá) nếu được đăng; (False, lý do) nếu phải bỏ qua; (True, None) nếu không khoá được (Drive lỗi)."""
    now = time.time()
    ds = _ds_khoa(key)
    if ds is None:
        return True, None
    if any(st == "XONG" and t > now - 24 * 3600 for t, _, st in ds):
        return False, "đã đăng trong 24h (khoá Drive)"
    if any(st == "CHO" and t > now - 20 * 60 for t, _, st in ds):
        return False, "lượt/máy khác đang đăng bài này"
    ten = f"{key}__{int(now)}__{MAY.replace('__', '_')}__CHO.txt"
    r = _rc("touch", f"{KHOA_DIR}/{ten}")
    if r is None or r.returncode != 0:
        return True, None
    time.sleep(4)
    ds = _ds_khoa(key) or []
    cho = sorted((t, n) for t, n, st in ds if st == "CHO" and t > now - 20 * 60)
    if any(st == "XONG" and t > now - 24 * 3600 for t, _, st in ds) or (cho and cho[0][1] != ten):
        _rc("deletefile", f"{KHOA_DIR}/{ten}", "--drive-use-trash=false")
        return False, "lượt/máy khác nhận đăng trước"
    return True, ten


def tha_khoa(ten, ok):
    if not ten:
        return
    if ok:
        _rc("moveto", f"{KHOA_DIR}/{ten}", f"{KHOA_DIR}/{ten[:-len('__CHO.txt')]}__XONG.txt")
    else:
        _rc("deletefile", f"{KHOA_DIR}/{ten}", "--drive-use-trash=false")


def don_khoa_cu():
    _thu_muc_khoa()
    _rc("delete", KHOA_DIR, "--min-age", "3d", "--drive-use-trash=false", timeout=120)


def da_co_tin(pid, p, minutes=15):
    """Chống đăng trùng Tin 24h: page vừa có Tin trong 15 phút → True."""
    try:
        r = requests.get(f"{G}/{pid}/stories", params={"limit": 5, "access_token": p["token"]}, timeout=30)
        for x in (r.json().get("data", []) if r.ok else []):
            t = int(x.get("creation_time") or 0)
            if t and t >= time.time() - minutes * 60:
                return True
    except Exception:
        pass
    return False


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    force = "--force" in a
    if force:
        a.remove("--force")
    at = None
    if "--at" in a:
        i = a.index("--at"); at = a[i + 1]; del a[i:i + 2]
    cmd = a[0]
    if cmd == "check":
        return check()
    capf = {"photo": 3, "carousel": 2, "reel": 3}.get(cmd)
    cap = open(a[capf], encoding="utf-8").read() if capf is not None else ""
    if cmd == "carousel":
        media = a[3:]
    else:
        media = a[2]
    kq = chay(cmd, a[1], media, cap, at, force)
    for k in kq:
        print(("OK  " if k["tt"] == "ok" else "BỎ QUA " if k["tt"] == "bo_qua" else "LỖI ") + f"{k['page']}: {k['ghi_chu']}")
    print(f"Xong {sum(1 for k in kq if k['tt'] != 'loi')}/{len(kq)} page.")


def chay(cmd, sel, media, cap="", at=None, force=False):
    """Đăng 1 bài lên 1 hoặc nhiều page, có khoá chống trùng. Trả list dict:
    {page, pid, tt: ok|bo_qua|loi, post_id, ghi_chu}. media: đường dẫn tệp (carousel: list tệp)."""
    if cmd not in ("photo", "carousel", "reel", "story-photo", "story-video"):
        die("Lệnh không hợp lệ: " + cmd)
    pages = load_pages(sel)
    m1 = media[0] if isinstance(media, list) else media
    if not force:
        don_khoa_cu()
    out = []
    for pid, p in pages:
        ten_khoa = None
        if not force:
            duoc, ten_khoa = giu_khoa(khoa_key(pid, cmd, cap, m1))
            if not duoc:
                out.append(dict(page=p["name"], pid=pid, tt="bo_qua", post_id="", ghi_chu=f"{ten_khoa} (chống đăng trùng)")); continue
            if cmd in ("photo", "carousel", "reel") and (da_co_bai(pid, p, cap) or (cmd == "reel" and da_co_video(pid, p, cap))):
                tha_khoa(ten_khoa, True)  # trên page đã có → ghi XONG để lượt sau khỏi kiểm tra lại
                out.append(dict(page=p["name"], pid=pid, tt="bo_qua", post_id="", ghi_chu="đã có bài cùng caption trong 12h (chống đăng trùng)")); continue
            if cmd.startswith("story") and da_co_tin(pid, p):
                tha_khoa(ten_khoa, False)
                out.append(dict(page=p["name"], pid=pid, tt="bo_qua", post_id="", ghi_chu="page vừa có Tin 24h trong 15 phút (chống đăng trùng)")); continue
        try:
            if cmd == "photo":
                r = photo(pid, p, m1, cap, at)
            elif cmd == "carousel":
                r = carousel(pid, p, cap, media, at)
            elif cmd == "reel":
                r = reel(pid, p, m1, cap, at)
            elif cmd == "story-photo":
                r = story_photo(pid, p, m1)
            else:
                r = story_video(pid, p, m1)
        except Exception as e:
            tha_khoa(ten_khoa, False)
            out.append(dict(page=p["name"], pid=pid, tt="loi", post_id="", ghi_chu=str(e)[:200])); continue
        tha_khoa(ten_khoa, r.ok)
        if r.ok:
            out.append(dict(page=p["name"], pid=pid, tt="ok", post_id=post_id(pid, r), ghi_chu=str(r.json())[:200]))
        else:
            out.append(dict(page=p["name"], pid=pid, tt="loi", post_id="", ghi_chu=err_text(r)))
    return out


if __name__ == "__main__":
    main()
