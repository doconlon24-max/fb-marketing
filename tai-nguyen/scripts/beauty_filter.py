"""Filter làm đẹp da nhẹ (không dùng AI tạo ảnh) – chỉ dùng cho ảnh nhân viên / khoảnh khắc,
KHÔNG dùng cho ảnh before/after hay ảnh kết quả điều trị.

python beauty_filter.py <in.jpg> <out.jpg> [--strength 0.55] [--compare compare.jpg]
  strength: 0.35 nhẹ · 0.55 vừa · 0.75 mạnh
"""
import argparse
import cv2
import numpy as np


def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path = getattr(getattr(cv2, "data", None), "haarcascades", "") + "haarcascade_frontalface_default.xml"
    casc = cv2.CascadeClassifier(path)
    if casc.empty():
        # OpenCV 5 không còn kèm file haarcascade: làm mịn theo màu da trên toàn ảnh
        h, w = img.shape[:2]
        return [("all", 0, w, h)]
    h = img.shape[0]
    faces = casc.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=6, minSize=(h // 20, h // 20))
    return [tuple(map(int, f)) for f in faces]


def skin_mask(img, faces):
    h, w = img.shape[:2]
    region = np.zeros((h, w), np.uint8)
    for (x, y, fw, fh) in faces:
        if x == "all":
            region[:] = 255
            continue
        cx, cy = x + fw // 2, y + int(fh * 0.55)
        cv2.ellipse(region, (cx, cy), (int(fw * 0.62), int(fh * 0.78)), 0, 0, 360, 255, -1)
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin = cv2.inRange(ycc, (40, 133, 77), (255, 178, 133))
    m = cv2.bitwise_and(skin, region)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    k = max(9, (h // 120) | 1)
    return cv2.GaussianBlur(m, (k * 2 + 1, k * 2 + 1), 0).astype(np.float32) / 255.0


def beautify(img, strength=0.55, faces=None):
    faces = faces or detect_faces(img)
    if not faces:
        return img, faces, None
    mask = skin_mask(img, faces)
    # làm mịn giữ cạnh, mạnh dần theo strength
    sm = img
    for _ in range(2):
        sm = cv2.bilateralFilter(sm, d=0, sigmaColor=28 + 30 * strength, sigmaSpace=6 + 8 * strength)
    # trả lại vân da li ti để không bị "mặt nhựa"
    fine = img.astype(np.float32) - cv2.GaussianBlur(img, (0, 0), 1.0).astype(np.float32)
    sm = np.clip(sm.astype(np.float32) + fine * (0.55 - 0.25 * strength), 0, 255)
    a = (mask * strength)[..., None]
    out = img.astype(np.float32) * (1 - a) + sm * a
    # sáng & đều màu nhẹ trên vùng da
    lab = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 0] += mask * (4 * strength)
    lab[..., 1] -= mask * (0.8 * strength)   # bớt đỏ rất nhẹ, giữ sắc hồng
    lab[..., 2] += mask * (1.0 * strength)   # giữ độ ấm của da
    out = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return out, faces, mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--strength", type=float, default=0.55)
    ap.add_argument("--compare")
    ap.add_argument("--face", nargs=4, type=int, action="append", help="x y w h (tự chỉ định khung mặt)")
    a = ap.parse_args()
    img = cv2.imdecode(np.fromfile(a.src, np.uint8), cv2.IMREAD_COLOR)
    out, faces, mask = beautify(img, a.strength, [tuple(f) for f in a.face] if a.face else None)
    print("faces:", faces)
    cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 95])[1].tofile(a.out)
    if a.compare and faces:
        crops = []
        for (x, y, fw, fh) in faces:
            if x == "all":
                x, y = 0, 0
            p = int(fw * 0.35)
            y0, y1, x0, x1 = max(0, y - p), y + fh + p, max(0, x - p), x + fw + p
            b, c = img[y0:y1, x0:x1], out[y0:y1, x0:x1]
            s = 520 / b.shape[0]
            b, c = cv2.resize(b, None, fx=s, fy=s), cv2.resize(c, None, fx=s, fy=s)
            for im_, t in ((b, "TRUOC"), (c, "SAU")):
                cv2.putText(im_, t, (14, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)
            crops.append(np.hstack([b, np.full((520, 8, 3), 255, np.uint8), c]))
        wmax = max(cimg.shape[1] for cimg in crops)
        crops = [np.hstack([cimg, np.full((520, wmax - cimg.shape[1], 3), 255, np.uint8)]) for cimg in crops]
        sheet = np.vstack([np.vstack([cimg, np.full((8, wmax, 3), 255, np.uint8)]) for cimg in crops])
        cv2.imencode(".jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 92])[1].tofile(a.compare)


if __name__ == "__main__":
    main()
