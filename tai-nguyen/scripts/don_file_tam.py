# -*- coding: utf-8 -*-
"""Dọn file sửa/nháp/tạm trên máy theo quy tắc "chỉ giữ bản cuối" (sếp chốt 15/11/2026).
Chạy: python tai-nguyen/scripts/don_file_tam.py          (xoá thật)
      python tai-nguyen/scripts/don_file_tam.py --thu    (chỉ liệt kê, không xoá)
XOÁ: file KHÔNG nằm trong git (untracked/ignored) ở bai-cho-duyet/ và quang-cao/test-video/ đã cũ hơn 2 ngày
     (cảnh cắt, video nền, nhạc tạm, log, .npy, ảnh soi khung, bản thử _v1.._vN trừ bản _v số lớn nhất);
     bản sao lưu app merah-studio/src.bak-*.html, chỉ giữ 3 bản mới nhất.
GIỮ: bản cuối đã đăng (video.mp4, video_xmas.mp4, anh_0x.png, ANHx.jpg, anh_bia.jpg, story.jpg), script .py/.html,
     mọi file đang trong git, mọi file mới sửa trong 2 ngày (có thể là việc đang dở).
Không đụng tới Google Drive (Drive: bản cũ vào Thùng rác ngay khi có bản mới – xem quy tắc trong tac-vu/nhan-vien-truc.md).
"""
import os, re, subprocess, sys, time

GOC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
THU = "--thu" in sys.argv
GIU_TEN = re.compile(r"(^|/)(video|video_xmas|anh_\d+|ANH\d+|anh_bia|story)\.(mp4|png|jpe?g)$", re.I)


def git_others():
    out = set()
    for extra in ([], ["--ignored", "--exclude-standard"]):
        r = subprocess.run(["git", "-C", GOC, "ls-files", "--others", *extra, "--", "bai-cho-duyet", "quang-cao/test-video"],
                           capture_output=True, text=True, encoding="utf-8")
        out |= {l.strip() for l in r.stdout.splitlines() if l.strip()}
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    han = time.time() - 2 * 86400
    ung = []
    files = sorted(git_others())
    # bản thử _vN: giữ số lớn nhất của mỗi nhóm
    nhom = {}
    for p in files:
        m = re.match(r"(.*)_v(\d+)(\.[a-z0-9]+)$", p, re.I)
        if m:
            nhom.setdefault((m.group(1), m.group(3).lower()), []).append((int(m.group(2)), p))
    giu_v = {max(v)[1] for v in nhom.values()}
    for p in files:
        f = os.path.join(GOC, p)
        if not os.path.isfile(f) or os.path.getmtime(f) > han:
            continue
        if p.endswith((".py", ".html")) or GIU_TEN.search(p) or p in giu_v:
            continue
        ung.append(f)
    baks = sorted([os.path.join(GOC, "merah-studio", x) for x in os.listdir(os.path.join(GOC, "merah-studio")) if x.startswith("src.bak-")],
                  key=os.path.getmtime, reverse=True)
    ung += baks[3:]
    tong = sum(os.path.getsize(f) for f in ung)
    for f in ung:
        if not THU:
            try: os.remove(f)
            except OSError: pass
    if not THU:
        for root, dirs, fs in os.walk(os.path.join(GOC, "bai-cho-duyet"), topdown=False):
            if root != os.path.join(GOC, "bai-cho-duyet") and not os.listdir(root):
                try: os.rmdir(root)
                except OSError: pass
    print(("Sẽ xoá" if THU else "Đã xoá") + f" {len(ung)} file, {tong/1e6:.1f} MB")


if __name__ == "__main__":
    main()
