"""Dò mặt KHÁCH (áo nâu, đứng bên phải) trong video + ảnh bằng YuNet. Bác sĩ áo xanh (bên trái) không che.
Ra mat_video.npy (cx, cy, size theo từng khung 1080x1920) và mat_anh.json."""
import json, os, subprocess, sys
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SRC = "C:/MERAH/TƯ LIỆU MERAH ĐĂNG BÀI/9-11-2026/"
MD = r"C:\Users\Surface\Downloads\FINE\ADS 2.10.1\model\face_detection_yunet_2023mar.onnx"
W, H = 1080, 1920

def det(img, thr=0.5):
    h, w = img.shape[:2]
    y = cv2.FaceDetectorYN.create(MD, "", (w, h), thr, 0.3, 50)
    _, f = y.detect(img)
    return [] if f is None else [(x + bw / 2, yy + bh / 2, max(bw, bh), s) for x, yy, bw, bh, *_, s in f]

# ---- video
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC + "IMG_7897 (1).MOV", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
yn = cv2.FaceDetectorYN.create(MD, "", (W, H), 0.45, 0.3, 50)
raw = []
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    _, f = yn.detect(fr)
    fs = [] if f is None else [(x + bw / 2, yy + bh / 2, max(bw, bh)) for x, yy, bw, bh, *_ in f]
    raw.append(fs)
n = len(raw)
# khách = mặt bên phải (cx > 520) gần vị trí trước đó
track = np.full((n, 3), np.nan); prev = None
for i, fs in enumerate(raw):
    cand = [f for f in fs if f[0] > 480]
    if prev is not None:
        cand = [f for f in cand if abs(f[0] - prev[0]) < 220 and abs(f[1] - prev[1]) < 220] or []
    if cand:
        best = max(cand, key=lambda f: f[0]); track[i] = best; prev = best
miss = np.isnan(track[:, 0])
print("khung", n, "thiếu", int(miss.sum()))
idx = np.arange(n)
for k in range(3):
    track[:, k] = np.interp(idx, idx[~miss], track[~miss, k])
# làm mượt
ker = np.ones(5) / 5
sm = np.stack([np.convolve(np.pad(track[:, k], 2, mode="edge"), ker, "valid") for k in range(3)], 1)
np.save("mat_video.npy", sm)
# ---- ảnh
out = {}
for f in ["photo_6307525521813738300_w.jpg", "photo_6307525521813738303_w.jpg", "photo_6307525521813738304_w.jpg", "photo_6307525521813738299_w.jpg"]:
    img = cv2.imdecode(np.fromfile(SRC + f, np.uint8), cv2.IMREAD_COLOR)
    fs = det(img); fs = sorted(fs, key=lambda z: z[0])
    print(f, img.shape[:2], [(int(a), int(b), int(c), round(float(s), 2)) for a, b, c, s in fs])
    out[f] = [float(v) for v in fs[-1][:3]] if fs else None   # mặt bên phải nhất = khách
json.dump(out, open("mat_anh.json", "w"), indent=1)
