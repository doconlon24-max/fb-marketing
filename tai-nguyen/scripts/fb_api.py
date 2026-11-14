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
import json, os, sys, time, datetime
import requests

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
    return requests.post(f"{G}/{pid}/video_reels", data=d, timeout=120)


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
    pages = load_pages(a[1])
    ok = 0
    for pid, p in pages:
        if not force:
            capf = {"photo": 3, "carousel": 2, "reel": 3}.get(cmd)
            if capf is not None and da_co_bai(pid, p, open(a[capf], encoding="utf-8").read()):
                ok += 1; print(f"BỎ QUA {p['name']}: đã có bài cùng caption trong 12h (chống đăng trùng). Dùng --force nếu thật sự muốn đăng lại."); continue
            if cmd.startswith("story") and da_co_tin(pid, p):
                ok += 1; print(f"BỎ QUA {p['name']}: page vừa có Tin 24h trong 15 phút (chống đăng trùng). Dùng --force nếu cần."); continue
        if cmd == "photo":
            r = photo(pid, p, a[2], open(a[3], encoding="utf-8").read(), at)
        elif cmd == "carousel":
            r = carousel(pid, p, open(a[2], encoding="utf-8").read(), a[3:], at)
        elif cmd == "reel":
            r = reel(pid, p, a[2], open(a[3], encoding="utf-8").read(), at)
        elif cmd == "story-photo":
            r = story_photo(pid, p, a[2])
        elif cmd == "story-video":
            r = story_video(pid, p, a[2])
        else:
            die("Lệnh không hợp lệ: " + cmd)
        if r.ok:
            ok += 1; print(f"OK  {p['name']}: {r.json()}")
        else:
            print(f"LỖI {p['name']}: {err_text(r)}")
    print(f"Xong {ok}/{len(pages)} page.")


if __name__ == "__main__":
    main()
