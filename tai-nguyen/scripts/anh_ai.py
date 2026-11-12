"""Tạo ảnh AI qua nhiều nhà cung cấp – mỗi người tự chọn công cụ mình có.

Dùng:  python3 tai-nguyen/scripts/anh_ai.py <prompt.txt|"câu lệnh"> <out.png> [--ty-le 9:16|4:5|1:1|16:9] [--nguon openai|gemini|higgsfield|replicate]

Không ghi --nguon thì lấy biến môi trường ANH_AI_NGUON, không có nữa thì tự chọn
theo khoá đang có (OPENAI_API_KEY → GEMINI_API_KEY → HIGGSFIELD_API_KEY → REPLICATE_API_TOKEN).
Khoá chỉ đọc từ biến môi trường, không bao giờ in ra.

Tên model đổi được bằng biến môi trường (nhà cung cấp hay đổi tên model):
  OPENAI_IMAGE_MODEL (mặc định gpt-image-1)
  GEMINI_IMAGE_MODEL (mặc định imagen-4.0-generate-001)
  REPLICATE_IMAGE_MODEL (mặc định black-forest-labs/flux-1.1-pro)
"""
import base64, json, os, subprocess, sys, time, urllib.request

def doc_prompt(x):
    return open(x, encoding="utf-8").read().strip() if os.path.isfile(x) else x

def http(url, body=None, headers=None, method=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", **(headers or {})}, method=method)
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())

def tai(url, out):
    with urllib.request.urlopen(url, timeout=300) as r, open(out, "wb") as f:
        f.write(r.read())

def openai(prompt, out, tl):
    size = {"9:16": "1024x1536", "4:5": "1024x1536", "1:1": "1024x1024", "16:9": "1536x1024"}.get(tl, "1024x1536")
    d = http("https://api.openai.com/v1/images/generations",
             {"model": os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"), "prompt": prompt, "size": size, "n": 1},
             {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
    it = d["data"][0]
    if it.get("b64_json"):
        open(out, "wb").write(base64.b64decode(it["b64_json"]))
    else:
        tai(it["url"], out)

def gemini(prompt, out, tl):
    m = os.environ.get("GEMINI_IMAGE_MODEL", "imagen-4.0-generate-001")
    d = http(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:predict",
             {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": tl if tl in ("9:16", "1:1", "16:9", "3:4", "4:3") else "3:4"}},
             {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    open(out, "wb").write(base64.b64decode(d["predictions"][0]["bytesBase64Encoded"]))

def replicate(prompt, out, tl):
    m = os.environ.get("REPLICATE_IMAGE_MODEL", "black-forest-labs/flux-1.1-pro")
    h = {"Authorization": "Bearer " + os.environ["REPLICATE_API_TOKEN"], "Prefer": "wait"}
    d = http(f"https://api.replicate.com/v1/models/{m}/predictions", {"input": {"prompt": prompt, "aspect_ratio": tl}}, h)
    for _ in range(120):
        if d.get("status") in ("succeeded", "failed", "canceled"):
            break
        time.sleep(3)
        d = http(d["urls"]["get"], headers=h, method="GET")
    if d.get("status") != "succeeded":
        raise RuntimeError("Replicate: " + str(d.get("error") or d.get("status")))
    o = d["output"]
    tai(o[0] if isinstance(o, list) else o, out)

def higgsfield(prompt, out, tl):
    tmp = out + ".prompt.txt"
    open(tmp, "w", encoding="utf-8").write(prompt)
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "higgsfield.py"), "anh", tmp, out, "--mau", "soul", "--ty-le", tl], check=True)
    os.remove(tmp)

NGUON = {"openai": ("OPENAI_API_KEY", openai), "gemini": ("GEMINI_API_KEY", gemini),
         "higgsfield": ("HIGGSFIELD_API_KEY", higgsfield), "replicate": ("REPLICATE_API_TOKEN", replicate)}

def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__); sys.exit(1)
    prompt, out = doc_prompt(a[0]), a[1]
    tl = a[a.index("--ty-le") + 1] if "--ty-le" in a else "9:16"
    ng = a[a.index("--nguon") + 1] if "--nguon" in a else os.environ.get("ANH_AI_NGUON", "")
    if not ng:
        ng = next((k for k, (env, _) in NGUON.items() if os.environ.get(env)), "")
    if ng not in NGUON:
        sys.exit("Chưa có công cụ ảnh AI: đặt một trong các biến OPENAI_API_KEY / GEMINI_API_KEY / HIGGSFIELD_API_KEY / REPLICATE_API_TOKEN "
                 "(hoặc dùng connector Higgsfield/Canva trong Claude).")
    env, fn = NGUON[ng]
    if not os.environ.get(env):
        sys.exit(f"Thiếu biến {env} cho nguồn {ng}.")
    fn(prompt, out, tl)
    print(f"Đã tạo {out} bằng {ng}")

if __name__ == "__main__":
    main()
