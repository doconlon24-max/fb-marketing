"""Reels 20261109-1900 'ANOTHER LUCKY XMAS WINNER!' - đồng bộ mẫu MERAH XMAS GIFT 5.11 / LUCKY XMAS 6.11.
Chép từ bài 20261108-1900. Che mặt KHÁCH (áo nâu) bằng tim hồng vẽ vector (mat_video.npy / mat_anh.json từ do_mat.py),
bác sĩ áo xanh không che. Ảnh có chữ sẵn (thẻ quà) đặt thành thẻ giữa khung, chữ nằm ngoài.
python do_mat.py  rồi  python build_xmas.py"""
import glob, json, math, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
XMAS = r"C:\Users\Surface\Downloads\CLAUDE DỰNG VIDEO\ADS SPA 5.11"
sys.path.insert(0, XMAS)
import trang_tri as TT  # noqa: E402

SRC = "C:/MERAH/TƯ LIỆU MERAH ĐĂNG BÀI/9-11-2026/"
VID = SRC + "IMG_7897 (1).MOV"
PAST = r"C:\Users\Surface\Downloads\MERAH\CÁC BÀI ĐÃ ĐĂNG TRÊN PAGE\BÀI ĐĂNG -ẢNH REP MESS\ĐÃ ĐĂNG LÊN PAGE"
LOGO = os.path.join(ROOT, "tai-nguyen", "mau-thiet-ke", "logo_dark.png")
F_SERIF = "C:/Windows/Fonts/georgiab.ttf"
F_SANS = "C:/Users/Surface/AppData/Local/CapCut/Apps/6.8.1.2770/Resources/Font/SystemFont/CapCutSansText-Bold.otf"
if not os.path.exists(F_SANS):
    F_SANS = "C:/Windows/Fonts/segoeuib.ttf"
W, H, FPS = 1080, 1920, 30
GOLD_L, CREAM, BROWN = (238, 211, 156), (247, 238, 224), (74, 46, 34)

# ------------------------------------------------------------------ lịch dựng
SEG = [(6.0, 9.0, "hook"), (0.4, 6.0, "pan"), (9.0, 13.0, "pan")]     # (từ, đến) trong video gốc
V_END = sum(b - a for a, b, _ in SEG)                                    # 12.6
PH = [("photo_{{ID_FACEBOOK}}_w.jpg", 2.8), ("photo_{{ID_FACEBOOK}}_w.jpg", 2.4)]
PROMO_DUR = 3.8
PAST_PICK = [11, 23, 22, 17]
PAST_DUR = 0.8
END_DUR = 3.4
T_PH = V_END
T_PROMO = T_PH + sum(d for _, d in PH)
T_PAST = T_PROMO + PROMO_DUR
T_END = T_PAST + PAST_DUR * len(PAST_PICK)
TOTAL = T_END + END_DUR
CUTS = [3.0, 8.6, T_PH, T_PH + PH[0][1], T_PROMO, T_PAST] + [T_PAST + PAST_DUR * i for i in range(1, len(PAST_PICK))] + [T_END]

# thẻ chữ: (bắt đầu, độ dài, [(chữ, cỡ, màu, font)], x, y, kiểu)
CARDS = [
    (0.0, 3.0, [("ANOTHER LUCKY", 58, CREAM, F_SANS), ("XMAS WINNER!", 96, GOLD_L, F_SERIF)], 540, 330, "red"),
    (3.0, 2.9, [("WHAT'S INSIDE?", 56, CREAM, F_SANS)], 540, 300, "brown"),
    (5.9, 2.7, [("PURE CHRISTMAS JOY", 52, CREAM, F_SANS)], 540, 300, "brown"),
    (8.6, V_END - 8.6, [("PRIZE", 104, GOLD_L, F_SERIF), ("REVEALED!", 60, CREAM, F_SANS)], 540, 330, "red"),
    (3.0, V_END - 3.0, [("CHRISTMAS LUCKY DRAW AT MERAH", 34, GOLD_L, F_SANS)], 540, 1765, "brown"),
    (T_PH, PH[0][1], [("SHE WON A", 34, GOLD_L, F_SANS), ("WALLET + LIPSTICK!", 54, CREAM, F_SANS)], 540, 1690, "brown"),
    (T_PH + PH[0][1], PH[1][1], [("COULD YOU BE", 40, CREAM, F_SANS), ("NEXT?", 80, GOLD_L, F_SERIF)], 540, 1690, "red"),
    (T_PROMO, PROMO_DUR, [("40% OFF", 132, GOLD_L, F_SERIF), ("UNTIL NOV 30", 58, CREAM, F_SANS)], 540, 760, "red"),
    (T_PROMO + .35, PROMO_DUR - .35, [("EARLY XMAS GIFTS", 50, CREAM, F_SANS), ("UP TO ₱10,000", 62, GOLD_L, F_SANS)], 540, 1100, "brown"),
    (T_PROMO + .7, PROMO_DUR - .7, [("Limited gifts  ·  Selected treatments", 30, CREAM, F_SANS), ("Message us to see what you qualify for", 30, GOLD_L, F_SANS)], 540, 1390, "brown"),
    (T_PAST, T_END - T_PAST, [("MORE HAPPY GUESTS AT MERAH", 44, CREAM, F_SANS)], 540, 1745, "brown"),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)


_font = {}


def font(p, s):
    if (p, s) not in _font:
        _font[(p, s)] = ImageFont.truetype(p, s)
    return _font[(p, s)]


def text_img(lines):
    """khối chữ căn giữa, có bóng mờ"""
    ws, hs = [], []
    for tx, px, _, fp in lines:
        b = font(fp, px).getbbox(tx); ws.append(b[2] - b[0]); hs.append(int(px * 1.22))
    w, h = max(ws) + 20, sum(hs) + 10
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 4
    for (tx, px, col, fp), lh, lw in zip(lines, hs, ws):
        d.text((w / 2, y + lh / 2), tx, font=font(fp, px), fill=col + (255,), anchor="mm")
        y += lh
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: int(v * .55)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (0, 0)); out.alpha_composite(im)
    return out, w - 20, h


_cardc = {}


def draw_card(cv, c, t):
    st, du, lines, x, y, kieu = c
    u, het = t - st, st + du - t
    if u < 0 or het < 0:
        return
    key = id(c)
    if key not in _cardc:
        ti, tw, th = text_img(lines)
        px0 = max(px for _, px, _, _ in lines)
        bw, bh = tw + max(70, px0 * 1.1), th + max(34, px0 * .55)
        base = TT.the_nen(bw, bh, kieu).copy()
        TT.dat(base, ti, base.width / 2, base.height / 2 + 2)
        _cardc[key] = base
    base = _cardc[key]
    if u < .35:
        k = u / .35; e = 1 - (1 - k) ** 3
        img = TT._alpha(TT.lat_3d(base, 80 * (1 - e), .85 + .15 * e + .05 * math.sin(math.pi * e)), min(1, k * 2))
    elif het < .15:
        img = TT._alpha(base, het / .15)
    else:
        img = base
    TT.dat(cv, img, x, y)


# ------------------------------------------------------------------ tim hồng che mặt (vẽ vector, không dùng emoji)
_heart = {}


def heart(s):
    s = max(40, int(s) // 4 * 4)
    if s in _heart:
        return _heart[s]
    S = 4; n = s * S; pad = s // 5
    tt = np.linspace(0, 2 * np.pi, 400)
    hx = 16 * np.sin(tt) ** 3
    hy = -(13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt))
    hx = (hx + 17) / 34 * n; hy = (hy + 18) / 34 * n
    poly = list(zip(hx, hy))
    m = Image.new("L", (n, n), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    yy = np.linspace(0, 1, n)[:, None]
    g = np.zeros((n, n, 4), np.uint8)
    top, bot = np.array([255, 150, 190]), np.array([236, 72, 128])
    g[..., :3] = (top[None, None, :] * (1 - yy[:, :, None]) + bot[None, None, :] * yy[:, :, None]).astype(np.uint8)
    g[..., 3] = 255
    body = Image.fromarray(g, "RGBA")
    rim = Image.new("RGBA", (n, n), (0, 0, 0, 0)); ImageDraw.Draw(rim).polygon(poly, fill=(255, 255, 255, 255))
    inner = m.filter(ImageFilter.MinFilter(int(n * .06) // 2 * 2 + 1))
    hrt = Image.new("RGBA", (n, n), (0, 0, 0, 0)); hrt.paste(rim, (0, 0), m); hrt.paste(body, (0, 0), inner)
    gl = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse((n * .2, n * .18, n * .42, n * .36), fill=(255, 255, 255, 120))
    hrt.alpha_composite(gl.filter(ImageFilter.GaussianBlur(n * .02)))
    hrt = hrt.resize((s, s), Image.LANCZOS)
    out = Image.new("RGBA", (s + 2 * pad, s + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.paste((60, 10, 30, 110), (pad, pad + s // 18), hrt.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(s / 25))); out.alpha_composite(hrt, (pad, pad))
    _heart[s] = out
    return out


def cover(img, cx, cy, size, k=1.45):
    hs = heart(size * k)   # tự dán (TT.dat cắt theo khung 1080x1920, ảnh gốc rộng hơn)
    img.alpha_composite(hs, (int(cx - hs.width / 2), int(cy + size * .04 - hs.height / 2)))


GRADE = "eq=brightness=0.04:contrast=1.05:saturation=1.08,colorbalance=rs=0.04:gs=0.01:bs=-0.05"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]

# ------------------------------------------------------------------ 0. video gốc đã chỉnh màu + che mặt khách
FACES = np.load("mat_video.npy")
REDO = not os.path.exists("src_che.mp4") or "--redo" in sys.argv
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", VID, "-vf", f"scale={W}:{H},{GRADE},hqdn3d=1.5:1.5:3:3",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        *ENC, "src_che.mp4"], stdin=subprocess.PIPE) if REDO else None
i = 0
while REDO:
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3:
        break
    fr = Image.frombytes("RGB", (W, H), raw).convert("RGBA")
    cx, cy, s = FACES[min(i, len(FACES) - 1)]
    cover(fr, cx, cy, s)
    enc.stdin.write(fr.convert("RGB").tobytes()); i += 1
if REDO:
    enc.stdin.close(); enc.wait()
dec.kill()

# ------------------------------------------------------------------ 1. nền: các đoạn video
parts = []
for j, (a, b, kieu) in enumerate(SEG):
    n = int(round((b - a) * FPS))
    if kieu == "hook":   # punch zoom cận cảnh rồi nhả dần
        z = "1.16+0.16*max(0,1-on/9)"
    else:
        z = f"1+0.04*on/{n}"
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", "src_che.mp4", "-vf",
         f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='max(0,min(ih-ih/zoom,900-ih/zoom/2))':d=1:s=1080x1920:fps=30",
         "-frames:v", str(n), *ENC, f"b_v{j}.mp4"])
    parts.append(f"b_v{j}.mp4")


def still(img, dur, out, z0=1.0, z1=1.06):
    n = int(round(dur * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", img, "-vf",
         f"scale=1080:1920,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30",
         "-frames:v", str(n), *ENC, out])


def graded_photo(f):
    """ảnh khách: sáng ấm nhẹ + tim hồng che mặt khách"""
    im = Image.open(SRC + f).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.05)
    r, g, b = im.split(); r = r.point(lambda v: min(255, v * 1.03)); b = b.point(lambda v: v * .97); im = Image.merge("RGB", (r, g, b))
    im = im.convert("RGBA"); cx, cy, s = MAT[f]; cover(im, cx, cy, s, 1.5)
    return im.convert("RGB")


def card_on_blur(im, out, top=250):
    """ảnh đã có chữ -> thẻ nguyên vẹn giữa khung trên nền mờ (không chữ đè)"""
    bg = ImageEnhance.Brightness(ImageOps.fit(im, (W, H)).filter(ImageFilter.GaussianBlur(45))).enhance(.8)
    fg = ImageOps.contain(im, (900, 1300))
    m = Image.new("L", fg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *fg.size), 22, fill=255)
    sh = Image.new("RGBA", (fg.width + 80, fg.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 50, fg.width + 40, fg.height + 50), 24, fill=(30, 15, 5, 150))
    bg = bg.convert("RGBA"); x, y = (W - fg.width) // 2, top + (1330 - fg.height) // 2
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40))
    fr = Image.new("RGBA", (fg.width + 16, fg.height + 16), (0, 0, 0, 0))   # khung vàng
    ImageDraw.Draw(fr).rounded_rectangle((0, 0, fr.width - 1, fr.height - 1), 28, fill=(214, 172, 100, 255))
    bg.alpha_composite(fr, (x - 8, y - 8))
    bg.paste(fg, (x, y), m)
    bg.convert("RGB").save(out, quality=95)


MAT = json.load(open("mat_anh.json"))
for i, (f, d) in enumerate(PH):
    card_on_blur(graded_photo(f), f"ph{i}.jpg"); still(f"ph{i}.jpg", d, f"b_ph{i}.mp4", 1.0, 1.05); parts.append(f"b_ph{i}.mp4")

# cảnh ưu đãi: nền ảnh 304 mờ tối ấm (đã che mặt trước khi làm mờ)
pr = graded_photo("photo_{{ID_FACEBOOK}}_w.jpg")
pr = ImageOps.fit(pr, (W, H)).filter(ImageFilter.GaussianBlur(40))
pr = Image.blend(pr, Image.new("RGB", (W, H), (70, 30, 20)), .45)
pr.save("promo.jpg", quality=95); still("promo.jpg", PROMO_DUR, "b_promo.mp4", 1.0, 1.04); parts.append("b_promo.mp4")

past = sorted(glob.glob(PAST + r"\*.jpg"))
for i, k in enumerate(PAST_PICK):
    card_on_blur(Image.open(past[k]).convert("RGB"), f"pa{i}.jpg"); still(f"pa{i}.jpg", PAST_DUR, f"b_pa{i}.mp4", 1.0, 1.03); parts.append(f"b_pa{i}.mp4")

# outro nền kem
end = Image.new("RGB", (W, H), (246, 238, 228)); ed = ImageDraw.Draw(end)
for yy in range(H):
    k = abs(yy - H * .45) / H
    ed.line((0, yy, W, yy), fill=(int(248 - 18 * k), int(241 - 22 * k), int(231 - 26 * k)))
lg = Image.open(LOGO).convert("RGBA"); lg = lg.resize((330, int(330 * lg.height / lg.width)))
end = end.convert("RGBA"); TT.dat(end, lg, W / 2, 740)
ed = ImageDraw.Draw(end)
for tx, px, fp, col, y in [("MESSAGE US", 76, F_SERIF, (90, 58, 36), 1010), ("TO BOOK", 76, F_SERIF, (150, 104, 58), 1100),
                           ("Christmas Lucky Draw for our beauty clients  ·  Limited gifts", 28, F_SANS, (110, 78, 52), 1215),
                           ("MAKATI CITY  ·  {{SO_DIEN_THOAI}}", 36, F_SANS, (110, 78, 52), 1290),
                           ("YOUR CONFIDENCE, YOUR GLOW", 24, F_SANS, (150, 120, 90), 1560)]:
    ed.text((W / 2, y), tx, font=font(fp, px), fill=col, anchor="mm")
ed.line((W / 2 - 160, 1170, W / 2 + 160, 1170), fill=(184, 144, 92), width=2)
end.convert("RGB").save("end.jpg", quality=95); still("end.jpg", END_DUR, "b_end.mp4", 1.0, 1.02); parts.append("b_end.mp4")

with open("list_xmas.txt", "w", encoding="utf-8") as f:
    f.writelines(f"file '{p}'\n" for p in parts)
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "list_xmas.txt", *ENC, "base.mp4"])

# ------------------------------------------------------------------ 2. lớp Giáng sinh + chữ, ghép từng khung
logo_s = Image.open(LOGO).convert("RGBA"); logo_s = logo_s.resize((96, int(96 * logo_s.height / logo_s.width)))
rng = np.random.default_rng(5)
SPK = [(rng.uniform(80, W - 80), rng.uniform(500, 1500), rng.uniform(0, 6.3), rng.uniform(3, 6)) for _ in range(18)]
GARL = ((0.0, 3.0), (8.6, V_END), (T_PROMO, T_PAST), (T_END, TOTAL + 1))


def frame_overlay(t):
    cv = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    big = t < 3.0 or 8.6 <= t < V_END or T_PROMO <= t < T_PAST or t >= T_END
    TT.lop_tuyet_bokeh(cv, t, bokeh=.6 if big else .3)
    for a0, b0 in GARL:
        if a0 <= t < b0:
            g = max(0.0, min(1.0, (t - a0) / .3 if a0 > 0 else 1.0, (b0 - t) / .3))
            TT.lop_day_thong(cv, t, g)
    if t < 2.6:
        TT.lop_kim_tuyen(cv, t + .3)
    if 8.6 <= t < V_END + .5:
        TT.lop_kim_tuyen(cv, t - 8.6)
    if T_PROMO <= t < T_PROMO + 2.6:
        TT.lop_kim_tuyen(cv, t - T_PROMO)
    d = ImageDraw.Draw(cv)
    for a0, b0 in ((0.0, 1.8), (8.6, V_END)):
        if a0 <= t < b0:
            for x, y, ph, sp in SPK:
                if 620 < y < 1150 and x > 480:   # không lấp lánh đè lên mặt khách / bác sĩ
                    continue
                al = max(0.0, math.sin((t - a0) * sp + ph)); r = 12 + 10 * al; c = GOLD_L + (int(255 * al),)
                d.line((x - r, y, x + r, y), fill=c, width=4); d.line((x, y - r, x, y + r), fill=c, width=4)
    for c in CUTS:
        dt = t - c
        if -.1 <= dt < .2:
            k = (dt + .1) / .1 if dt < 0 else 1 - dt / .2; k = k * k * (3 - 2 * k)
            cv.alpha_composite(Image.new("RGBA", (W, H), (255, 244, 220, int(150 * k))))
    if t < T_END:
        TT.dat(cv, logo_s, W / 2, 95)
    for c in CARDS:
        draw_card(cv, c, t)
    return cv


N = int(round(TOTAL * FPS))
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "base.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "video_only.mp4"], stdin=subprocess.PIPE)
for i in range(N):
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3:
        break
    fr = Image.frombytes("RGB", (W, H), raw).convert("RGBA")
    fr.alpha_composite(frame_overlay(i / FPS))
    enc.stdin.write(fr.convert("RGB").tobytes())
    if i % 150 == 0:
        print(f"khung {i}/{N}", flush=True)
enc.stdin.close(); enc.wait(); dec.wait()

# ------------------------------------------------------------------ 3. nhạc + tiếng thật
run([sys.executable, "nhac_giang_sinh.py", f"{TOTAL:.2f}", f"0-{V_END}:-10"])
fa = ";".join(f"[2:a]atrim={a}:{b},asetpts=PTS-STARTPTS[s{j}]" for j, (a, b, _) in enumerate(SEG))
fa += ";" + "".join(f"[s{j}]" for j in range(len(SEG))) + f"concat=n={len(SEG)}:v=0:a=1,volume=0.9,afade=t=out:st={V_END - .4}:d=0.4[v]"
run(["ffmpeg", "-y", "-v", "error", "-i", "video_only.mp4", "-i", "NHAC_GIANG_SINH.wav", "-i", VID,
     "-filter_complex", fa + f";[1:a][v]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,volume=-1.3dB,"
     f"afade=t=out:st={TOTAL - 1}:d=1[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
     "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", "../video.mp4"])
run(["ffmpeg", "-y", "-v", "error", "-ss", "1.2", "-i", "../video.mp4", "-frames:v", "1", "../anh_bia.jpg"])
print("xong", round(TOTAL, 2), "giây")
