"""Tạo ảnh AI bằng Higgsfield API cho MERAH (sếp yêu cầu 10/11/2026). KHÔNG in khoá.
Khoá: biến môi trường HIGGSFIELD_API_KEY dạng "KEY_ID:KEY_SECRET" (hoặc 2 biến HF_API_KEY_ID + HF_API_KEY_SECRET).
Trên máy: file C:\\MERAH\\.bao-mat\\higgsfield.txt (nếu sếp tự dán).

python higgsfield.py anh "<prompt hoặc đường dẫn .txt>" <ra.png> [--mau ideogram|soul] [--ty-le 9:16] [--chat-luong 1080p] [--so 1|4] [--anh-mau URL]
  --mau ideogram (mặc định): Ideogram 4.0 – vẽ CHỮ tốt, hợp poster có chữ/giá. Tỉ lệ: 9:16, 4:5, 1:1, 3:4, 2:3...
                              --anh-mau URL công khai để làm lại theo ảnh mẫu (remix).
  --mau soul               : SOUL V2 – ảnh chân thực kiểu tạp chí, hợp NỀN / người mẫu lifestyle. Tỉ lệ: 9:16, 3:4, 1:1, 2:3...
                              --chat-luong 720p|1080p, --so 1 hoặc 4 ảnh.
Ra: <ra>.png (nhiều ảnh thì <ra>_1.png, _2.png...) + <ra>.json (request_id, mẫu, prompt).
Quy tắc ảnh AI MERAH: không kim tiêm, không before/after, không bịa khách/bác sĩ; ảnh có người do AI tạo phải gắn nhãn AI.
"""
import json, os, sys, time, uuid
import requests

API = "https://api.higgsfield.ai"
MAU = {"ideogram": "/ideogram/v4.0", "soul": "/higgsfield-ai/soul/v2/standard"}


def auth():
    k = os.environ.get("HIGGSFIELD_API_KEY", "").strip().strip("'\"")
    if not k and os.environ.get("HF_API_KEY_ID") and os.environ.get("HF_API_KEY_SECRET"):
        k = os.environ["HF_API_KEY_ID"].strip() + ":" + os.environ["HF_API_KEY_SECRET"].strip()
    if not k:
        p = r"C:\MERAH\.bao-mat\higgsfield.txt"
        if os.path.exists(p):
            k = open(p, encoding="utf-8").read().strip()
    if not k:
        sys.exit("LỖI: chưa có khoá Higgsfield (HIGGSFIELD_API_KEY dạng KEY_ID:KEY_SECRET)")
    if ":" not in k:
        print("CẢNH BÁO: khoá không có dạng KEY_ID:KEY_SECRET – Higgsfield cần cả ID và SECRET, có thể bị từ chối.")
    return {"Authorization": "Key " + k, "Content-Type": "application/json"}


def tao(prompt, ra, mau="ideogram", ty_le="9:16", chat_luong="1080p", so=1, anh_mau=None):
    if os.path.exists(prompt) and prompt.endswith(".txt"):
        prompt = open(prompt, encoding="utf-8").read().strip()
    if mau == "ideogram":
        body = {"prompt": prompt[:2048], "aspect_ratio": ty_le, "rendering_speed": "QUALITY"}
        if anh_mau:
            body["image_url"] = anh_mau
    else:
        body = {"prompt": prompt, "aspect_ratio": ty_le, "resolution": chat_luong, "batch_size": 4 if so >= 4 else 1}
    h = auth(); h["Idempotency-Key"] = str(uuid.uuid4())
    r = requests.post(API + MAU[mau], headers=h, json=body, timeout=60)
    if not r.ok:
        if "not_enough_credits" in r.text:
            sys.exit("LỖI: tài khoản Higgsfield HẾT CREDIT API – sếp cần nạp credit tại cloud.higgsfield.ai rồi chạy lại.")
        sys.exit(f"LỖI gửi yêu cầu {r.status_code}: {r.text[:400]}")
    j = r.json(); rid = j.get("request_id"); st_url = j.get("status_url") or f"{API}/requests/{rid}/status"
    print("Đã gửi:", mau, rid)
    t0 = time.time()
    while True:
        time.sleep(4)
        s = requests.get(st_url, headers=auth(), timeout=30)
        if not s.ok:
            if time.time() - t0 > 600:
                sys.exit(f"LỖI kiểm tra trạng thái {s.status_code}: {s.text[:300]}")
            continue
        sj = s.json(); stt = sj.get("status")
        if stt == "completed":
            break
        if stt in ("failed", "nsfw", "canceled"):
            sys.exit(f"LỖI: Higgsfield trả về '{stt}': {json.dumps(sj)[:400]}")
        if time.time() - t0 > 600:
            sys.exit("LỖI: quá 10 phút chưa xong, request_id " + str(rid))
    imgs = [i.get("url") for i in sj.get("images", []) if i.get("url")]
    if not imgs:
        sys.exit("LỖI: xong nhưng không có ảnh: " + json.dumps(sj)[:300])
    base, ext = os.path.splitext(ra); ext = ext or ".png"; ra_list = []
    for n, u in enumerate(imgs, 1):
        f = ra if len(imgs) == 1 else f"{base}_{n}{ext}"
        d = requests.get(u, timeout=120); d.raise_for_status(); open(f, "wb").write(d.content); ra_list.append(f)
    json.dump({"request_id": rid, "mau": mau, "body": body, "anh": ra_list, "luc": time.strftime("%Y-%m-%d %H:%M:%S")},
              open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Xong:", ", ".join(ra_list), f"({time.time() - t0:.0f}s)")
    return ra_list


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] != "anh" or len(a) < 3:
        sys.exit(__doc__)
    g = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    tao(a[1], a[2], g("--mau", "ideogram"), g("--ty-le", "9:16"), g("--chat-luong", "1080p"), int(g("--so", "1")), g("--anh-mau"))
