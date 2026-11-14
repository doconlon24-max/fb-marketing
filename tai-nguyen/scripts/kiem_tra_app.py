# -*- coding: utf-8 -*-
"""Kiểm tra app QUẢN TRỊ MERAH + bản chia sẻ SPA MARKETING (phần chạy được trên máy, không cần mạng).
Chạy: python tai-nguyen/scripts/kiem_tra_app.py   -> in JSON {ok, loi:[...], canh_bao:[...]}
Phần kiểm tra dữ liệu Sheet + mở app thật làm theo tac-vu/kiem-tra-app-hang-ngay.md.
"""
import io, json, os, re, subprocess, sys, tempfile
GOC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
loi, canh = [], []
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def js_ok(html, ten):
    js = "\n".join(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, flags=re.S))
    t = os.path.join(tempfile.gettempdir(), "kt_" + ten + ".mjs")
    io.open(t, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", t], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        loi.append(f"{ten}: lỗi cú pháp JS – " + (r.stderr or "").strip().splitlines()[0][:200] if r.stderr else ten + ": lỗi JS")
    # khai báo trùng tên (lỗi hay gặp khi vá thêm hàm)
    ten_ham = re.findall(r"^(?:const|let|function|async function)\s+([A-Za-z_$][\w$]*)", js, flags=re.M)
    trung = sorted({x for x in ten_ham if ten_ham.count(x) > 1})
    if trung:
        loi.append(f"{ten}: khai báo trùng tên {trung}")

src = io.open(os.path.join(GOC, "merah-studio/src.html"), encoding="utf-8").read()
idx = io.open(os.path.join(GOC, "merah-studio/index.html"), encoding="utf-8").read()
js_ok(src, "src")
if "__LOGO_LIGHT__" in idx:
    loi.append("index.html còn __LOGO_LIGHT__ – chưa dựng lại từ src.html")
# index phải khớp src (trừ logo)
if re.sub(r'const LOGO_LIGHT="[^"]*", LOGO_DARK="[^"]*";', "", idx) != re.sub(r'const LOGO_LIGHT="[^"]*", LOGO_DARK="[^"]*";', "", src):
    canh.append("index.html khác src.html (ngoài logo) – cần dựng lại index rồi đăng")
# bản chia sẻ dựng được
out = os.path.join(tempfile.gettempdir(), "kt_appchung")
os.makedirs(out, exist_ok=True)
r = subprocess.run([sys.executable, os.path.join(GOC, "tai-nguyen/scripts/lam_app_chung.py"), os.path.join(GOC, "merah-studio"), out, os.path.join(out, "chk.js")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
if r.returncode:
    loi.append("Bản chia sẻ không dựng được: " + (r.stderr or r.stdout).strip().splitlines()[-1][:200])
else:
    js_ok(io.open(os.path.join(out, "src.html"), encoding="utf-8").read(), "chung")
    m = re.search(r"ID con sot: (\[.*\])", r.stdout)
    if m and m.group(1) != "[]":
        canh.append("Bản chia sẻ còn sót ID riêng của MERAH: " + m.group(1))
    a = io.open(os.path.join(GOC, "app-facebook-marketing/src.html"), encoding="utf-8").read()
    if a != io.open(os.path.join(out, "src.html"), encoding="utf-8").read():
        canh.append("app-facebook-marketing chưa cập nhật theo bản MERAH mới nhất – dựng lại rồi đăng SPA MARKETING")
print(json.dumps({"ok": not loi, "loi": loi, "canh_bao": canh}, ensure_ascii=False, indent=1))
