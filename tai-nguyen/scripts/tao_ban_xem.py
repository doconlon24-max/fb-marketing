# -*- coding: utf-8 -*-
"""Tạo BẢN XEM NHẸ (<9,5 MB) cho video trên Drive để app QUẢN TRỊ MERAH phát được ngay trong app.
Kết nối Google Drive của app chỉ tải được file dưới 10 MB, nên video thành phẩm 20–30 MB không phát được.
Bản xem đặt ở Drive `TƯ LIỆU QUẢNG CÁO/PHONG CÁCH VIDEO/_xem/<ID video gốc>_xem.mp4` – app tự tìm theo tên này.

Chạy (máy sếp hoặc đám mây, cần rclone remote `merah:` + ffmpeg):
  python tai-nguyen/scripts/tao_ban_xem.py <id hoặc link Drive> [<id> ...]
  python tai-nguyen/scripts/tao_ban_xem.py --tu-file ds.txt     (mỗi dòng 1 id/link)
Video đã có bản xem thì bỏ qua (thêm --lam-lai để làm lại). In JSON từng video.
"""
import json, os, re, subprocess, sys, tempfile

GIOI_HAN = 9.3e6  # byte


def run(cmd, t=900):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=t, encoding="utf-8", errors="replace")


def goc_xem():
    r = run(["rclone", "lsf", "merah:", "--dirs-only", "--max-depth", "1"], 60)
    base = "merah:TƯ LIỆU QUẢNG CÁO" if any(n.strip("/") == "TƯ LIỆU QUẢNG CÁO" for n in r.stdout.splitlines()) else "merah:MERAH/TƯ LIỆU QUẢNG CÁO"
    return base + "/PHONG CÁCH VIDEO/_xem"


def ids_tu(args):
    out = []
    for a in args:
        m = re.search(r"(?:/d/|[?&]id=)([\w-]{20,})", a) or re.fullmatch(r"([\w-]{20,})", a.strip())
        if m:
            out.append(m.group(1))
    return list(dict.fromkeys(out))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    a = sys.argv[1:]
    lam_lai = "--lam-lai" in a
    a = [x for x in a if x != "--lam-lai"]
    if "--tu-file" in a:
        i = a.index("--tu-file"); a = a[:i] + open(a[i + 1], encoding="utf-8").read().split() + a[i + 2:]
    if os.path.isdir(os.path.expanduser("~/bin")):
        os.environ["PATH"] = os.path.expanduser("~/bin") + os.pathsep + os.environ.get("PATH", "")
    dich = goc_xem()
    co_san = set(run(["rclone", "lsf", dich], 120).stdout.split())
    for vid in ids_tu(a):
        ten = vid + "_xem.mp4"
        if ten in co_san and not lam_lai:
            print(json.dumps({"id": vid, "ok": True, "bo_qua": "đã có bản xem"}, ensure_ascii=False)); continue
        tmp = tempfile.mkdtemp(prefix="xem_")
        try:
            r = run(["rclone", "backend", "copyid", "merah:", vid, tmp + os.sep])
            fs = [os.path.join(tmp, f) for f in os.listdir(tmp)]
            if not fs:
                print(json.dumps({"id": vid, "ok": False, "loi": "không tải được từ Drive (file đã xoá hoặc không có quyền)"}, ensure_ascii=False)); continue
            src = fs[0]
            if os.path.getsize(src) <= GIOI_HAN:  # vốn đã nhẹ: dùng luôn
                out = src
            else:
                d = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], 60).stdout.strip()
                dur = max(1.0, float(d or 30))
                vbr = int(min(1400, max(250, (GIOI_HAN * 8 / dur) / 1000 - 70)))  # kbps, chừa 64k cho tiếng
                out = os.path.join(tmp, "xem.mp4")
                run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale='min(540,iw)':-2", "-c:v", "libx264", "-preset", "veryfast",
                     "-b:v", f"{vbr}k", "-maxrate", f"{vbr}k", "-bufsize", f"{vbr * 2}k", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", out])
                if not os.path.exists(out) or os.path.getsize(out) > 9.9e6:
                    print(json.dumps({"id": vid, "ok": False, "loi": "nén chưa xuống dưới 10 MB"}, ensure_ascii=False)); continue
            r = run(["rclone", "copyto", out, f"{dich}/{ten}"])
            print(json.dumps({"id": vid, "ok": r.returncode == 0, "mb": round(os.path.getsize(out) / 1e6, 1), "ten": ten, **({"loi": r.stderr[-200:]} if r.returncode else {})}, ensure_ascii=False))
        finally:
            for f in os.listdir(tmp):
                try: os.remove(os.path.join(tmp, f))
                except OSError: pass
            try: os.rmdir(tmp)
            except OSError: pass


if __name__ == "__main__":
    main()
