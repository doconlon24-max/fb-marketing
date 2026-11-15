"""Căn mặt vào giữa khung: dò mặt YuNet từng khung, làm mượt, crop+zoom, xuất 1080x1920.
python can_giua_mat.py vao.mp4|png ra.mp4|png [zoom_min] [y_mat=0.40]"""
import sys, subprocess, json, cv2, numpy as np
sys.path.insert(0, r"C:/MERAH/he-thong/tai-nguyen/scripts")
from duong_dan_may import tim
MD = tim("model/face_detection_yunet_2023mar.onnx")
W, H = 1080, 1920
src, dst = sys.argv[1], sys.argv[2]
zmin = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
ymat = float(sys.argv[4]) if len(sys.argv) > 4 else 0.40
CO_DINH = len(sys.argv) > 6 and sys.argv[6] == "co_dinh"
ZMAX = float(sys.argv[5]) if len(sys.argv) > 5 else 1.45
yn = cv2.FaceDetectorYN.create(MD, "", (W, H), 0.5, 0.3, 50)
def det(fr):
    _, f = yn.detect(fr)
    if f is None: return None
    x, y, bw, bh = max(f, key=lambda r: r[-1])[:4]
    return (x+bw/2, y+bh/2, bh)
def crop(fr, cx, cy, z):
    cw, ch = W/z, H/z
    x0 = min(max(cx-cw/2, 0), W-cw); y0 = min(max(cy-ch*ymat, 0), H-ch)
    M = np.float32([[z, 0, -x0*z], [0, z, -y0*z]])
    return cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LANCZOS4), (x0+cw/2)
def zoom_need(cx):  # zoom tối thiểu để mặt vào đúng giữa
    return max(zmin, W/(2*max(min(cx, W-cx), 1)))
if src.lower().endswith((".png", ".jpg")):
    fr = cv2.resize(cv2.imread(src), (W, H)); d = det(fr)
    out, c = crop(fr, d[0], d[1], zoom_need(d[0])); cv2.imwrite(dst, out)
    print(json.dumps({"mat_cx": float(d[0]), "zoom": float(zoom_need(d[0]))})); sys.exit()
fps = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src]).decode().strip()
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
frs, tr = [], []
while True:
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3); frs.append(fr); d = det(fr)
    tr.append(d if d else (np.nan,)*3)
tr = np.array(tr, float); n = len(tr); idx = np.arange(n)
for k in range(3):
    ok = ~np.isnan(tr[:, k]); tr[:, k] = np.interp(idx, idx[ok], tr[ok, k])
# tách shot theo khác biệt khung, mỗi shot làm mượt + zoom riêng
small = [cv2.resize(f, (54, 96)).astype(np.int16) for f in frs]
cuts = [0] + [i for i in range(1, n) if np.abs(small[i]-small[i-1]).mean() > 28] + [n]
k = max(3, int(eval(fps)) | 1); ker = np.ones(k)/k
sm = np.zeros_like(tr); zs = np.zeros(n)
for a, b in zip(cuts[:-1], cuts[1:]):
    seg = tr[a:b]; kk = min(k, (b-a) | 1); kr = np.ones(kk)/kk
    med = np.median(seg, 0); sm[a:b] = med  # trục dọc + cỡ mặt: cố định theo trung vị shot
    m = kk // 2  # trục ngang: lọc trung vị (bỏ khung dò nhầm) rồi trung bình trượt 2 lần
    x = np.array([np.median(seg[max(0, i-m):i+m+1, 0]) for i in range(b-a)])
    for _ in range(2): x = np.convolve(np.pad(x, m, mode="edge"), kr, "valid")
    sm[a:b, 0] = x
    if CO_DINH: sm[a:b] = np.median(tr[a:b], 0)  # khung cố định cả shot: không rung
    zs[a:b] = min(max(zoom_need(c) for c in sm[a:b, 0]), ZMAX)
print("shot:", cuts, "zoom:", sorted(set(np.round(zs, 3))))
q = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", fps, "-i", "-",
     "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
lech = []
for fr, (cx, cy, s), z in zip(frs, sm, zs):
    o, c = crop(fr, cx, cy, z); lech.append(abs((cx - (c - W/(2*z))) * z - W/2)); q.stdin.write(o.tobytes())
q.stdin.close(); q.wait()
print(json.dumps({"khung": n, "thieu_mat": int(np.isnan(np.array([1]))[0]), "cx_tb": round(float(np.mean(tr[:, 0]))), "lech_tam_max_px": round(max(lech))}))
