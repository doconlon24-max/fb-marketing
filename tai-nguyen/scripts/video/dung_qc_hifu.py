"""Dựng video QUẢNG CÁO theo mẫu "Ngọc Dung HIFU" (tai-nguyen/hoc-video/ngoc-dung-hifu.md), nhận diện MERAH.
python dung_qc_hifu.py <cau_hinh.json> <ra.mp4>
cau_hinh.json: {
  "nguon": "raw.mp4",                     # video thô (dọc)
  "truoc": [t0, t1], "sau": [t0, t1],     # khoảng giây trước/sau trong video thô
  "the": [[giay, x, y, w, h, "Nhãn"], ...],   # 3 thẻ cận vùng (toạ độ theo khung 1080x1920 sau khi phóng)
  "vong": [x, y, r],                      # vòng tròn tự vẽ trên cảnh 'trước'
  "uu_dai": {"dich_vu": "MAXFILL COLLAGEN", "nhan": "CHRISTMAS DEAL", "tu": "FROM", "gia": "₱2,999",
             "dong1": "40% OFF · until Nov 30", "dong2": "Gifts up to ₱10,000"},
  "loi_ich": ["INSTANT VOLUME", "SHARPER JAWLINE", "QUICK 15–30 MIN"],
  "cta": ["LIMITED GIFTS", "MESSAGE US NOW"],
  "ghi_chu_ket_qua": "Sample result · Results may vary",
  "giong": "vo.mp3", "giong_doan": "vo_doan.json",   # tuỳ chọn
  "nhac": true
}
"""
import json, math, os, random, subprocess, sys, shutil
from PIL import ImageChops
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LOGO = os.path.join(ROOT, "thuong-hieu", "logo", "LOGO_MR_vang_nau_trong_suot.png")
FD = "C:/Windows/Fonts/" if os.name == "nt" else "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    for f in [FD + name, FD + "DejaVuSans-Bold.ttf", FD + "DejaVuSerif-Bold.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()
SERIF = lambda s: font("georgiab.ttf" if os.name == "nt" else "DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("segoeuib.ttf" if os.name == "nt" else "DejaVuSans-Bold.ttf", s)
SANSI = lambda s: font("segoeuii.ttf" if os.name == "nt" else "DejaVuSans-Oblique.ttf", s)
NAU, VANG, KEM, DO = (150, 104, 58), (201, 164, 106), (243, 233, 220), (179, 32, 42)


def ease(x):
    x = max(0, min(1, x)); return x * x * (3 - 2 * x)


def back(x):  # nảy
    x = max(0, min(1, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, *im.size], r, fill=255)
    out = im.convert("RGBA"); out.putalpha(m); return out


def shadow(im, r=28, off=14, a=120):
    pad = r * 2; sh = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    m = Image.new("L", sh.size, 0); m.paste(im.split()[-1], (pad, pad)); m = m.filter(ImageFilter.GaussianBlur(r))
    sh.putalpha(m.point(lambda v: v * a // 255)); out = sh.copy(); out.alpha_composite(im, (pad - off // 2, pad - off)); return out, pad


def text_c(d, cx, y, s, f, fill, stroke=0, sc=None):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc)


def gold_text(s, f):
    """Chữ vàng 3D: gradient + viền nâu + bóng."""
    tmp = ImageDraw.Draw(Image.new("L", (1, 1))); bb = tmp.textbbox((0, 0), s, font=f, stroke_width=6)
    w, h = bb[2] - bb[0] + 30, bb[3] - bb[1] + 40
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).text((15 - bb[0], 10 - bb[1]), s, font=f, fill=255)
    grad = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / h; c = [int(a + (b - a) * (0.5 + 0.5 * math.cos(t * 6.2))) for a, b in zip((255, 236, 170), (176, 120, 40))]
        ImageDraw.Draw(grad).line([(0, y), (w, y)], fill=tuple(c))
    edge = Image.new("L", (w, h), 0); ImageDraw.Draw(edge).text((15 - bb[0], 10 - bb[1]), s, font=f, fill=255, stroke_width=6, stroke_fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (60, 30, 10, 0)); sh.putalpha(edge.filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * 0.6))
    out.alpha_composite(sh, (0, 6))
    br = Image.new("RGBA", (w, h), (110, 66, 24, 255)); br.putalpha(edge); out.alpha_composite(br)
    g = grad.convert("RGBA"); g.putalpha(mask); out.alpha_composite(g)
    hl = Image.new("RGBA", (w, h), (255, 255, 255, 0)); hm = mask.crop((0, 0, w, h // 3)).point(lambda v: v * 0.35)
    hl.putalpha(Image.new("L", (w, h), 0)); hl.paste((255, 255, 255, 90), (0, 0, w, h // 3), hm); out.alpha_composite(hl)
    return out


def pill(text, f, w_full, prog, bg=NAU):
    """Thanh pill quét trái → phải, chữ hiện sau."""
    h = int(f.size * 1.9); im = Image.new("RGBA", (w_full, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ww = int(w_full * ease(min(1, prog / 0.55)))
    if ww > h:
        d.rounded_rectangle([0, 0, ww, h], h // 2, fill=bg + (235,), outline=VANG + (255,), width=3)
    if prog > 0.5:
        a = int(255 * ease((prog - 0.5) / 0.3))
        tw = d.textlength(text, font=f); d.text(((w_full - tw) / 2, h * 0.18), text, font=f, fill=(255, 255, 255, a))
    return im



def chay(a, b, x):
    """Thời điểm cảnh quay thật: chạy ĐÚNG tốc độ gốc (1x) từ a; hết đoạn [a,b] thì chạy lùi rồi tới (boomerang) – không bao giờ lặp khung/đứng hình."""
    span = b - a
    if span <= 0.05:
        return a
    k = x % (2 * span)
    return a + (k if k < span else 2 * span - k)


def tho(im, lt, D, amp=0.03):
    """Zoom thở rất nhẹ liên tục trong mỗi đoạn để hình không bao giờ đứng yên (mượt như video quay)."""
    z = 1 + 0.4 * amp * max(0.0, lt)  # đẩy cận đều ~1.2%/giây, không chậm dần -> không có khung trùng
    if z <= 1.0005:
        return im
    cw, ch = W / z, H / z; x0, y0 = (W - cw) / 2, (H - ch) / 2
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))

class Src:
    def __init__(self, path, tmp):
        self.dir = os.path.join(tmp, "src"); os.makedirs(self.dir, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vf",
                        f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},hqdn3d=1.5:1.5:3:3,unsharp=5:5:1.0:5:5:0.0,eq=brightness=0.03:saturation=1.05",
                        os.path.join(self.dir, "%05d.jpg")], check=True)
        self.n = len(os.listdir(self.dir))

    def at(self, t):
        i = max(1, min(self.n, int(round(t * FPS)) + 1)); return Image.open(os.path.join(self.dir, f"{i:05d}.jpg")).convert("RGB")


def main(cfg_path, out):
    C = json.load(open(cfg_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda k: os.path.join(base, C[k]) if C.get(k) else None
    tmp = os.path.join(base, "_dung"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    S = Src(p("nguon"), tmp); fr = os.path.join(tmp, "f"); os.makedirs(fr)
    logo = Image.open(LOGO).convert("RGBA"); logo = logo.resize((150, int(150 * logo.height / logo.width)))
    tb0, tb1 = C["truoc"]; ta0, ta1 = C["sau"]
    # độ dài đoạn theo giọng đọc
    vo = [2.6, 7.0, 4.2, 3.0]
    if C.get("giong_doan") and os.path.exists(p("giong_doan")):
        vo = [x["giay"] for x in json.load(open(p("giong_doan"), encoding="utf-8"))][:4]
    A = 2.4; Bg = 0.35; Cc = max(2.4, vo[0] + 0.6 - A - Bg)
    Dd = 3.0; Ee = max(4.0, vo[1] + 0.5 - Dd); Ff = max(4.2, vo[2] + 0.5); Gg = max(3.2, vo[3] + 0.6); Oo = 2.0
    seg = [("A", A), ("B", Bg), ("C", Cc), ("D", Dd), ("E", Ee), ("F", Ff), ("G", Gg), ("O", Oo)]
    starts = {}; t = 0
    for k, d in seg:
        starts[k] = t; t += d
    total = t
    blur_before = S.at(tb0 + 0.5).filter(ImageFilter.GaussianBlur(30))
    sparks = [(random.random() * W, random.random() * H, random.random() * 6 + 2, random.random() * 6.28) for _ in range(60)]
    U = C["uu_dai"]

    def sparkle(im, tt, k=1.0):
        d = ImageDraw.Draw(im)
        for x, y, r, ph in sparks:
            a = (math.sin(tt * 4 + ph) + 1) / 2
            if a > 0.55:
                yy = (y - tt * 60) % H; rr = r * a * k
                d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=(255, 236, 180, int(200 * a)))
                d.line([x - rr * 2.5, yy, x + rr * 2.5, yy], fill=(255, 245, 210, int(150 * a)), width=1)

    def overlay_logo(im):
        im.alpha_composite(logo, (W - logo.width - 40, 40))

    for i in range(int(total * FPS)):
        tt = i / FPS
        k = max(kk for kk, _ in seg if starts[kk] <= tt) if False else [kk for kk, _ in seg if starts[kk] <= tt][-1]
        lt = tt - starts[k]
        if k == "A":  # chồng thẻ 3D
            im = blur_before.copy().convert("RGBA")
            im.alpha_composite(Image.new("RGBA", (W, H), (40, 24, 12, 90)))
            cards = C["the"]; per = A / len(cards)
            for j in range(len(cards) - 1, -1, -1):
                gs, x, y, w, h, lab = cards[j]
                src = S.at(gs).crop((x, y, x + w, y + h)).resize((700, 900))
                card = rounded(src, 46); d = ImageDraw.Draw(card)
                for yy in range(560, 900):
                    a = int(230 * (yy - 560) / 340); d.line([(0, yy), (700, yy)], fill=NAU + (a,))
                card = rounded(card.convert("RGB"), 46) if False else card
                top_lab = (lab, card)
                off = j - max(0.0, lt - 0.45 * per) / per
                if j == len(cards) - 1:
                    off = max(off, 0.0)
                if off < -1:
                    continue
                if off < 0:  # đang trượt ra
                    pr = ease(-off); dx = -pr * 1100; rot = pr * 18; alpha = 1 - pr * 0.3
                else:
                    dx = off * 26; rot = -off * 4; alpha = 1
                c2 = card.rotate(rot, expand=True, resample=Image.BICUBIC)
                if off < 0.5:  # chỉ thẻ trên cùng hiện nhãn
                    dl = ImageDraw.Draw(c2); f54 = SANS(58)
                    dl.text((c2.width / 2 - dl.textlength(lab, font=f54) / 2, c2.height - 150), lab, font=f54, fill=(255, 255, 255, 255))
                cs, pad = shadow(c2)
                im.alpha_composite(cs, (int((W - c2.width) / 2 + dx - pad), int(430 + off * 22 - pad)))
        elif k == "B":  # glitch cắt lát
            a = S.at(tb0); im = a.copy().convert("RGBA"); rnd = random.Random(i)
            for s in range(14):
                y0 = rnd.randint(0, H - 60); hh = rnd.randint(20, 90); sh = rnd.randint(-120, 120)
                band = a.crop((0, y0, W, y0 + hh)); im.paste(band, (sh, y0))
            r, g, b = im.convert("RGB").split(); im = Image.merge("RGB", (ImageChops.offset(r, 12, 0), g, b)).convert("RGBA")
            im.alpha_composite(Image.new("RGBA", (W, H), (120, 80, 200, 40)))
        elif k == "C":  # cảnh trước + vòng tròn tự vẽ
            im = S.at(chay(tb0, tb1, lt)).convert("RGBA"); d = ImageDraw.Draw(im)
            cx, cy, r = C["vong"]; pr = ease(min(1, lt / 0.9))
            d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], -100, -100 + 360 * pr, fill=(230, 40, 50, 255), width=10)
            pp = pill("BEFORE", SANS(44), 300, min(1, lt / 0.6), bg=(60, 40, 30)); im.alpha_composite(pp, (60, 260))
        elif k == "D":  # trước | sau 2 thẻ
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            text_c(d, W / 2, 230, "REAL GLOW-UP", SERIF(84), NAU)
            for j, (src_t, lab) in enumerate([(tb0 + 0.4, "BEFORE"), (chay(ta0, ta1 - .05, 1.0 + lt), "AFTER")]):
                zoom = 1 + 0.04 * ease(lt / Dd)
                fimg = S.at(src_t); cw, ch = int(W / zoom), int(H / zoom)
                fimg = fimg.crop(((W - cw) // 2, (H - ch) // 2 + 60, (W + cw) // 2, (H + ch) // 2 + 60)).resize((480, 860))
                card = rounded(fimg, 36); d2 = ImageDraw.Draw(card)
                d2.rounded_rectangle([0, 0, 479, 859], 36, outline=VANG + (255,), width=6)
                pr = back(min(1, (lt - j * 0.25) / 0.5))
                if pr <= 0:
                    continue
                c2 = card.resize((max(1, int(480 * pr)), max(1, int(860 * pr))))
                cs, pad = shadow(c2)
                im.alpha_composite(cs, (int(45 + j * 510 + (480 - c2.width) / 2 - pad), int(400 + (860 - c2.height) / 2 - pad)))
                pl = pill(lab, SANS(40), 260, min(1, max(0, (lt - 0.4 - j * 0.25) / 0.6)), bg=NAU if j else (90, 70, 60))
                im.alpha_composite(pl, (int(45 + j * 510 + 110), 1300))
            text_c(d, W / 2, 1420, C.get("ghi_chu_ket_qua", ""), SANSI(30), (120, 90, 60))
            sparkle(im, tt, 0.6)
        elif k == "E":  # thẻ ưu đãi giá vàng 3D
            im = S.at(chay(ta0, ta1 - .05, 0.5 + lt)).filter(ImageFilter.GaussianBlur(24)).convert("RGBA")
            im.alpha_composite(Image.new("RGBA", (W, H), KEM + (150,)))
            pr = back(min(1, lt / 0.6)); cw, ch = int(900 * pr), int(1180 * pr)
            if cw > 10:
                card = Image.new("RGBA", (900, 1180), (255, 251, 244, 245)); d = ImageDraw.Draw(card)
                d.rounded_rectangle([0, 0, 899, 1179], 48, outline=VANG + (255,), width=8)
                d.rounded_rectangle([280, 50, 620, 120], 35, fill=DO + (255,)); text_c(d, 450, 60, U["nhan"], SANS(40), (255, 255, 255))
                text_c(d, 450, 175, U["dich_vu"].split()[0], SERIF(110), NAU)
                if len(U["dich_vu"].split()) > 1:
                    text_c(d, 450, 300, " ".join(U["dich_vu"].split()[1:]), SERIF(80), NAU)
                text_c(d, 450, 430, U["tu"], SANS(56), (110, 80, 50))
                gt = gold_text(U["gia"], SANS(220)); card.alpha_composite(gt, (int(450 - gt.width / 2), 490))
                text_c(d, 450, 820, U["dong1"], SANS(54), DO)
                text_c(d, 450, 910, U["dong2"], SANS(50), NAU)
                d.rounded_rectangle([200, 1020, 700, 1110], 45, fill=NAU + (255,)); text_c(d, 450, 1035, "MESSAGE US", SANS(50), (255, 255, 255))
                c2 = card.resize((cw, ch)); cs, pad = shadow(c2, 30, 18, 140)
                im.alpha_composite(cs, (int((W - cw) / 2 - pad), int((H - ch) / 2 - pad + 40)))
            sparkle(im, tt, 1.2)
        elif k == "F":  # lợi ích pill quét
            span = ta1 - ta0; im = S.at(chay(ta0, ta1 - .05, lt)).convert("RGBA")
            li = C["loi_ich"]; per = Ff / len(li); j = min(len(li) - 1, int(lt / per)); pr = min(1, (lt - j * per) / 0.9)
            pl = pill("✓  " + li[j] if False else li[j], SANS(56), 860, pr)
            im.alpha_composite(pl, (110, 1480))
            if pr > 0.6:
                d = ImageDraw.Draw(im); cx, cy = 180, 1480 + pl.height // 2; rr = 30 * back(min(1, (pr - 0.6) / 0.4))
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(70, 170, 90, 255))
                if rr > 15:
                    d.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 14, cy - 10)], fill=(255, 255, 255), width=6)
            d = ImageDraw.Draw(im); text_c(d, W / 2, 1780, C.get("ghi_chu_ket_qua", ""), SANSI(28), (255, 255, 255))
        elif k == "G":  # CTA khan hiếm
            im = S.at(ta1 - 0.1).convert("RGBA")
            pr = back(min(1, lt / 0.5)); st = Image.new("RGBA", (860, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
            d.rounded_rectangle([0, 0, 859, 419], 60, fill=(255, 251, 244, 245), outline=VANG + (255,), width=8)
            text_c(d, 430, 50, C["cta"][0], SERIF(92), DO)
            d.rounded_rectangle([110, 210, 750, 340], 65, fill=NAU + (255,)); text_c(d, 430, 232, C["cta"][1], SANS(66), (255, 255, 255))
            bob = math.sin(lt * 5) * 8; s2 = st.resize((max(1, int(860 * pr)), max(1, int(420 * pr))))
            cs, pad = shadow(s2); im.alpha_composite(cs, (int((W - s2.width) / 2 - pad), int(260 + bob - pad)))
            if lt > 0.8:  # con trỏ bấm
                cl = (lt - 0.8) % 1.2; d = ImageDraw.Draw(im); x0, y0 = 720, 600 + bob
                sc = 0.85 if cl < 0.15 else 1.0
                pts = [(0, 0), (0, 70), (18, 54), (32, 84), (44, 78), (30, 49), (54, 49)]
                d.polygon([(x0 + px * sc, y0 + py * sc) for px, py in pts], fill=(255, 255, 255), outline=(30, 30, 30))
                if cl < 0.35:
                    rr = 20 + cl * 120; d.ellipse([x0 - rr, y0 - rr, x0 + rr, y0 + rr], outline=(255, 255, 255, int(255 * (1 - cl / 0.35))), width=5)
            sparkle(im, tt, 0.8)
        else:  # outro
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            big = Image.open(LOGO).convert("RGBA"); big = big.resize((420, int(420 * big.height / big.width)))
            pr = ease(min(1, lt / 0.5)); big.putalpha(big.split()[-1].point(lambda v: int(v * pr)))
            im.alpha_composite(big, ((W - big.width) // 2, 560))
            text_c(d, W / 2, 1060, "MERAH BEAUTY", SERIF(86), NAU)
            text_c(d, W / 2, 1180, "Makati City  ·  {{SO_DIEN_THOAI}}", SANS(44), (110, 80, 50))
            text_c(d, W / 2, 1270, "Message us to book", SANSI(46), DO)
            sparkle(im, tt, 0.7)
        if k not in ("O",):
            overlay_logo(im)
        im.convert("RGB").save(os.path.join(fr, f"{i:05d}.jpg"), quality=90)
    # âm thanh
    vid = os.path.join(tmp, "v.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", vid], check=True)
    ins, flt, n = ["-i", vid], [], 1
    starts_vo = [0.25, starts["D"] + 0.15, starts["F"] + 0.1, starts["G"] + 0.1]
    if C.get("giong") and os.path.exists(p("giong")):
        # tách từng đoạn giọng theo thời lượng rồi đặt đúng mốc
        acc = 0
        for j, dur in enumerate(vo):
            ins += ["-ss", str(acc), "-t", str(dur), "-i", p("giong")]; acc += dur
            flt.append(f"[{n}:a]adelay={int(starts_vo[j]*1000)}|{int(starts_vo[j]*1000)},volume=1.15[v{j}]"); n += 1
    nh = None
    if C.get("nhac", True):
        duck = ",".join(f"{starts_vo[j]:.2f}-{starts_vo[j]+vo[j]:.2f}:-12" for j in range(len(vo)))
        subprocess.run([sys.executable, os.path.join(HERE, "nhac_giang_sinh.py"), f"{total:.2f}", duck], cwd=tmp, check=True)
        for cand in [os.path.join(tmp, "NHAC_GIANG_SINH.wav"), os.path.join(HERE, "NHAC_GIANG_SINH.wav")]:
            if os.path.exists(cand):
                nh = cand; break
    if nh:
        ins += ["-i", nh]; flt.append(f"[{n}:a]volume=0.55[m]"); n += 1
    labels = [f"[v{j}]" for j in range(len(vo)) if any(f"[v{j}]" in x for x in flt)] + (["[m]"] if nh else [])
    if labels:
        flt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", out], check=True)
    else:
        shutil.copy(vid, out)
    print(f"Xong {out}: {total:.1f}s; mốc đoạn: " + ", ".join(f"{k}={starts[k]:.1f}" for k, _ in seg))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
