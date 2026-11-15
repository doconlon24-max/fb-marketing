# Xoá chữ Hàn (trên) + nhãn BEFORE/AFTER xanh (giữa dưới) bằng cv2.inpaint từng khung -> clean.mp4 (không tiếng)
import cv2, numpy as np, subprocess, sys
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(5)
m = np.zeros((1920, 1080), np.uint8)
m[215:385, 255:825] = 255      # chữ Hàn
m[1370:1495, 385:695] = 255    # nhãn BEFORE/AFTER
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if f.shape[:2] != (1920, 1080): f = cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    p.stdin.write(cv2.inpaint(f, m, 9, cv2.INPAINT_TELEA).tobytes()); n += 1
p.stdin.close(); p.wait(); print("khung", n, "fps", fps)
