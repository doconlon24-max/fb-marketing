# Dựng ảnh Giáng sinh 9-11 (bài 0700 + carousel 1100 + 2 story). Ảnh thật: chỉ sáng ấm nhẹ, không làm mịn, không AI.
import sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
sys.path.insert(0, r"C:\Users\Surface\Downloads\CLAUDE DỰNG VIDEO\ADS SPA 5.11")
import trang_tri as T

SRC = r"C:\MERAH\TƯ LIỆU MERAH ĐĂNG BÀI\9-11-2026\photo_{{ID_FACEBOOK}}"
BASE = r"C:\Users\Surface\Downloads\CLAUDE HỌC\SUB AGENT"
OUT = BASE + r"\bai-cho-duyet"
LOGO = BASE + r"\tai-nguyen\mau-thiet-ke\logo_dark.png"
F = "C:/Windows/Fonts/"
CREAM = (246, 238, 226); BROWN = (78, 44, 30); RED = (166, 22, 34); GOLD = (196, 160, 98); GOLD_D = (150, 104, 58)
W = 1080

def font(n, s): return ImageFont.truetype(F + n, s)

# vị trí mặt KHÁCH (áo nâu) trên ảnh gốc 1920x2560: tâm, cỡ tim
FACE = {"299": (1150, 1255, 400), "303": (1038, 1235, 450), "304": (922, 1140, 520)}


def warm(im):
    im = ImageEnhance.Brightness(im).enhance(1.07)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.035 + 2)))
    b = b.point(lambda v: int(v * 0.955))
    return Image.merge("RGB", (r, g, b))


def heart(sz):
    S = 4; n = sz * S
    m = Image.new("L", (n, n), 0); d = ImageDraw.Draw(m)
    pts = []
    for i in range(400):
        t = 2 * math.pi * i / 400
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((n / 2 + x * n / 36, n * 0.45 - y * n / 36))
    d.polygon(pts, fill=255)
    m = m.resize((sz, sz), Image.LANCZOS)
    # viền trắng
    edge = m.filter(ImageFilter.MaxFilter(max(3, (sz // 40) | 1)))
    out = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    out.paste((255, 255, 255, 255), (0, 0), edge)
    # thân hồng có gradient + bóng sáng
    body = Image.new("RGBA", (sz, sz))
    bd = ImageDraw.Draw(body)
    for y in range(sz):
        k = y / sz
        bd.line([(0, y), (sz, y)], fill=(int(250 - 20 * k), int(150 - 55 * k), int(185 - 45 * k), 255))
    inner = m.filter(ImageFilter.MinFilter(max(3, (sz // 40) | 1)))
    out.paste(body, (0, 0), inner)
    hl = Image.new("L", (sz, sz), 0)
    ImageDraw.Draw(hl).ellipse((sz * 0.2, sz * 0.14, sz * 0.42, sz * 0.3), fill=120)
    hl = ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(sz / 30)), inner)
    out.paste((255, 255, 255, 255), (0, 0), hl)
    sh = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); sh.putalpha(edge.filter(ImageFilter.GaussianBlur(sz / 25)).point(lambda v: v * 0.35))
    res = Image.new("RGBA", (sz + 20, sz + 20), (0, 0, 0, 0))
    res.alpha_composite(sh, (12, 16)); res.alpha_composite(out, (6, 6))
    return res


def photo(n):
    im = warm(Image.open(SRC + n + "_w.jpg").convert("RGB")).convert("RGBA")
    cx, cy, s = FACE[n]
    h = heart(s)
    im.alpha_composite(h, (int(cx - h.width / 2), int(cy - h.height * 0.40)))
    return im.convert("RGB")


def card(img, box, w, h):
    """ảnh trong khung vàng bo góc + viền trắng + bóng"""
    im = img.crop(box).resize((w, h), Image.LANCZOS)
    r = 34
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    pad = 14
    c = Image.new("RGBA", (w + 2 * pad + 40, h + 2 * pad + 40), (0, 0, 0, 0))
    sh = Image.new("L", c.size, 0); ImageDraw.Draw(sh).rounded_rectangle((20, 30, 20 + w + 2 * pad, 30 + h + 2 * pad), r + pad, fill=90)
    c.paste((90, 50, 20, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((20, 20, 20 + w + 2 * pad, 20 + h + 2 * pad), r + pad, fill=(255, 251, 244), outline=GOLD, width=4)
    d.rounded_rectangle((20 + pad - 5, 20 + pad - 5, 20 + pad + w + 4, 20 + pad + h + 4), r + 4, outline=GOLD, width=2)
    c.paste(im, (20 + pad, 20 + pad), m)
    return c  # offset ảnh trong c: (20+pad)


def background(H):
    bg = Image.new("RGB", (W, H), CREAM)
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((-W * 0.3, -H * 0.1, W * 1.3, H * 0.75), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(220))
    bg = Image.composite(Image.new("RGB", (W, H), (252, 247, 238)), bg, g).convert("RGBA")
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((26, 26, W - 27, H - 27), 30, outline=GOLD, width=2)
    return bg


def sparkle(d, x, y, r, c=GOLD):
    k = r * 0.22
    d.polygon([(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)], fill=c)


def snow(cv, H, area, seed):
    rnd = random.Random(seed)
    lay = Image.new("RGBA", cv.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(70):
        x = rnd.uniform(40, W - 40); y = rnd.uniform(*area)
        r = rnd.uniform(1.5, 4.5)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, rnd.randint(150, 230)))
    cv.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))


def bow(cv, cx, cy, s=1.0):
    S = 3; w, h = int(120 * s), int(70 * s)
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cxs, cys = w * S / 2, h * S * 0.42
    L = w * S * 0.46; Hh = h * S * 0.38
    d.polygon([(cxs, cys), (cxs - L, cys - Hh), (cxs - L * 0.9, cys + Hh * 0.9)], fill=RED)
    d.polygon([(cxs, cys), (cxs + L, cys - Hh), (cxs + L * 0.9, cys + Hh * 0.9)], fill=RED)
    d.polygon([(cxs, cys), (cxs - L * 0.55, cys - Hh * 0.55), (cxs - L * 0.5, cys + Hh * 0.45)], fill=(205, 45, 55))
    d.polygon([(cxs, cys), (cxs + L * 0.55, cys - Hh * 0.55), (cxs + L * 0.5, cys + Hh * 0.45)], fill=(205, 45, 55))
    d.polygon([(cxs - 8 * S, cys), (cxs - L * 0.35, h * S), (cxs - L * 0.18, h * S * 0.95)], fill=(140, 15, 26))
    d.polygon([(cxs + 8 * S, cys), (cxs + L * 0.35, h * S), (cxs + L * 0.18, h * S * 0.95)], fill=(140, 15, 26))
    d.ellipse((cxs - 11 * S * s, cys - 11 * S * s, cxs + 11 * S * s, cys + 11 * S * s), fill=(185, 28, 40))
    im = im.resize((w, h), Image.LANCZOS)
    cv.alpha_composite(im, (int(cx - w / 2), int(cy - h * 0.42)))
    d2 = ImageDraw.Draw(cv)
    d2.line([(cx - 250, cy), (cx - 75 * s, cy)], fill=GOLD, width=2)
    d2.line([(cx + 75 * s, cy), (cx + 250, cy)], fill=GOLD, width=2)


def text_mixed(d, cx, y, t, fn, fb, fill):
    """căn giữa, ký tự ₱ dùng font dự phòng"""
    parts = []
    for ch in t:
        f = fb if ch == "₱" else fn
        if parts and parts[-1][1] is f: parts[-1][0] += ch
        else: parts.append([ch, f])
    tw = sum(d.textlength(s, font=f) for s, f in parts)
    x = cx - tw / 2
    for s, f in parts:
        d.text((x, y), s, font=f, fill=fill, anchor="ls"); x += d.textlength(s, font=f)


def spaced(d, cx, y, t, fn, fill, sp):
    ws = [d.textlength(c, font=fn) for c in t]; x = cx - (sum(ws) + sp * (len(t) - 1)) / 2
    for c, w in zip(t, ws): d.text((x, y), c, font=fn, fill=fill, anchor="ls"); x += w + sp


def fit(d, t, name, size, maxw):
    while d.textlength(t, font=font(name, size)) > maxw: size -= 2
    return font(name, size)


def phone_icon(d, x, y, s, c):
    d.rounded_rectangle((x, y, x + s * 0.62, y + s), s * 0.12, outline=c, width=2)
    d.line([(x + s * 0.22, y + s * 0.86), (x + s * 0.40, y + s * 0.86)], fill=c, width=2)


def garland(cv, dy):
    lay = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); T.lop_day_thong(lay, 0.3)
    cv.alpha_composite(lay.crop((0, -dy, W, 420)) if dy < 0 else lay, (0, max(0, dy)))


def corner_deco(cv, H):
    """cành thông + châu ở 2 góc dưới (cắt từ dây thông)"""
    lay = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); T.lop_day_thong(lay, 1.1)
    piece = lay.crop((0, 0, 360, 260))
    L = piece.rotate(28, Image.BICUBIC, expand=True)
    R = piece.transpose(Image.FLIP_LEFT_RIGHT).rotate(-28, Image.BICUBIC, expand=True)
    cv.alpha_composite(L.crop((0, 0, L.width, L.height)), (-110, H - L.height + 40))
    cv.alpha_composite(R, (W - R.width + 110, H - R.height + 40))


def build(H, pid, crop, card_wh, card_y, l1, l2, sub, foot, foot2=None, seed=1):
    cv = background(H)
    snow(cv, H, (180, card_y), seed)
    garland(cv, -55)
    lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((210, 100), Image.LANCZOS)
    ly = 128 if H < 1500 else 190
    cv.alpha_composite(lg, ((W - lg.width) // 2, ly))
    d = ImageDraw.Draw(cv)
    y = ly + lg.height + 34
    spaced(d, W / 2, y, "INTERNATIONAL AESTHETIC CLINIC", font("GIL_____.TTF", 17), GOLD_D, 6)
    big = 1.0 if H < 1500 else 1.12
    f1 = fit(d, l1, "BOD_BI.TTF", int(84 * big), 900)
    f2 = fit(d, l2, "BOD_B.TTF", int(70 * big), 920)
    y += int(96 * big)
    d.text((W / 2, y), l1, font=f1, fill=RED, anchor="ms")
    y += int(82 * big)
    d.text((W / 2, y), l2, font=f2, fill=BROWN, anchor="ms")
    y += int(48 * big)
    bow(cv, W / 2, y, 0.8 * big)
    d = ImageDraw.Draw(cv)
    y += int(62 * big)
    text_mixed(d, W / 2, y, sub, font("BOD_I.TTF", int(38 * big)), font("segoeuii.ttf", int(34 * big)), GOLD_D)
    sparkle(d, 120, y - 14, 13); sparkle(d, W - 120, y - 14, 13)
    # ảnh
    img = photo(pid)
    cw, ch = card_wh
    c = card(img, crop, cw, ch)
    cv.alpha_composite(c, ((W - c.width) // 2 + 10, card_y - 20))
    # băng đỏ cuối
    by = card_y + ch + 2 * 14 + 22
    bh = H - by
    d = ImageDraw.Draw(cv)
    band = Image.new("RGBA", (W, bh), RED + (255,))
    bd = ImageDraw.Draw(band)
    for i in range(bh):
        k = i / max(1, bh)
        bd.line([(0, i), (W, i)], fill=(int(176 - 40 * k), int(26 - 10 * k), int(38 - 10 * k), 255))
    bd.line([(0, 3), (W, 3)], fill=GOLD, width=3)
    cv.alpha_composite(band, (0, by))
    d = ImageDraw.Draw(cv)
    lines = [foot] + ([foot2] if foot2 else [])
    gap = 40
    ty = by + bh / 2 - (len(lines) - 1) * gap / 2 + 9
    for i, t in enumerate(lines):
        fn = font("GILI____.TTF", 27) if i == 0 else font("GIL_____.TTF", 26)
        if "+63" in t:
            tw = d.textlength(t, font=fn)
            phone_icon(d, W / 2 - tw / 2 - 30, ty - 24, 26, CREAM)
            d.text((W / 2 + 10, ty), t, font=fn, fill=CREAM, anchor="ms")
        else:
            d.text((W / 2, ty), t, font=fn, fill=CREAM, anchor="ms")
        ty += gap
    return cv.convert("RGB")


def crop_for(pid, ratio, x0, x1, y0):
    w = x1 - x0; h = int(w / ratio)
    if y0 + h > 2560: y0 = 2560 - h
    return (x0, y0, x1, y0 + h)



REV = r"C:\MERAH\TƯ LIỆU MERAH ĐĂNG BÀI\9-11-2026\photo_"
# vùng làm mờ trên ảnh gốc 960x1280: avatar (tâm, bán kính) + họ (trừ chữ cái đầu)
REVBLUR = {"{{ID_FACEBOOK}}": ((241, 305, 27), (407, 285, 472, 319)),
           "{{ID_FACEBOOK}}": ((243, 330, 27), (351, 317, 410, 347))}


def review_photo(n):
    im = warm(Image.open(REV + n + "_y.jpg").convert("RGB"))
    (cx, cy, r), box = REVBLUR[n]
    for b in [(cx - r, cy - r, cx + r, cy + r), box]:
        reg = im.crop(b).filter(ImageFilter.GaussianBlur(9)).filter(ImageFilter.GaussianBlur(9))
        m = Image.new("L", reg.size, 0); dm = ImageDraw.Draw(m)
        if b[2] - b[0] == 2 * r: dm.ellipse((0, 0, reg.width - 1, reg.height - 1), fill=255)
        else: dm.rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), 6, fill=255)
        im.paste(reg, b[:2], m)
    return im


def build_review(H, n, crop, ch, l1, sub, foot, foot2=None, seed=1):
    cv = background(H)
    garland(cv, -55)
    lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((190, 90), Image.LANCZOS)
    ly = 120 if H < 1500 else 190
    cv.alpha_composite(lg, ((W - lg.width) // 2, ly))
    d = ImageDraw.Draw(cv)
    y = ly + lg.height + 30
    spaced(d, W / 2, y, "INTERNATIONAL AESTHETIC CLINIC", font("GIL_____.TTF", 16), GOLD_D, 6)
    big = 1.0 if H < 1500 else 1.12
    y += int(92 * big)
    d.text((W / 2, y), l1, font=fit(d, l1, "BOD_BI.TTF", int(80 * big), 900), fill=RED, anchor="ms")
    y += int(42 * big)
    bow(cv, W / 2, y, 0.75 * big)
    d = ImageDraw.Draw(cv)
    y += int(56 * big)
    d.text((W / 2, y), sub, font=font("BOD_I.TTF", int(38 * big)), fill=GOLD_D, anchor="ms")
    card_y = y + 34
    snow(cv, H, (180, H - 120), seed)
    img = review_photo(n)
    cw = int(ch * (crop[2] - crop[0]) / (crop[3] - crop[1]))
    c = card(img, crop, cw, ch)
    cv.alpha_composite(c, ((W - c.width) // 2 + 10, card_y - 20))
    d = ImageDraw.Draw(cv)
    # sao vàng hai bên thẻ
    mid = card_y + ch / 2
    for sx in ((W - cw) / 2 - 70, (W + cw) / 2 + 70):
        sparkle(d, sx, mid - 60, 16); sparkle(d, sx + (18 if sx < W / 2 else -18), mid + 10, 9)
    by = card_y + ch + 2 * 14 + 22
    bh = H - by
    band = Image.new("RGBA", (W, bh), RED + (255,)); bd = ImageDraw.Draw(band)
    for i in range(bh):
        k = i / max(1, bh); bd.line([(0, i), (W, i)], fill=(int(176 - 40 * k), int(26 - 10 * k), int(38 - 10 * k), 255))
    bd.line([(0, 3), (W, 3)], fill=GOLD, width=3)
    cv.alpha_composite(band, (0, by))
    d = ImageDraw.Draw(cv)
    lines = [foot] + ([foot2] if foot2 else [])
    ty = by + bh / 2 - (len(lines) - 1) * 20 + 9
    for i, t in enumerate(lines):
        fn = font("GILI____.TTF", 27) if i == 0 else font("GIL_____.TTF", 26)
        if "+63" in t:
            tw = d.textlength(t, font=fn); phone_icon(d, W / 2 - tw / 2 - 30, ty - 24, 26, CREAM)
            d.text((W / 2 + 10, ty), t, font=fn, fill=CREAM, anchor="ms")
        else:
            d.text((W / 2, ty), t, font=fn, fill=CREAM, anchor="ms")
        ty += 40
    return cv.convert("RGB")


def reviews_0700():
    A, B = "{{ID_FACEBOOK}}", "{{ID_FACEBOOK}}"
    cA, cB = (40, 90, 920, 1270), (60, 70, 940, 1250)
    o = OUT + "/20261109-0700/"
    build_review(1350, A, cA, 800, "+1 More Love", "from our customers", "MERAH BEAUTY  ·  Makati City", None, 11).save(o + "20261109-0700_anh_01.jpg", quality=93, subsampling=0)
    build_review(1350, B, cB, 800, "5-Star Google Reviews", "Thank you for trusting MERAH", "Message us to book  ·  {{SO_DIEN_THOAI}}", None, 12).save(o + "20261109-0700_anh_02.jpg", quality=93, subsampling=0)
    build_review(1920, A, cA, 1180, "+1 More Love", "from our customers", "Thank you for trusting MERAH", "MERAH BEAUTY · Makati City · {{SO_DIEN_THOAI}}", 13).save(o + "story.jpg", quality=93, subsampling=0)
    print("ok reviews")


if __name__ == "__main__":
    jobs = []
    # ---- 0700: ảnh đơn 4:5 + story
    feed_wh, story_wh = (880, 610), (900, 1000)
    sub07 = "40% off until Nov 30 · Gifts up to ₱10,000"
    f07 = "Selected treatments. Message us to see what you qualify for."
    if False: jobs.append(("20261109-0700/20261109-0700_anh_01.jpg", 1350, "304", crop_for("304", 880 / 610, 0, 1920, 760), feed_wh, 610,
                 "Christmas Gifts", "AWAIT AT MERAH", sub07, f07, None, 3))
    if False: jobs.append(("20261109-0700/story.jpg", 1920, "304", crop_for("304", 900 / 1000, 160, 1920, 640), story_wh, 760,
                 "Christmas Gifts", "AWAIT AT MERAH", sub07, f07, "MERAH BEAUTY · Makati City · {{SO_DIEN_THOAI}}", 4))
    # ---- 1100: carousel 2 slide + story
    jobs.append(("20261109-1100/20261109-1100_anh_01.jpg", 1350, "299", crop_for("299", 880 / 610, 0, 1920, 700), feed_wh, 610,
                 "Congrats to Today's", "LUCKY WINNER!", "Christmas Lucky Draw at MERAH", "MERAH BEAUTY · Makati City", None, 5))
    jobs.append(("20261109-1100/20261109-1100_anh_02.jpg", 1350, "303", crop_for("303", 880 / 610, 0, 1920, 760), feed_wh, 610,
                 "1 Wallet + 1 Lipstick!", "COULD YOU BE NEXT?", "Christmas Lucky Draw at MERAH", "Message us to book  ·  {{SO_DIEN_THOAI}}", None, 6))
    jobs.append(("20261109-1100/story.jpg", 1920, "299", crop_for("299", 900 / 1000, 0, 1760, 640), story_wh, 760,
                 "Congrats to Today's", "LUCKY WINNER!", "Christmas Lucky Draw at MERAH", "Could you be next? Message us to book",
                 "MERAH BEAUTY · Makati City · {{SO_DIEN_THOAI}}", 7))
    if sys.argv[1:] == ["reviews"]: reviews_0700(); sys.exit()
    only = sys.argv[1:]
    for out, H, pid, crop, wh, cy, l1, l2, sub, foot, foot2, sd in jobs:
        if only and not any(o in out for o in only): continue
        im = build(H, pid, crop, wh, cy, l1, l2, sub, foot, foot2, sd)
        im.save(OUT + "/" + out, quality=93, subsampling=0); print("ok", out, crop)
