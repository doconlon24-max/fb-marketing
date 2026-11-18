"""Cổng nhận file tạm từ Chrome (chỉ localhost) – dùng khi Chrome bật "Hỏi nơi lưu" làm kẹt lượt tải thứ 2 trở đi.
Chạy:  python tai-nguyen/scripts/nhan_file_tam.py [cổng=8799]
Trang web (đang mở trong Chrome) gửi:  fetch('http://localhost:8799/SPY_IG-xxx.mp4',{method:'POST',body:blob})
File lưu vào thư mục Downloads của người dùng. Chỉ nhận tên dạng SPY_*.mp4/jpg, tối đa 300MB. Tắt bằng Ctrl-C.
"""
import http.server, os, re, sys

DICH = os.path.join(os.path.expanduser("~"), "Downloads")
TEN_OK = re.compile(r"^SPY_[A-Za-z0-9_\-\.]{1,120}\.(mp4|jpg|png|m4a)$")


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        # trang nhận: trang khác (vd Instagram, bị CSP chặn gọi localhost) mở cửa sổ này rồi postMessage({ten, blob})
        html = (b"<!doctype html><meta charset=utf-8><title>nhan file</title><body>cho file...<script>"
                b"addEventListener('message',async e=>{const d=e.data||{};if(!d.ten||!d.blob)return;"
                b"const r=await fetch('/'+d.ten,{method:'POST',body:d.blob});const t=r.status+':'+await r.text();"
                b"document.body.textContent='da luu '+d.ten+' '+t;e.source&&e.source.postMessage({ten:d.ten,kq:t},'*')});"
                b"opener&&opener.postMessage({san_sang:1},'*');"
                # cach 2: http://localhost:8799/#ten=SPY_x.mp4&u=<link file> -> trang nay tu tai link roi luu
                b"(async()=>{const h=new URLSearchParams(location.hash.slice(1));const u=h.get('u'),ten=h.get('ten');if(!u||!ten)return;"
                b"try{const p=await fetch('/lay/'+ten,{method:'POST',body:u});"
                b"document.title='XONG '+p.status+':'+await p.text();}catch(e){document.title='LOI '+String(e).slice(0,80)}"
                b"history.replaceState(null,'','/')})()</script>")
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(html)

    def do_POST(self):
        ten = os.path.basename(self.path.split("?")[0])
        n = int(self.headers.get("Content-Length") or 0)
        if self.path.startswith("/lay/"):  # trang gửi link file (CDN mạng xã hội) -> máy tự tải
            u = self.rfile.read(min(n, 8000)).decode("utf-8", "ignore").strip()
            ok = TEN_OK.match(ten) and re.match(r"^https://[a-z0-9\.\-]+\.(cdninstagram\.com|fbcdn\.net|tiktokcdn\.com|tiktokcdn-us\.com)/", u)
            if not ok:
                self.send_response(400); self._cors(); self.end_headers(); return
            import urllib.request, shutil
            p = os.path.join(DICH, ten)
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.instagram.com/"})
            with urllib.request.urlopen(req, timeout=120) as r, open(p + ".part", "wb") as f:
                shutil.copyfileobj(r, f)
            os.replace(p + ".part", p)
            self.send_response(200); self._cors(); self.end_headers()
            self.wfile.write(str(os.path.getsize(p)).encode())
            print("da tai", ten, os.path.getsize(p), flush=True)
            return
        if not TEN_OK.match(ten) or n <= 0 or n > 300_000_000:
            self.send_response(400); self._cors(); self.end_headers(); return
        p = os.path.join(DICH, ten)
        with open(p + ".part", "wb") as f:
            con = n
            while con > 0:
                b = self.rfile.read(min(1 << 20, con))
                if not b:
                    break
                f.write(b); con -= len(b)
        os.replace(p + ".part", p)
        self.send_response(200); self._cors(); self.end_headers()
        self.wfile.write(str(os.path.getsize(p)).encode())
        print("da nhan", ten, os.path.getsize(p), flush=True)


if __name__ == "__main__":
    cong = int(sys.argv[1]) if len(sys.argv) > 1 else 8799
    print("nhan file tai", DICH, "cong", cong, flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", cong), H).serve_forever()
