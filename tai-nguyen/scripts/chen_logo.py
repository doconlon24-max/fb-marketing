"""Chèn LOGO THẬT MERAH lên ảnh AI (ChatGPT/Higgsfield hay vẽ sai logo) + đưa về đúng cỡ đăng page.
  python chen_logo.py <anh_vao> <anh_ra> [--ti-le 3:4|4:5|9:16|1:1] [--logo nau|kem|vang] [--vi-tri tren|duoi]
Mặc định: 3:4 (1080x1440), logo MR nâu, giữa phía trên. Nền tối → --logo kem hoặc vang.
"""
import argparse, os
from PIL import Image

KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = {"nau": "LOGO_MR_nau_tach_nen.png", "kem": "LOGO_MR_nho_kem_trong_suot.png", "vang": "LOGO_MR_vang_nau_trong_suot.png"}
CO = {"3:4": (1080, 1440), "4:5": (1080, 1350), "9:16": (1080, 1920), "1:1": (1080, 1080)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vao"); ap.add_argument("ra")
    ap.add_argument("--ti-le", default="3:4", choices=list(CO))
    ap.add_argument("--logo", default="nau", choices=list(LOGO))
    ap.add_argument("--vi-tri", default="tren", choices=["tren", "duoi"])
    a = ap.parse_args()
    W, H = CO[a.ti_le]
    im = Image.open(a.vao).convert("RGB")
    # cắt giữa đúng tỉ lệ rồi thu về cỡ chuẩn (không méo)
    r = W / H
    if im.width / im.height > r:
        w = int(im.height * r); im = im.crop(((im.width - w) // 2, 0, (im.width - w) // 2 + w, im.height))
    else:
        h = int(im.width / r); im = im.crop((0, (im.height - h) // 2, im.width, (im.height - h) // 2 + h))
    im = im.resize((W, H), Image.LANCZOS)
    lg = Image.open(os.path.join(KHO, "thuong-hieu", "logo", LOGO[a.logo])).convert("RGBA")
    lw = int(W * 0.17)
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    y = int(H * 0.025) if a.vi_tri == "tren" else H - lg.height - int(H * 0.03)
    im.paste(lg, ((W - lw) // 2, y), lg)
    im.save(a.ra, quality=95)
    print(a.ra, W, H)


if __name__ == "__main__":
    main()
