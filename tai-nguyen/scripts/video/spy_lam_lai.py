"""Làm sạch video SPY (sưu tầm, đã xin phép) trước khi dựng lại thành video MERAH – sếp chốt 10/11/2026.
Bỏ HẾT giọng/âm thanh gốc, xoá chữ/logo/watermark gốc, rồi mới dựng lại bằng chữ + giọng + nhạc + SFX của MERAH.

1) Xem khung có lưới toạ độ để tìm chữ cần xoá (nhân viên edit mở ảnh ra xem):
   python spy_lam_lai.py khung <video> <thu_muc_ra> [--moi 1.0]
      -> khung_luoi.jpg (các khung 1 giây/lần, lưới 100 px theo khung 1080x1920 sau chuẩn hoá)
2) Xoá chữ + bỏ tiếng:
   python spy_lam_lai.py xoa <video> <ra.mp4> --vung "x,y,w,h[,t0,t1]" [--vung ...] [--kieu inpaint|mo|cat]
      x,y,w,h theo khung 1080x1920 (đã chuẩn hoá dọc 9:16); t0,t1 = giây xuất hiện (bỏ trống = cả video).
      inpaint: vá nền (hợp chữ nhỏ/phụ đề trên nền đơn giản) · mo: làm mờ mạnh (nền phức tạp) ·
      cat: chỉ chuẩn hoá + bỏ tiếng (khi định cắt khung để loại vùng chữ).
      Video ra KHÔNG có âm thanh, 1080x1920, 30 fps.
3) Lời thoại gốc (để hiểu ý, viết lại kịch bản MERAH bằng lời mới – KHÔNG chép nguyên văn):
   python ../giong_doc.py nghe <video> <loi_goc.txt>   (ElevenLabs Speech-to-Text)
Sau đó: viết kịch bản tiếng Anh mới cho MERAH -> giong_doc.py doc (giọng Mely) -> dựng theo phong cách trong album
(chữ MERAH mới, nhạc + SFX bằng sfx.py, outro khách thật MERAH, before/after nơi khác ghi "Sample result · Results may vary")."""
import os, subprocess, sys, tempfile
try:
    import cv2
except ImportError:  # đám mây chưa cài được opencv -> dùng ffmpeg
    cv2 = None
import numpy as np

W, H, FPS = 1080, 1920, 30


def chuan_hoa(src, dst, keep_audio=False):
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf, *([] if keep_audio else ["-an"]), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", dst], check=True)


def khung(src, outdir, moi=1.0):
    os.makedirs(outdir, exist_ok=True)
    if cv2 is None:  # không opencv: ffmpeg xuất khung có lưới
        tmp = os.path.join(outdir, "_chuan.mp4"); chuan_hoa(src, tmp)
        grid = r"drawgrid=w=100:h=100:t=2:c=yellow@0.8,drawtext=text='%{pts\:hms}':x=w-tw-30:y=30:fontsize=70:fontcolor=red"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-vf", f"fps=1/{moi},{grid},scale=360:640,tile=6x8", "-frames:v", "1", os.path.join(outdir, "khung_luoi.jpg")], check=True)
        os.remove(tmp); print(os.path.join(outdir, "khung_luoi.jpg"), "(ffmpeg)"); return
    tmp = os.path.join(outdir, "_chuan.mp4"); chuan_hoa(src, tmp)
    cap = cv2.VideoCapture(tmp); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); step = max(1, int(FPS * moi)); thumbs = []
    for i in range(0, n, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
        if not ok:
            break
        for x in range(0, W, 100):
            cv2.line(f, (x, 0), (x, H), (0, 255, 255), 1); cv2.putText(f, str(x), (x + 3, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        for y in range(0, H, 100):
            cv2.line(f, (0, y), (W, y), (0, 255, 255), 1); cv2.putText(f, str(y), (3, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.putText(f, f"{i / FPS:.1f}s", (W - 260, 90), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 0, 255), 6)
        thumbs.append(cv2.resize(f, (360, 640)))
    cols = 6; rows = (len(thumbs) + cols - 1) // cols
    sheet = np.full((rows * 640, cols * 360, 3), 255, np.uint8)
    for k, t in enumerate(thumbs):
        sheet[(k // cols) * 640:(k // cols + 1) * 640, (k % cols) * 360:(k % cols + 1) * 360] = t
    cv2.imwrite(os.path.join(outdir, "khung_luoi.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
    cap.release(); os.remove(tmp); print(os.path.join(outdir, "khung_luoi.jpg"), f"{len(thumbs)} khung")


def xoa_ffmpeg(tmp, dst, vung, kieu):
    """Không cần opencv: delogo (vá nền) hoặc boxblur (làm mờ) từng vùng theo thời gian."""
    fs = []
    for v in vung:
        x, y, w, h = [int(a) for a in v[:4]]; t0, t1 = (v[4], v[5]) if len(v) >= 6 else (0, 99999)
        x = max(1, min(x, W - 3)); y = max(1, min(y, H - 3)); w = max(2, min(w, W - x - 1)); h = max(2, min(h, H - y - 1))
        en = f":enable='between(t,{t0},{t1})'"
        fs.append(f"delogo=x={x}:y={y}:w={w}:h={h}{en}" if kieu != "mo" else None)
        if kieu == "mo":
            fs[-1] = None
    if kieu == "mo":
        parts = ["[0:v]split=" + str(len(vung) + 1) + "".join(f"[s{i}]" for i in range(len(vung) + 1))]; last = "s0"
        for i, v in enumerate(vung, 1):
            x, y, w, h = [int(a) for a in v[:4]]; t0, t1 = (v[4], v[5]) if len(v) >= 6 else (0, 99999)
            parts.append(f"[s{i}]crop={w}:{h}:{x}:{y},boxblur=20:3[b{i}]")
            parts.append(f"[{last}][b{i}]overlay={x}:{y}:enable='between(t,{t0},{t1})'[o{i}]"); last = f"o{i}"
        args = ["-filter_complex", ";".join(parts), "-map", f"[{last}]"]
    else:
        args = ["-vf", ",".join(f for f in fs if f)]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, *args, "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", dst], check=True)
    print("Xong (ffmpeg, không opencv):", dst)


def xoa(src, dst, vung, kieu="inpaint"):
    tmpd = tempfile.mkdtemp(); tmp = os.path.join(tmpd, "chuan.mp4"); chuan_hoa(src, tmp)
    if cv2 is None and vung and kieu != "cat":
        return xoa_ffmpeg(tmp, dst, vung, kieu)
    if kieu == "cat" or not vung:
        os.replace(tmp, dst); print("Xong (chỉ chuẩn hoá + bỏ tiếng):", dst); return
    cap = cv2.VideoCapture(tmp)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        t = i / FPS; mask = np.zeros((H, W), np.uint8)
        for v in vung:
            x, y, w, h = v[:4]; t0, t1 = (v[4], v[5]) if len(v) >= 6 else (0, 1e9)
            if t0 <= t <= t1:
                pad = 6; mask[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad] = 255
        if mask.any():
            if kieu == "mo":
                bl = cv2.GaussianBlur(f, (0, 0), 25); f = np.where(mask[..., None] > 0, bl, f)
            else:
                small = cv2.resize(f, (W // 2, H // 2)); m2 = cv2.resize(mask, (W // 2, H // 2), interpolation=cv2.INTER_NEAREST)
                fix = cv2.resize(cv2.inpaint(small, m2, 7, cv2.INPAINT_TELEA), (W, H))
                soft = cv2.GaussianBlur(mask, (0, 0), 3)[..., None] / 255.0
                f = (fix * soft + f * (1 - soft)).astype(np.uint8)
        p.stdin.write(f.tobytes()); i += 1
    p.stdin.close(); p.wait(); cap.release(); print("Xong:", dst, f"{i} khung, không còn âm thanh gốc")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "khung":
        khung(a[1], a[2], float(a[a.index("--moi") + 1]) if "--moi" in a else 1.0)
    elif a[0] == "xoa":
        vs = [list(map(float, a[i + 1].split(","))) for i, x in enumerate(a) if x == "--vung"]
        vs = [[int(v[0]), int(v[1]), int(v[2]), int(v[3])] + v[4:] for v in vs]
        xoa(a[1], a[2], vs, a[a.index("--kieu") + 1] if "--kieu" in a else "inpaint")
