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
    print(f"{path}: {len(fr)} khung, {fps:.0f} fps, {len(fr) / fps:.1f} s; khung lặp {dup} ({dup / len(fr):.0%})")
    # đoạn giật = >=3 chuỗi lặp ngắn trong 1 giây
    bad = []
    for s, n in giat:
        cnt = sum(1 for s2, _ in giat if s <= s2 < s + fps)
        if cnt >= 3 and (not bad or s / fps - bad[-1] > 1):
            bad.append(s / fps)
    for s, n in tinh:
        print(f"  khung đứng yên {s / fps:.1f}s → {(s + n) / fps:.1f}s ({n / fps:.1f}s) – chỉ OK nếu là thẻ tĩnh có chủ đích")
    if bad:
        print("  GIẬT (cảnh bị phát chậm, khung lặp liên tục) quanh các giây:", ", ".join(f"{t:.1f}" for t in bad))
        print("KẾT LUẬN: GIẬT – phải dựng lại, cảnh quay thật chạy đúng tốc độ gốc"); return 1
    print("KẾT LUẬN: MƯỢT"); return 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    sys.exit(main(a[0], int(a[a.index("--max") + 1]) if "--max" in a else 3))
