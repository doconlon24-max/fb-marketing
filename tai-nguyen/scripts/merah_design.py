"""MERAH BEAUTY – thiết kế ảnh feed 4:5 kiểu "Merah Diary" từ ảnh thô (không dùng AI).

Cách dùng:
  python merah_design.py <anh_tho> <file_ra.png> [--logo logo.png]
Tham số bố cục (vùng cắt, vị trí che mặt, chữ) chỉnh trong CONFIG bên dưới.
"""
import argparse
import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

F = r"C:\Windows\Fonts"
FONT_SERIF = rf"{F}\BOD_R.TTF"       # Bodoni – tiêu đề
FONT_ITALIC = rf"{F}\GARAIT.TTF"     # Garamond nghiêng – chữ nhấn
FONT_SANS = rf"{F}\GIL_____.TTF"     # Gill Sans – chữ nhỏ
FONT_EMOJI = rf"{F}\seguiemj.ttf"

BROWN = (74, 46, 34)
GOLD = (176, 132, 72)
CREAM = (246, 238, 228)

CONFIG = {
    "crop": (0, 300, 720, 1200),           # x0, y0, x1, y1 trên ảnh gốc (tỉ lệ 4:5)
    "faces": [((122, 768), 185)],          # (tâm mặt trên ảnh gốc, cỡ sticker) – che mặt khách
    "kicker": "MERAH DIARY  ·  EARLY CHRISTMAS",
    "title1": "A Sweet Surprise",
    "title2": "for Our Lovely Client",
    "footer_left": "MERAH BEAUTY – Makati City",
    "footer_right": "{{SO_DIEN_THOAI}}",
}

W, H = 1080, 1350


def font(path, size):
    return ImageFont.truetype(path, size)


def spaced(draw, xy, text, fnt, fill, spacing, anchor_center=True):
    """Vẽ chữ giãn khoảng cách, căn giữa theo x."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += w + spacing
    return total


def warm_grade(im):
    im = ImageEnhance.Brightness(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Color(im).enhance(1.08)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.05 + 4)))
    g = g.point(lambda v: min(255, int(v * 1.01 + 1)))
    b = b.point(lambda v: int(v * 0.92))
    return Image.merge("RGB", (r, g, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--logo", help="PNG logo nền trong suốt (nếu có)")
    a = ap.parse_args()
    c = CONFIG

    src = Image.open(a.src).convert("RGB")
    x0, y0, x1, y1 = c["crop"]
    sc = W / (x1 - x0)
    im = src.crop(c["crop"]).resize((W, H), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im = warm_grade(im)

    # Lớp sáng kem phía trên để chữ dễ đọc
    fade = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fade)
    for y in range(640):
        t = y / 640
        fd.line([(0, y), (W, y)], fill=int(225 * (1 - t ** 2.2)))
    im = Image.composite(Image.new("RGB", (W, H), CREAM), im, fade)

    d = ImageDraw.Draw(im)

    # Che mặt khách bằng sticker tim hồng (giống cách page đang làm)
    emo = None
    for (fx, fy), size in c["faces"]:
        emo = emo or font(FONT_EMOJI, 109)
        st = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(st).text((80, 80), "💗", font=emo, embedded_color=True, anchor="mm")
        s = int(size * sc)
        st = st.resize((s, s), Image.LANCZOS)
        cx, cy = (fx - x0) * sc, (fy - y0) * sc
        im.paste(st, (int(cx - s / 2), int(cy - s / 2)), st)

    # Logo / wordmark
    if a.logo:
        lg = Image.open(a.logo).convert("RGBA")
        lg.thumbnail((260, 150))
        im.paste(lg, ((W - lg.width) // 2, 48), lg)
        ty = 48 + lg.height + 26
    else:
        d.text((W / 2, 80), "MR", font=font(FONT_SERIF, 92), fill=BROWN, anchor="mm")
        spaced(d, (W / 2, 128), "MERAH BEAUTY", font(FONT_SANS, 24), BROWN, 7)
        ty = 182

    # Kicker + tiêu đề
    d.line([(W / 2 - 60, ty), (W / 2 + 60, ty)], fill=GOLD, width=2)
    spaced(d, (W / 2, ty + 20), c["kicker"], font(FONT_SANS, 22), GOLD, 4)
    d.text((W / 2, ty + 112), c["title1"], font=font(FONT_SERIF, 84), fill=BROWN, anchor="mm")
    d.text((W / 2, ty + 192), c["title2"], font=font(FONT_ITALIC, 62), fill=GOLD, anchor="mm")
    hy = ty + 250
    d.line([(W / 2 - 110, hy), (W / 2 - 22, hy)], fill=GOLD, width=2)
    d.line([(W / 2 + 22, hy), (W / 2 + 110, hy)], fill=GOLD, width=2)
    d.polygon([(W / 2, hy - 9), (W / 2 + 9, hy), (W / 2, hy + 9), (W / 2 - 9, hy)], fill=GOLD)

    # Hạt lấp lánh nhẹ kiểu tuyết – chỉ ở vùng trên, không rơi lên người
    rnd = random.Random(7)
    sp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    for _ in range(40):
        x, y, r = rnd.randint(0, W), rnd.randint(30, 560), rnd.choice([2, 2, 3])
        sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 240, rnd.randint(120, 220)))
    sp = sp.filter(ImageFilter.GaussianBlur(0.8))
    im.paste(sp, (0, 0), sp)

    # Footer nâu
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 96, W, H], fill=BROWN)
    d.line([(0, H - 96), (W, H - 96)], fill=GOLD, width=3)
    fs = font(FONT_SANS, 28)
    d.text((60, H - 48), c["footer_left"], font=fs, fill=CREAM, anchor="lm")
    d.text((W - 60, H - 48), c["footer_right"], font=fs, fill=CREAM, anchor="rm")

    # Viền vàng mảnh
    d.rectangle([22, 22, W - 23, H - 119], outline=(*GOLD,), width=2)

    im.save(a.out, optimize=True)
    print("saved", a.out)


if __name__ == "__main__":
    main()
