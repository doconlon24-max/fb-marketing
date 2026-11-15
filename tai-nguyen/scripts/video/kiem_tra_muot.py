"""Kiểm tra video có bị giật/lag (khung hình lặp) trước khi nộp – sếp yêu cầu 10/11/2026.
   python kiem_tra_muot.py <video.mp4> [--max 3]
Đọc từng khung (thu nhỏ), đếm chuỗi khung GIỐNG HỆT nhau liên tiếp.
- Chuỗi lặp ngắn rải rác giữa cảnh chuyển động = cảnh quay bị phát chậm -> GIẬT -> phải dựng lại (cảnh quay thật luôn chạy 1x).
- Khung đứng yên hoàn toàn > 0.5 s chỉ được phép ở thẻ chữ/ảnh tĩnh có chủ đích (logo cuối...).
Thoát mã 1 nếu "GIẬT" để nhân viên biết phải sửa."""
import subprocess, sys
import numpy as np

def main(path, max_lap=3):
    w, h = 216, 384  # đủ nét để thấy chuyển động của đồ hoạ mảnh (vòng, đường kẻ)
    fps_s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path],
                           capture_output=True, text=True).stdout.strip() or "30/1"
    a, b = fps_s.split("/"); fps = float(a) / float(b or 1)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16)
    if len(fr) < 2:
        sys.exit("Không đọc được khung")
    dd = np.abs(np.diff(fr, axis=0)).reshape(len(fr) - 1, -1)
    d = dd.mean(axis=1)
    # khung "trùng" = không có vùng nào thay đổi rõ (phân vị 99.5 của chênh lệch < 5): khung lặp thật chỉ còn nhiễu nén;
    # đồ hoạ mảnh đang chạy (vòng, chữ đếm) hay zoom chậm thì có vùng đổi mạnh -> không tính là lặp
    same = (dd > 12).mean(axis=1) < 0.0003
    runs, i = [], 0
    while i < len(same):
        if same[i]:
            j = i
            while j < len(same) and same[j]:
                j += 1
            runs.append((i, j - i + 1)); i = j
        else:
            i += 1
    # chuỗi lặp ngắn (2..15 khung) xen giữa chuyển động = dấu hiệu phát chậm
    giat = [(s, n) for s, n in runs if max_lap < n <= 15]
    tinh = [(s, n) for s, n in runs if n > 15]
    dup = int(same.sum())
    # NHẢY CẢNH (sếp 15/11, VD7): cảnh quay liền bị chắp nhiều đoạn ngắn/ảnh tĩnh -> tư thế nhảy giữa chừng.
    # = các điểm đổi khung đột ngột cỡ vừa (8..45; >45 là chuyển cảnh có chủ đích) gom theo cụm <0.3s; >=3 cụm trong 4s = nhảy.
    cu = [i for i in range(len(d)) if 8 < d[i] < 45]
    nhom = []
    for i in cu:
        if not nhom or i - nhom[-1] > fps * 0.3:
            nhom.append(i)
    nhay = []
    for k, i in enumerate(nhom):
        if sum(1 for j in nhom if i <= j < i + fps * 4) >= 3 and (not nhay or i / fps - nhay[-1] > 4):
            nhay.append(i / fps)
    print(f"{path}: {len(fr)} khung, {fps:.0f} fps, {len(fr) / fps:.1f} s; khung lặp {dup} ({dup / len(fr):.0%})")
    # đoạn giật = >=3 chuỗi lặp ngắn trong 1 giây
    bad = []
    for s, n in giat:
        cnt = sum(1 for s2, _ in giat if s <= s2 < s + fps)
        if cnt >= 3 and (not bad or s / fps - bad[-1] > 1):
            bad.append(s / fps)
    for s, n in tinh:
        print(f"  khung đứng yên {s / fps:.1f}s → {(s + n) / fps:.1f}s ({n / fps:.1f}s) – chỉ OK nếu là thẻ tĩnh có chủ đích")
    if nhay:
        print("  NHẢY CẢNH (nhiều đoạn ngắn/ảnh tĩnh chắp vào nhau trong cảnh liền) quanh các giây:", ", ".join(f"{t:.1f}" for t in nhay))
        print("KẾT LUẬN: NHẢY – phải dùng 1 đoạn video liền mạch cho cảnh đó (không xen ảnh tĩnh, không cắt ngắn <3s)"); return 1
    if bad:
        print("  GIẬT (cảnh bị phát chậm, khung lặp liên tục) quanh các giây:", ", ".join(f"{t:.1f}" for t in bad))
        print("KẾT LUẬN: GIẬT – phải dựng lại, cảnh quay thật chạy đúng tốc độ gốc"); return 1
    print("KẾT LUẬN: MƯỢT"); return 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    sys.exit(main(a[0], int(a[a.index("--max") + 1]) if "--max" in a else 3))
