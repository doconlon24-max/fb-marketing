"""Video spa 5.11: nâng lên 1080x1920, làm mịn da mặt KHÁCH NAM (bên trái), dò mặt KHÁCH NỮ (bên phải) để che.
Ra: NGUON_<tên>.mp4 (đã mịn da, giữ tiếng gốc) + mat_<tên>.npz (khung mặt nữ theo từng khung hình).
Chạy từ thư mục KHÔNG dấu (MediaPipe lỗi với đường dẫn có dấu):  python xu_ly_mat.py IMG_5515 [--xem 1,5,9]"""
import os, subprocess, sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = r"C:\Users\Surface\Downloads\CLAUDE DỰNG VIDEO\video thô đăng spa 5.11"
MD = r"C:\Users\Surface\Downloads\FINE\ADS 2.10.1\model"
W, H = 1080, 1920
ten = sys.argv[1]
XEM = [float(x) for x in sys.argv[sys.argv.index("--xem") + 1].split(",")] if "--xem" in sys.argv else None

EYE_L = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
EYE_R = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
BROW_L = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
BROW_R = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149,
        150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

yunet = cv2.FaceDetectorYN.create(os.path.join(MD, "face_detection_yunet_2023mar.onnx"), "", (W, H), 0.55, 0.3, 50)
lmk = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=os.path.join(MD, "face_landmarker.task")),
    running_mode=vision.RunningMode.IMAGE, num_faces=1, min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))


def ghi_anh(path, img):
    ok, buf = cv2.imencode(".jpg", img)
    open(path, "wb").write(buf.tobytes())


def diem_mat_nam(fr, box):
    x, y, w, h = box
    cx, cy, s = x + w / 2, y + h / 2, max(w, h) * 1.9
    x0, y0 = int(max(cx - s / 2, 0)), int(max(cy - s / 2, 0))
    x1, y1 = int(min(cx + s / 2, W)), int(min(cy + s / 2, H))
    crop = fr[y0:y1, x0:x1]
    if crop.size == 0:
        return None
    k = 480 / max(crop.shape[:2])
    big = cv2.resize(crop, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
    r = lmk.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(big, cv2.COLOR_BGR2RGB)))
    if not r.face_landmarks:
        return None
    bh, bw = big.shape[:2]
    return np.array([[q.x * bw / k + x0, q.y * bh / k + y0] for q in r.face_landmarks[0]], np.float32)


def lam_min(fr, lm, box):
    m = np.zeros(fr.shape[:2], np.uint8)
    if lm is not None:
        p = lm.astype(np.int32)
        cv2.fillPoly(m, [p[OVAL]], 255)
        for g in (EYE_L, EYE_R, BROW_L, BROW_R, LIPS):
            cv2.fillPoly(m, [cv2.convexHull(p[g])], 0)
    else:   # không có điểm mặt: làm mịn nhẹ cả khung mặt
        x, y, w, h = [int(v) for v in box]
        cv2.ellipse(m, (x + w // 2, y + h // 2), (w // 2, int(h * 0.55)), 0, 0, 360, 160, -1)
    m = cv2.GaussianBlur(m, (21, 21), 0).astype(np.float32)[..., None] / 255 * 0.8
    sm = cv2.bilateralFilter(fr, 9, 45, 7)
    sm = cv2.convertScaleAbs(sm, alpha=1.04, beta=6)
    return (fr * (1 - m) + sm * m).astype(np.uint8)


def main():
    src = os.path.join(RAW, ten + ".MOV")
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    out = os.path.join(HERE, f"NGUON_{ten}.mp4")
    tmp = os.path.join(os.getcwd(), f"_tmp_{ten}.mp4")
    pr = None if XEM else subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    nu, i, xem, n_nam = [], 0, [], 0
    sharpen = np.array([[0, -0.25, 0], [-0.25, 2, -0.25], [0, -0.25, 0]], np.float32)
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        fr = cv2.filter2D(cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4), -1, sharpen)
        _, fc = yunet.detect(fr)
        fc = [] if fc is None else [f[:4] for f in fc]
        trai = [f for f in fc if f[0] + f[2] / 2 < W * 0.52]
        phai = [f for f in fc if f[0] + f[2] / 2 >= W * 0.52]
        f_nu = max(phai, key=lambda f: f[2] * f[3]) if phai else None
        f_nam = max(trai, key=lambda f: f[2] * f[3]) if trai else None
        nu.append(None if f_nu is None else [f_nu[0] + f_nu[2] / 2, f_nu[1] + f_nu[3] / 2, max(f_nu[2], f_nu[3])])
        if f_nam is not None:
            lm = diem_mat_nam(fr, f_nam)
            n_nam += lm is not None
            fr = lam_min(fr, lm, f_nam)
        if XEM and any(abs(i / fps - t) < 0.5 / fps for t in XEM):
            v = fr.copy()
            for f, c in ((f_nu, (0, 0, 255)), (f_nam, (0, 255, 0))):
                if f is not None:
                    cv2.rectangle(v, (int(f[0]), int(f[1])), (int(f[0] + f[2]), int(f[1] + f[3])), c, 4)
            xem.append(cv2.resize(v, (360, 640)))
        if pr:
            pr.stdin.write(fr.tobytes())
        i += 1
    thieu = sum(v is None for v in nu)
    if XEM:
        ghi_anh(os.path.join(HERE, f"_xem_mat_{ten}.jpg"), np.hstack(xem))
        print(f"{i} khung · thiếu mặt nữ {thieu} · có điểm mặt nam {n_nam}")
        return
    pr.stdin.close()
    pr.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
    os.remove(tmp)
    idx = [k for k, v in enumerate(nu) if v is not None]
    arr = np.zeros((len(nu), 3), np.float32)
    for k in range(len(nu)):
        if nu[k] is not None:
            arr[k] = nu[k]
            continue
        a = max([j for j in idx if j < k], default=None)
        b = min([j for j in idx if j > k], default=None)
        if a is None and b is None:
            arr[k] = [W * 0.72, H * 0.33, 200]
        elif a is None or b is None:
            arr[k] = nu[a if b is None else b]
        else:
            u = (k - a) / (b - a)
            arr[k] = np.array(nu[a]) * (1 - u) + np.array(nu[b]) * u
    sm = arr.copy()
    for c in range(3):
        sm[:, c] = np.convolve(np.pad(arr[:, c], 3, mode="edge"), np.ones(7) / 7, mode="valid")
    sm[:, 2] = np.maximum(sm[:, 2], arr[:, 2])   # không thu nhỏ hơn mặt thật
    np.savez(os.path.join(HERE, f"mat_{ten}.npz"), nu=sm, thieu=np.array([v is None for v in nu]), fps=fps)
    print(f"ok {out} · {i} khung · thiếu mặt nữ {thieu} (đã nội suy) · điểm mặt nam {n_nam}")


main()
