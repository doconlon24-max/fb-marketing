"""Đồ hoạ Giáng sinh "3D" vẽ bằng code (không dùng emoji): dây thông + quả châu bóng + đèn, tuyết 3 lớp có chiều sâu,
đèn bokeh ấm, mưa giấy kim tuyến lật 3D, thẻ nền chữ cao cấp lật 3D."""
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
rng0 = np.random.default_rng(21)


def _rgba(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- quả châu bóng
def qua_chau(r, mau, ss=3):
    R = r * ss
    y, x = np.mgrid[-R:R, -R:R].astype(np.float32)
    d = np.sqrt(x * x + y * y) / R
    inside = d <= 1
    # chiếu sáng cầu: pháp tuyến
    nz = np.sqrt(np.clip(1 - d * d, 0, 1))
    nx, ny = x / R, y / R
    lx, ly, lz = -0.45, -0.55, 0.7
    lam = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    base = np.array(mau, np.float32)
    col = base[None, None, :] * (0.25 + 0.85 * lam[..., None])
    # phản chiếu (spec)
    rx, ry, rz = 2 * nz * nx, 2 * nz * ny, 2 * nz * nz - 1
    spec = np.clip(rx * lx + ry * ly + rz * lz, 0, 1) ** 40
    col += 255 * spec[..., None] * 0.95
    # viền tối + ánh vành
    col *= (1 - 0.35 * d ** 6)[..., None]
    rim = np.clip((d - 0.82) / 0.18, 0, 1) * np.clip(ny + 0.3, 0, 1)
    col += np.array([255, 230, 190]) * rim[..., None] * 0.25
    a = np.zeros(d.shape + (4,), np.float32)
    a[..., :3] = col
    a[..., 3] = 255 * np.clip((1 - d) * R / 1.5, 0, 1) * inside
    im = _rgba(a).resize((2 * r, 2 * r), Image.LANCZOS)
    # nắp vàng + móc
    can = Image.new("RGBA", (2 * r, 2 * r + r // 2), (0, 0, 0, 0))
    can.alpha_composite(im, (0, r // 2))
    dr = ImageDraw.Draw(can)
    cw, ch = int(r * 0.55), int(r * 0.32)
    x0 = r - cw // 2
    for k in range(ch):
        g = int(150 + 90 * math.sin(math.pi * k / ch))
        dr.line((x0, r // 2 - ch // 2 + k + 2, x0 + cw, r // 2 - ch // 2 + k + 2), fill=(g, int(g * 0.8), int(g * 0.4), 255))
    dr.ellipse((r - r * 0.13, 0, r + r * 0.13, r * 0.3), outline=(220, 180, 100, 255), width=max(2, r // 18))
    return can


# ---------------------------------------------------------------- dây thông trên cùng
def day_thong(rong=W, cao=300, seed=4):
    rng = np.random.default_rng(seed)
    S = 2
    im = Image.new("RGBA", (rong * S, cao * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def path(s):  # 2 vòng võng
        return s * rong, 30 + 70 * abs(math.sin(math.pi * s * 2)) ** 0.8

    for layer, (n, shade) in enumerate(((2600, 0.55), (2600, 0.8), (1800, 1.0))):
        for _ in range(n):
            s = rng.uniform(-0.02, 1.02)
            bx, by = path(s)
            by += rng.normal(0, 14) + layer * 3
            ang = rng.uniform(0, 2 * math.pi)
            ln = rng.uniform(16, 34)
            g = rng.uniform(0.7, 1.1) * shade
            c = (int(22 * g), int(88 * g + rng.uniform(0, 20)), int(48 * g), 255)
            d.line((bx * S, by * S, (bx + ln * math.cos(ang)) * S, (by + ln * math.sin(ang)) * S), fill=c, width=2 * S)
    # dây hạt vàng
    pts = [path(s) for s in np.linspace(0, 1, 400)]
    for i, (x, y) in enumerate(pts[::3]):
        d.ellipse(((x - 2.4) * S, (y + 18 - 2.4) * S, (x + 2.4) * S, (y + 18 + 2.4) * S), fill=(235, 195, 110, 255))
    im = im.resize((rong, cao), Image.LANCZOS)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").point(lambda v: v * 120 // 255))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (0, 10))
    out.alpha_composite(im)
    return out, path


DEN = [(rng0.uniform(0.02, 0.98), rng0.uniform(0, 6.3), [(255, 214, 140), (255, 120, 100), (255, 240, 200)][i % 3])
       for i in range(26)]
_cache = {}


def lop_day_thong(cv, t, alpha=1.0):
    if "gar" not in _cache:
        _cache["gar"] = day_thong()
        _cache["bau"] = [qua_chau(46, (175, 20, 32)), qua_chau(40, (210, 160, 70)), qua_chau(34, (190, 30, 40)),
                         qua_chau(42, (225, 180, 90))]
    gar, path = _cache["gar"]
    g = gar if alpha >= 0.99 else _alpha(gar, alpha)
    cv.alpha_composite(g, (0, 0))
    dr = ImageDraw.Draw(cv)
    # đèn nhấp nháy (có quầng)
    glow = Image.new("RGBA", (W, 320), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for s, ph, c in DEN:
        x, y = path(s)
        k = 0.55 + 0.45 * math.sin(t * 4 + ph)
        r = 7 + 6 * k
        gd.ellipse((x - r * 2.2, y + 6 - r * 2.2, x + r * 2.2, y + 6 + r * 2.2), fill=c + (int(110 * k * alpha),))
        gd.ellipse((x - 4, y + 2, x + 4, y + 10), fill=(255, 250, 235, int(255 * alpha)))
    cv.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)), (0, 0))
    # quả châu đung đưa
    for j, s in enumerate((0.12, 0.38, 0.63, 0.88)):
        x, y = path(s)
        b = _cache["bau"][j]
        dai = 40 + 22 * (j % 2)
        ang = 7 * math.sin(t * 2.2 + j)
        bx = x + dai * math.sin(math.radians(ang))
        by = y + 15 + dai * math.cos(math.radians(ang))
        dr.line((x, y + 15, bx, by), fill=(230, 200, 140, int(220 * alpha)), width=2)
        bb = b.rotate(-ang, Image.BICUBIC, expand=True)
        dat(cv, bb if alpha >= 0.99 else _alpha(bb, alpha), bx, by + bb.height / 2 - 6)


def _alpha(im, a):
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


def dat(cv, s, cx, cy):
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    x0, y0, x1, y1 = max(0, -x), max(0, -y), min(s.width, W - x), min(s.height, H - y)
    if x1 > x0 and y1 > y0:
        cv.alpha_composite(s.crop((x0, y0, x1, y1)), (x + x0, y + y0))


# ---------------------------------------------------------------- tuyết 3 lớp + bokeh
def _dot(r, blur):
    k = ("dot", r, blur)
    if k not in _cache:
        s = int(r * 2 + blur * 4 + 4)
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r), fill=(255, 255, 255, 255))
        _cache[k] = im.filter(ImageFilter.GaussianBlur(blur)) if blur else im
    return _cache[k]


TUYET = []
for lop, (n, r0, r1, v0, v1, blur, a) in enumerate(((60, 1.5, 3, 40, 70, 0, 0.55), (34, 3, 6, 80, 120, 1, 0.75),
                                                     (10, 10, 18, 160, 220, 6, 0.55))):
    for _ in range(n):
        TUYET.append(dict(x=rng0.uniform(0, W), y0=rng0.uniform(0, H), v=rng0.uniform(v0, v1),
                          r=int(rng0.uniform(r0, r1)), b=blur, a=a, ph=rng0.uniform(0, 6.3), amp=10 + lop * 15))
BOKEH = [dict(x=rng0.uniform(0, W), y=rng0.choice([rng0.uniform(80, 520), rng0.uniform(1450, 1880)]),
              r=int(rng0.uniform(18, 46)), c=[(255, 205, 130), (255, 170, 110), (255, 235, 190)][i % 3],
              ph=rng0.uniform(0, 6.3), vx=rng0.uniform(-8, 8)) for i in range(16)]


def lop_tuyet_bokeh(cv, t, bokeh=0.5):
    if bokeh > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for b in BOKEH:
            k = 0.5 + 0.5 * math.sin(t * 1.3 + b["ph"])
            x = (b["x"] + b["vx"] * t) % W
            ld.ellipse((x - b["r"], b["y"] - b["r"], x + b["r"], b["y"] + b["r"]), fill=b["c"] + (int(90 * k * bokeh),))
        cv.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9)))
    for f in TUYET:
        y = (f["y0"] + f["v"] * t) % (H + 60) - 30
        x = f["x"] + f["amp"] * math.sin(t * 1.1 + f["ph"])
        dat(cv, _alpha(_dot(f["r"], f["b"]), f["a"]), x, y)


# ---------------------------------------------------------------- mưa kim tuyến lật 3D
CONF = [dict(x=rng0.uniform(60, W - 60), vy=rng0.uniform(260, 520), vx=rng0.uniform(-90, 90), w=rng0.uniform(14, 24),
             h=rng0.uniform(26, 42), sp=rng0.uniform(4, 9), rot=rng0.uniform(0, 360), vr=rng0.uniform(-200, 200),
             c=[(230, 190, 95), (200, 25, 40), (245, 225, 170), (40, 130, 70)][i % 4], d0=rng0.uniform(0, 0.4))
        for i in range(70)]


def lop_kim_tuyen(cv, u):
    """u = giây kể từ lúc bắt đầu rơi"""
    d = ImageDraw.Draw(cv)
    for c in CONF:
        tt = u - c["d0"]
        if tt < 0:
            continue
        y = -50 + c["vy"] * tt
        if y > H + 50:
            continue
        x = c["x"] + c["vx"] * tt + 30 * math.sin(tt * 3)
        flip = math.cos(tt * c["sp"])           # lật 3D: bề ngang co giãn theo cos
        w = c["w"] * abs(flip) + 1.5
        shade = 0.55 + 0.45 * abs(flip)
        col = tuple(int(v * shade) for v in c["c"]) + (235,)
        a = math.radians(c["rot"] + c["vr"] * tt)
        pts = [(-w / 2, -c["h"] / 2), (w / 2, -c["h"] / 2), (w / 2, c["h"] / 2), (-w / 2, c["h"] / 2)]
        pts = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
        d.polygon(pts, fill=col)


# ---------------------------------------------------------------- thẻ nền chữ cao cấp
KIEU = {
    "red": dict(c0=(150, 14, 28), c1=(92, 6, 16), vien=(236, 200, 120), vien2=(255, 236, 190), a=245),
    "brown": dict(c0=(70, 48, 30), c1=(30, 20, 13), vien=(214, 172, 100), vien2=(245, 220, 165), a=228),
}


def the_nen(w, h, kieu="brown"):
    k = ("the", int(w), int(h), kieu)
    if k in _cache:
        return _cache[k]
    K = KIEU[kieu]
    S = 2
    w, h = int(w), int(h)
    r = min(h // 2, 44)
    yy = np.linspace(0, 1, h * S)[:, None, None]
    grad = np.array(K["c0"])[None, None, :] * (1 - yy) + np.array(K["c1"])[None, None, :] * yy
    body = np.zeros((h * S, w * S, 4), np.float32)
    body[..., :3] = grad
    body[..., 3] = K["a"]
    body = _rgba(body)
    m = Image.new("L", (w * S, h * S), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), r * S, fill=255)
    out = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    out.paste(body, (0, 0), m)
    d = ImageDraw.Draw(out)
    # bóng kính nửa trên
    gl = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle((6 * S, 5 * S, w * S - 6 * S, h * S * 0.48), r * S, fill=(255, 255, 255, 34))
    out.alpha_composite(gl)
    # viền vàng kép
    d.rounded_rectangle((1 * S, 1 * S, w * S - 1 * S, h * S - 1 * S), r * S, outline=K["vien"] + (255,), width=4 * S)
    d.rounded_rectangle((10 * S, 10 * S, w * S - 10 * S, h * S - 10 * S), max(4, r - 9) * S,
                        outline=K["vien2"] + (120,), width=1 * S)
    # hoa văn kim cương 2 đầu
    for cx in (22 * S, w * S - 22 * S):
        cy = h * S / 2
        q = 7 * S
        d.polygon([(cx, cy - q), (cx + q * 0.7, cy), (cx, cy + q), (cx - q * 0.7, cy)], fill=K["vien2"] + (230,))
    out = out.resize((w, h), Image.LANCZOS)
    # đổ bóng
    pad = 40
    sh = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), r, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    sh.alpha_composite(out, (pad, pad))
    _cache[k] = sh
    return sh


def lat_3d(img, goc, scale=1.0):
    """xoay quanh trục ngang (rotateX) với phối cảnh -> ảnh RGBA mới, cùng tâm"""
    a = np.asarray(img)
    h, w = a.shape[:2]
    th = math.radians(goc)
    f = 1400.0
    pts = []
    for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
        X, Y = (x - w / 2) * scale, (y - h / 2) * scale
        Y2, Z = Y * math.cos(th), Y * math.sin(th)
        k = f / (f + Z)
        pts.append((w / 2 + X * k, h / 2 + Y2 * k))
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32(pts))
    return Image.fromarray(cv2.warpPerspective(a, M, (w, h), flags=cv2.INTER_LINEAR), "RGBA")


def ve_the_chu(cv, sp, t, kieu):
    """sp: mục chữ đã hiệu chỉnh (x, y, dong[(text, px, màu, font)], start, dur) -> vẽ thẻ khớp khung chữ"""
    import sys
    DC = sys.modules["dung_capcut"]
    ws = [DC.do_rong(tx, px, fp) for tx, px, _, fp in sp["dong"]]
    hs = sum(px * 1.22 for _, px, _, _ in sp["dong"])
    px0 = max(px for _, px, _, _ in sp["dong"])
    w = max(ws) + max(70, px0 * 1.1)
    h = hs + max(34, px0 * 0.55)
    u = t - sp["start"]
    het = sp["start"] + sp["dur"] - t
    if u < 0 or het < 0:
        return
    base = the_nen(w, h, kieu)
    if u < 0.35:           # lật vào 3D
        k = u / 0.35
        e = 1 - (1 - k) ** 3
        img = lat_3d(base, 80 * (1 - e), 0.85 + 0.15 * e + 0.05 * math.sin(math.pi * e))
        img = _alpha(img, min(1, k * 2))
    elif het < 0.15:       # thoát
        img = _alpha(base, het / 0.15)
    else:
        img = base
    dat(cv, img, sp["x"], sp["y"])
    # vệt sáng lướt
    sw = ((u - 0.4) * 0.8) % 2.2
    if u > 0.4 and sw < 1:
        gx = sp["x"] - w / 2 + sw * w
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([(gx - 20, sp["y"] - h / 2 + 6), (gx + 30, sp["y"] - h / 2 + 6),
                                     (gx + 5, sp["y"] + h / 2 - 6), (gx - 45, sp["y"] + h / 2 - 6)],
                                    fill=(255, 245, 220, 60))
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rounded_rectangle((sp["x"] - w / 2 + 4, sp["y"] - h / 2 + 4, sp["x"] + w / 2 - 4,
                                             sp["y"] + h / 2 - 4), min(int(h / 2), 40), fill=255)
        lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel("A")), np.asarray(m))))
        cv.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))
