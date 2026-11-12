"""Tải 1 video SPY về và đẩy vào Drive: TƯ LIỆU QUẢNG CÁO/SPY/<dd-mm-yyyy>/ (tự tạo thư mục ngày nếu chưa có).

Dùng được cả trên máy sếp lẫn đám mây (cần rclone remote `merah:`).
  python spy_tai_ve.py --key FB-123 --who "ten doi thu" --url "<link>" [--date dd-mm-yyyy] [--khong-day]
  python spy_tai_ve.py --key FB-123 --who "ten doi thu" --tu-downloads [--cho 40]
      (video đã được Chrome tải về thư mục Downloads với tên SPY_<key>.mp4 – cách dùng trên máy sếp)

--url: link file video trực tiếp (vd link fbcdn lấy từ thẻ <video> khi mở bài trong Chrome, hoặc link Manifold trả về),
       hoặc link bài TikTok (khi đó dùng yt-dlp – chỉ chạy được trên máy có mạng tới tiktok.com).
Không đổi User-Agent, không dùng cookie/proxy; bị chặn thì báo lỗi và dừng.
In ra 1 dòng JSON: {"ok":true,"file":...,"drive":...,"giay":...} hoặc {"ok":false,"loi":...}
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")


def spy_base():
    """Trên máy sếp remote trỏ thẳng vào thư mục MERAH; trên đám mây trỏ vào gốc Drive."""
    r = run(["rclone", "lsf", "merah:", "--dirs-only", "--max-depth", "1"], 60)
    names = r.stdout.splitlines()
    if any(n.strip("/") == "TƯ LIỆU QUẢNG CÁO" for n in names):
        return "merah:TƯ LIỆU QUẢNG CÁO/SPY"
    return "merah:MERAH/TƯ LIỆU QUẢNG CÁO/SPY"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--who", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--tu-downloads", action="store_true")
    ap.add_argument("--cho", type=int, default=40)
    ap.add_argument("--date", default="")
    ap.add_argument("--khong-day", action="store_true")
    a = ap.parse_args()

    if os.path.isdir(os.path.expanduser("~/bin")):
        os.environ["PATH"] = os.path.expanduser("~/bin") + os.pathsep + os.environ.get("PATH", "")
    ngay = a.date or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%d-%m-%Y")
    ten = re.sub(r"[^\w.-]+", "_", f"SPY_{a.key}_{a.who}".strip("_"), flags=re.UNICODE)[:90] + ".mp4"
    xoa_sau = ""
    tmp = tempfile.mkdtemp(prefix="spy_")
    dich = os.path.join(tmp, ten)
    try:
        host = urllib.parse.urlparse(a.url).netloc.lower()
        if a.tu_downloads:
            import glob, time
            dl = os.path.join(os.path.expanduser("~"), "Downloads")
            nguon, het = "", time.time() + a.cho
            while time.time() < het and not nguon:
                c = [f for f in glob.glob(os.path.join(dl, f"SPY_{a.key}*.mp4")) if time.time() - os.path.getmtime(f) < 900]
                if c:
                    nguon = max(c, key=os.path.getmtime)
                else:
                    # Chrome đang hỏi nơi lưu: tệp đã tải đủ nằm ở dạng .tmp trong Downloads
                    t = [f for f in glob.glob(os.path.join(dl, "*.tmp")) if time.time() - os.path.getmtime(f) < 180 and os.path.getsize(f) > 50_000]
                    if t and time.time() > het - a.cho / 2:
                        nguon = max(t, key=os.path.getmtime)
                    else:
                        time.sleep(2)
            if not nguon:
                return print(json.dumps({"ok": False, "loi": "không thấy tệp SPY_%s*.mp4 trong Downloads (Chrome chưa tải xong hoặc đang hỏi nơi lưu)" % a.key}, ensure_ascii=False))
            shutil.copyfile(nguon, dich)
            xoa_sau = nguon  # sếp chốt 12/11/2026: đẩy lên Drive xong là xoá bản trên máy
        elif "tiktok.com" in host and "/video/" in a.url:
            r = run([sys.executable, "-m", "yt_dlp", "--no-playlist", "-o", dich, a.url], 300)
            if r.returncode != 0:
                return print(json.dumps({"ok": False, "loi": (r.stderr or r.stdout).strip().splitlines()[-1][:300]}, ensure_ascii=False))
        else:
            r = run(["curl", "-L", "-sS", "-m", "240", "-o", dich, "-w", "%{http_code}", a.url], 260)
            if r.returncode != 0 or not r.stdout.strip().startswith("2"):
                return print(json.dumps({"ok": False, "loi": f"curl {r.returncode} http {r.stdout.strip()} {r.stderr.strip()[:200]}"}, ensure_ascii=False))
        if not os.path.exists(dich) or os.path.getsize(dich) < 50_000:
            return print(json.dumps({"ok": False, "loi": "tệp tải về quá nhỏ hoặc không có"}, ensure_ascii=False))
        p = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration", "-of", "csv=p=0", dich], 60)
        try:
            giay = round(float(p.stdout.strip().splitlines()[0]), 1)
        except Exception:
            return print(json.dumps({"ok": False, "loi": "tệp tải về không phải video (có thể là bài ảnh)"}, ensure_ascii=False))
        drive = f"{spy_base()}/{ngay}/{ten}"
        if not a.khong_day:
            r = run(["rclone", "copyto", dich, drive], 600)
            if r.returncode != 0:
                return print(json.dumps({"ok": False, "loi": "rclone: " + r.stderr.strip()[-300:]}, ensure_ascii=False))
        da_xoa = True
        if xoa_sau and not a.khong_day:
            try: os.remove(xoa_sau)
            except OSError: da_xoa = False  # Chrome còn giữ tệp (đang hỏi nơi lưu) – sẽ tự mất khi đóng hộp thoại
        print(json.dumps({"ok": True, "file": ten, "drive": drive, "ngay": ngay, "giay": giay, "mb": round(os.path.getsize(dich) / 1e6, 1), "da_xoa_tren_may": da_xoa}, ensure_ascii=False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
