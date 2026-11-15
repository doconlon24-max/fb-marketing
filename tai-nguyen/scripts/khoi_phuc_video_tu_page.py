"""KHÔI PHỤC video thành phẩm QC bị mất trên Drive bằng chính bài đã đăng trên page (video của MERAH) – không tốn token.
  python khoi_phuc_video_tu_page.py            # tự tìm: dòng QUANG-CAO 'Đã đăng page' có link F không tải được (404)
  python khoi_phuc_video_tu_page.py --thu      # chỉ in dòng hỏng
Tải video gốc từ bài (Graph API, token page) → THÀNH PHẨM QUẢNG CÁO/<dd-mm-yyyy>/<yyyy-mm-dd>_<VDx>.mp4 → sửa cột F, ghi K → tạo bản xem.
(15/11/2026: 3 video 10/11–13/11 bị xoá hẳn khỏi Drive, khôi phục bằng cách này.)
"""
import json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import requests  # noqa: E402
import fb_api as F, sheet_api as S  # noqa: E402  (fb_api tự đặt PATH/cấu hình rclone)


def rc(*a, t=600):
    return subprocess.run(["rclone", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t)


def con_tren_drive(fid):
    r = rc("backend", "copyid", "merah:", fid, os.path.join(tempfile.gettempdir(), "kp_chk") + os.sep, "--dry-run", t=120)
    return r.returncode == 0 and "notFound" not in (r.stderr or "")


def main():
    thu = "--thu" in sys.argv
    P = json.load(open(F.PAGES, encoding="utf-8"))
    rows = S.get("QUANG-CAO!A1:N")
    for i, r in enumerate(rows[1:], 2):
        r = (r + [""] * 14)[:14]
        ma, ngay_b, page, st, k, post = r[0], r[1], r[7], r[8], r[10], r[11].strip()
        m = re.search(r"/d/([\w-]{20,})", r[5])
        if not (ma.startswith("QC-") and st == "Đã đăng page" and post and m) or con_tren_drive(m.group(1)):
            continue
        print(ma, "mất file Drive", m.group(1))
        if thu:
            continue
        pid, p = F.load_pages(page.strip())[0]
        att = ((requests.get(f"{F.G}/{pid}_{post.split('_')[-1]}", params={"fields": "attachments{target}", "access_token": p["token"]}, timeout=60).json()
                .get("attachments") or {}).get("data") or [{}])[0]
        vid = (att.get("target") or {}).get("id")
        src = requests.get(f"{F.G}/{vid}", params={"fields": "source", "access_token": p["token"]}, timeout=60).json().get("source") if vid else None
        if not src:
            print(" -> không lấy được video từ bài"); continue
        d, mo, y = (ngay_b.split("/") + ["", "", ""])[:3]
        ten = f"{y}-{mo.zfill(2)}-{d.zfill(2)}_{ma.split('-')[-1]}.mp4"
        f = os.path.join(tempfile.mkdtemp(prefix="kp_"), ten)
        with requests.get(src, stream=True, timeout=300) as g, open(f, "wb") as o:
            for ch in g.iter_content(1 << 20):
                o.write(ch)
        thu_muc = f"merah:THÀNH PHẨM QUẢNG CÁO/{d.zfill(2)}-{mo.zfill(2)}-{y}"
        if rc("copyto", f, f"{thu_muc}/{ten}").returncode != 0:
            print(" -> rclone lỗi"); continue
        fid = rc("lsf", thu_muc, "--format", "pi", "--separator", "|", "--include", ten).stdout.strip().split("|")[-1]
        S.goi([{"op": "set", "range": f"QUANG-CAO!F{i}", "values": [[f"https://drive.google.com/file/d/{fid}/view"]]},
               {"op": "set", "range": f"QUANG-CAO!K{i}", "values": [[k.rstrip() + " | file Drive cũ bị mất – máy khôi phục từ bài đã đăng trên page"]]}])
        subprocess.run([sys.executable, os.path.join(HERE, "tao_ban_xem.py"), fid])
        print(" -> ok", fid)


if __name__ == "__main__":
    main()
