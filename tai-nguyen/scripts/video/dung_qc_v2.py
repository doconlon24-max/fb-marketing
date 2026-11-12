"""Video QC MERAH v2 – kịch bản người dùng chốt 10/11/2026:
1 Full mặt khách (hook) → 2 chồng thẻ chi tiết vấn đề (chậm) → 3 "Chỉ 30 phút cùng MAXFILL tại MERAH" (đồng hồ chạy + hoạt hình HA collagen
vào lớp da, KHÔNG vẽ kim tiêm, da săn chắc/trẻ hoá) → 4 chuyển cảnh khách đẹp → 5 before|after cùng 1 khung → 6 outro ảnh thật MERAH
(khách + bác sĩ check-in, feedback điện thoại, tin nhắn, BA khách thật) → 7 khuyến mãi → 8 CTA → 9 logo.
python dung_qc_v2.py <cau_hinh.json> <ra.mp4>   (cấu hình như dung_qc_hifu.py + "anh_that": [ảnh...], "giong_doan" 8 đoạn)
"""
import json, math, os, random, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dung_qc_hifu import (chay, tho, W, H, FPS, LOGO, SERIF, SANS, SANSI, NAU, VANG, KEM, DO, ease, back, rounded, shadow, text_c,
                          gold_text, pill, Src)

HERE = os.path.dirname(os.path.abspath(__file__))


def fit_card(img, w, h, r=40, border=VANG):
    """Ảnh vừa khung, GIỮ tỉ lệ, chỉ bo góc chính ảnh – không thêm nền trắng/kem."""
    im = img.convert("RGB"); k = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    c = rounded(im, r); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], r, outline=border + (255,), width=4); return c


def sharp_card(S, gs, x, y, w, h, scale=1.25, win=0.15):
    """Thẻ vấn đề NÉT: cắt rộng hơn (bớt phóng to), chọn khung nét nhất trong ±win giây, Lanczos + khử nhiễu + tăng nét."""
    cx, cy = x + w / 2, y + h / 2; w2, h2 = int(w * scale), int(h * scale)
    x2 = int(min(max(0, cx - w2 / 2), W - w2)); y2 = int(min(max(0, cy - h2 / 2), H - h2))
    try:
        import cv2, numpy as np
    except ImportError:  # đám mây không có opencv: Lanczos + UnsharpMask bằng PIL
        im = S.at(gs).crop((x2, y2, x2 + w2, y2 + h2)).resize((700, 900), Image.LANCZOS)
        return im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=160, threshold=2))
    best, bv = None, -1
    for k in range(int((gs - win) * FPS), int((gs + win) * FPS) + 1):
        a = np.array(S.at(max(0, k / FPS)))[y2:y2 + h2, x2:x2 + w2]
        v = cv2.Laplacian(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var()
        if v > bv:
            best, bv = a, v
    a = cv2.resize(best, (700, 900), interpolation=cv2.INTER_LANCZOS4); a = cv2.bilateralFilter(a, 5, 30, 5)
    a = cv2.addWeighted(a, 1.8, cv2.GaussianBlur(a, (0, 0), 2.2), -0.8, 0)
    return Image.fromarray(a)


SERVICE = "MAXFILL"


def skin_anim(lt, dur):
    """Hoạt hình: đồng hồ 0→30 phút + mặt cắt lớp da, hạt HA collagen lan vào, sợi collagen mọc, nếp nhăn phẳng dần. Không có kim."""
    im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im); p = ease(min(1, lt / (dur * 0.85)))
    text_c(d, W / 2, 130, "ONLY 30 MINUTES", SERIF(96), NAU)
    text_c(d, W / 2, 245, "with " + SERVICE + " at MERAH Beauty", SANSI(50), (120, 85, 50))
    # đồng hồ
    cx, cy, R = W / 2, 660, 200
    d.ellipse([cx - R - 18, cy - R - 18, cx + R + 18, cy + R + 18], fill=(255, 251, 244), outline=VANG, width=14)
    d.rectangle([cx - 26, cy - R - 70, cx + 26, cy - R - 18], fill=VANG); d.rounded_rectangle([cx - 60, cy - R - 100, cx + 60, cy - R - 64], 14, fill=NAU)
    d.pieslice([cx - R, cy - R, cx + R, cy + R], -90, -90 + 360 * p * 0.5, fill=(232, 205, 160))
    for k in range(60):
        a = math.radians(k * 6 - 90); r1 = R - (26 if k % 5 == 0 else 12)
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a)], fill=NAU, width=5 if k % 5 == 0 else 2)
    a = math.radians(-90 + 360 * p * 0.5)
    d.line([cx, cy, cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a)], fill=DO, width=10); d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=DO)
    mins = int(round(30 * p)); text_c(d, cx, cy + 70, f"{mins:02d} MIN", SANS(64), NAU)
    # mặt cắt da
    top = 1020; bw = 920; x0 = (W - bw) / 2; amp = 26 * (1 - p)
    def surf(x):
        return top + amp * math.sin((x - x0) / 55) + (amp * 0.6) * math.sin((x - x0) / 23)
    layers = [((250, 214, 190), 0, 70), ((240, 190, 165), 70, 330), ((250, 230, 170), 330, 520)]
    for col, a1, a2 in layers:
        pts = [(x, surf(x) + a1) for x in range(int(x0), int(x0 + bw) + 1, 8)] + [(x, surf(x) + a2) for x in range(int(x0 + bw), int(x0) - 1, -8)]
        d.polygon(pts, fill=col)
    d.line([(x, surf(x)) for x in range(int(x0), int(x0 + bw) + 1, 6)], fill=(200, 140, 120), width=5)
    rnd = random.Random(7)
    for k in range(int(26 * p) + 2):  # sợi collagen mọc
        y = top + 110 + rnd.random() * 200; xa = x0 + rnd.random() * (bw - 200); ln = 120 + rnd.random() * 160
        pts = [(xa + s, y + 10 * math.sin(s / 18 + k)) for s in range(0, int(ln * min(1, p * 1.6)), 6)]
        if len(pts) > 1:
            d.line(pts, fill=(255, 248, 235), width=4)
    for k in range(90):  # hạt HA lan từ trên xuống, toả ra
        st = rnd.random() * 0.5; prog = max(0, min(1, (p - st) / 0.5))
        if prog <= 0:
            continue
        xs = x0 + 200 + rnd.random() * (bw - 400); xe = x0 + rnd.random() * bw; ye = top + 90 + rnd.random() * 230
        x = xs + (xe - xs) * ease(prog); y = top - 160 + (ye - top + 160) * ease(prog); r = 9 + 6 * math.sin(lt * 6 + k)
        d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], fill=(150, 200, 255, 90)); d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 175, 245))
    labs = ["HA collagen restores volume", "Firmer, smoother skin", "Younger-looking glow"]
    for k, lab in enumerate(labs):
        s0 = 0.15 + k * 0.27
        if p > s0:
            pl = pill(lab, SANS(46), 780, min(1, (p - s0) / 0.12)); im.alpha_composite(pl, (150, 1600 + k * 105))
    return im


def main(cfg_path, out):
    C = json.load(open(cfg_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(cfg_path))
    P = lambda v: os.path.join(base, v)
    tmp = os.path.join(base, "_dung2"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    S = Src(P(C["nguon"]), tmp); fr = os.path.join(tmp, "f"); os.makedirs(fr)
    logo = Image.open(LOGO).convert("RGBA"); logo = logo.resize((150, int(150 * logo.height / logo.width)))
    tb0, tb1 = C["truoc"]; ta0, ta1 = C["sau"]; U = C["uu_dai"]; globals()["SERVICE"] = U["dich_vu"].title().upper()
    vo = [3.0, 4.0, 8.0, 2.0, 2.5, 3.0, 6.5, 3.5]
    if C.get("giong_doan") and os.path.exists(P(C["giong_doan"])):
        vo = [x["giay"] for x in json.load(open(P(C["giong_doan"]), encoding="utf-8"))]
    n_cards = len(C["the"]); card_imgs = None; per = max(1.3, (vo[1] + 0.3) / n_cards)
    seg = [("hook", max(3.0, vo[0] + 0.5)), ("the", per * n_cards), ("glitch", 0.35), ("dongho", max(6.5, vo[2] + 0.5)),
           ("dep", max(2.4, vo[3] + 0.6)), ("ss", max(3.6, vo[4] + 0.8)), ("that", max(len(C["anh_that"]) * 1.05, vo[5] + 0.5)),
           ("qua", 3.8), ("km", max(4.6, vo[6] + 0.7 - 3.8)), ("cta", max(3.4, vo[7] + 0.6)), ("logo", 1.8)]
    st, t = {}, 0
    for k, dd in seg:
        st[k] = t; t += dd
    total = t; dur = dict(seg)
    vo_at = [st["hook"] + 0.3, st["the"] + 0.15, st["dongho"] + 0.2, st["dep"] + 0.2, st["ss"] + 0.3, st["that"] + 0.2, st["qua"] + 0.2, st["cta"] + 0.15]
    blur_b = S.at(tb0 + 0.5).filter(ImageFilter.GaussianBlur(30))
    reals = [Image.open(P(f)).convert("RGB") for f in C["anh_that"]]
    quas = [Image.open(P(f)).convert("RGB") for f in C.get("anh_qua", [])] or reals[:1]
    sparks = [(random.random() * W, random.random() * H, random.random() * 6 + 2, random.random() * 6.28) for _ in range(60)]

    def sparkle(im, tt, k=1.0):
        d = ImageDraw.Draw(im)
        for x, y, r, ph in sparks:
            a = (math.sin(tt * 4 + ph) + 1) / 2
            if a > 0.55:
                yy = (y - tt * 60) % H; rr = r * a * k
                d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=(255, 236, 180, int(200 * a)))

    order = [k for k, _ in seg]
    for i in range(int(total * FPS)):
        tt = i / FPS; k = [kk for kk in order if st[kk] <= tt][-1]; lt = tt - st[k]
        if k == "hook":  # full mặt, đẩy cận chậm
            z = 1 + 0.08 * ease(lt / dur[k]); f = S.at(chay(tb0, tb1 - .05, lt)); cw, ch = int(W / z), int(H / z)
            im = f.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H)).convert("RGBA")
            d = ImageDraw.Draw(im); a = ease(min(1, lt / 0.6))
            box = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
            text_c(bd, W / 2, 40, "Is this what you see", SERIF(78), (255, 255, 255, int(255 * a)), 4, (60, 35, 20, int(200 * a)))
            text_c(bd, W / 2, 140, "in the mirror?", SERIF(78), (255, 255, 255, int(255 * a)), 4, (60, 35, 20, int(200 * a)))
            im.alpha_composite(box, (0, 230))
        elif k == "the":  # chồng thẻ chậm
            im = blur_b.copy().convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, H), (40, 24, 12, 90)))
            for j in range(n_cards - 1, -1, -1):
                gs, x, y, w, h, lab = C["the"][j]
                if card_imgs is None:
                    card_imgs = [sharp_card(S, min(max(c[0], tb0 + 0.2), tb1 - 0.3), *c[1:5]) for c in C["the"]]  # thẻ vấn đề CHỈ lấy khung BEFORE
                card = rounded(card_imgs[j], 46); dd = ImageDraw.Draw(card)
                for yy in range(600, 900):
                    dd.line([(0, yy), (700, yy)], fill=NAU + (int(225 * (yy - 600) / 300),))
                off = j - max(0.0, lt - 0.55 * per) / per
                if j == n_cards - 1:
                    off = max(off, 0.0)
                if off < -1:
                    continue
                if off < 0:
                    pr = ease(-off); dx = -pr * 1100; rot = pr * 18
                else:
                    dx = off * 26; rot = -off * 4
                c2 = card.rotate(rot, expand=True, resample=Image.BICUBIC)
                if off < 0.5:
                    dl = ImageDraw.Draw(c2); f = SANS(60); dl.text((c2.width / 2 - dl.textlength(lab, font=f) / 2, c2.height - 150), lab, font=f, fill=(255, 255, 255))
                cs, pad = shadow(c2); im.alpha_composite(cs, (int((W - c2.width) / 2 + dx - pad), int(430 + off * 22 - pad)))
        elif k == "glitch":
            a = S.at(ta0); im = a.copy(); rnd = random.Random(i)
            for s in range(14):
                y0 = rnd.randint(0, H - 60); hh = rnd.randint(20, 90); im.paste(a.crop((0, y0, W, y0 + hh)), (rnd.randint(-120, 120), y0))
            r, g, b = im.split(); im = Image.merge("RGB", (ImageChops.offset(r, 12, 0), g, b)).convert("RGBA")
            im.alpha_composite(Image.new("RGBA", (W, H), (255, 236, 200, 60)))
        elif k == "dongho":
            im = skin_anim(lt, dur[k]); sparkle(im, tt, 0.6)
        elif k == "dep":  # chớp sáng → khách đẹp
            im = S.at(chay(ta0, ta1 - .05, 0.3 + lt)).convert("RGBA"); fl = max(0, 1 - lt / 0.45)
            if fl > 0:
                im.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 240, int(255 * fl))))
            pr = back(min(1, max(0, (lt - 0.3) / 0.5)))
            if pr > 0:
                g = gold_text("HELLO, NEW GLOW!", SERIF(76)); g = g.resize((max(1, int(g.width * pr)), max(1, int(g.height * pr))))
                im.alpha_composite(g, (int((W - g.width) / 2), 260))
            sparkle(im, tt, 1.3)
        elif k == "ss":  # before | after cùng khung
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            text_c(d, W / 2, 150, "SEE THE DIFFERENCE", SERIF(80), NAU)
            for j, src_t in enumerate([chay(tb0, tb1 - .1, 0.6 + lt), chay(ta0, ta1 - .05, 1.2 + lt)]):
                f = S.at(src_t); half = f.crop((W // 2 - 300 + (0 if j else -60), 300, W // 2 + 300 + (0 if j else -60), 300 + 1200)).resize((520, 1040))
                c = rounded(half, 30); ImageDraw.Draw(c).rounded_rectangle([0, 0, 519, 1039], 30, outline=VANG + (255,), width=6)
                im.alpha_composite(c, (12 + j * 536, 300))
                pl = pill("BEFORE" if j == 0 else "AFTER", SANS(44), 280, min(1, lt / 0.6), bg=(90, 70, 60) if j == 0 else NAU)
                im.alpha_composite(pl, (12 + j * 536 + 120, 1370))
            d.line([(W / 2, 300), (W / 2, 1340)], fill=VANG, width=6)
            text_c(d, W / 2, 1490, C.get("ghi_chu_ket_qua", ""), SANSI(32), (120, 90, 60))
        elif k == "that":  # ảnh thật MERAH
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            text_c(d, W / 2, 140, "LOVED BY", SANS(54), (120, 85, 50)); text_c(d, W / 2, 210, "MERAH CLIENTS", SERIF(96), NAU)
            each = dur[k] / len(reals); j = min(len(reals) - 1, int(lt / each)); q = (lt - j * each) / each
            if j > 0:  # ảnh trước trượt ra
                prev = fit_card(reals[j - 1], 960, 1300); pr = ease(min(1, q / 0.35))
                if pr < 1:
                    p2 = prev.rotate(-6 * pr, expand=True, resample=Image.BICUBIC); cs, pad = shadow(p2)
                    im.alpha_composite(cs, (int((W - p2.width) / 2 - pr * 1100 - pad), int(330 + (1300 - p2.height) / 2 - pad)))
            cur = fit_card(reals[j], 960, 1300); pr = back(min(1, q / 0.35)); s = 0.85 + 0.15 * pr
            c2 = cur.resize((max(1, int(cur.width * s)), max(1, int(cur.height * s)))).rotate(2 * (1 - pr), expand=True, resample=Image.BICUBIC); cs, pad = shadow(c2)
            im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(330 + (1300 - c2.height) / 2 - pad)))
            sparkle(im, tt, 0.7)
        elif k == "qua":  # quà Giáng sinh – ảnh khách trúng thưởng thật
            im = Image.new("RGBA", (W, H), (122, 22, 28, 255)); d = ImageDraw.Draw(im)
            g = gold_text("CHRISTMAS", SERIF(110)); im.alpha_composite(g, (int((W - g.width) / 2), 150))
            text_c(d, W / 2, 300, "LUCKY DRAW AT MERAH", SANS(58), (255, 240, 215))
            ph = fit_card(quas[int(lt / (dur[k] / len(quas))) % len(quas)], 980, 900, 44); pr = back(min(1, lt / 0.5)); s = 0.8 + 0.2 * pr
            c2 = ph.resize((max(1, int(ph.width * s)), max(1, int(ph.height * s)))); cs, pad = shadow(c2, 30, 18, 150)
            im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(430 + (900 - c2.height) / 2 - pad)))
            for n2, (txt, y0, t0) in enumerate([("₱10,000 CASH WINNER!", 1400, 0.5), ("Could you be next?", 1530, 1.0), ("Limited gifts only", 1660, 1.5)]):
                if lt > t0:
                    pl = pill(txt, SANS(56 if n2 < 2 else 46), 760, min(1, (lt - t0) / 0.4), bg=NAU)
                    im.alpha_composite(pl, (int((W - pl.width) / 2), y0))
            sparkle(im, tt, 1.6)
        elif k == "km":  # khuyến mãi
            im = S.at(chay(ta0, ta1 - .05, 1 + lt)).filter(ImageFilter.GaussianBlur(24)).convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, H), KEM + (150,)))
            pr = back(min(1, lt / 0.6)); cw, ch = int(900 * pr), int(1180 * pr)
            if cw > 10:
                card = Image.new("RGBA", (900, 1180), (0, 0, 0, 0)); d = ImageDraw.Draw(card)  # nền trong suốt, chỉ phần bo góc có màu
                d.rounded_rectangle([0, 0, 899, 1179], 48, fill=(255, 251, 244, 245), outline=VANG + (255,), width=8)
                fn = SANS(40); pw = d.textlength(U["nhan"], font=fn) + 80
                d.rounded_rectangle([450 - pw / 2, 50, 450 + pw / 2, 122], 36, fill=DO + (255,)); text_c(d, 450, 60, U["nhan"], fn, (255, 255, 255))
                text_c(d, 450, 165, U["dich_vu"].split(" ")[0], SERIF(110), NAU); text_c(d, 450, 290, " ".join(U["dich_vu"].split(" ")[1:]), SERIF(80), NAU)
                text_c(d, 450, 400, U["tu"], SANS(52), (110, 80, 50))
                g = gold_text(U["gia"], SANS(220)); card.alpha_composite(g, (int(450 - g.width / 2), 500))
                text_c(d, 450, 820, U["dong1"], SANS(54), DO); text_c(d, 450, 910, U["dong2"], SANS(50), NAU)
                d.rounded_rectangle([200, 1020, 700, 1110], 45, fill=NAU + (255,)); text_c(d, 450, 1035, "MESSAGE US", SANS(50), (255, 255, 255))
                c2 = card.resize((cw, ch)); cs, pad = shadow(c2, 30, 18, 140); im.alpha_composite(cs, (int((W - cw) / 2 - pad), int((H - ch) / 2 - pad + 40)))
            sparkle(im, tt, 1.2)
        elif k == "cta":
            im = S.at(ta1 - 0.1).convert("RGBA")
            pr = back(min(1, lt / 0.5)); stc = Image.new("RGBA", (860, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(stc)
            d.rounded_rectangle([0, 0, 859, 419], 60, fill=(255, 251, 244, 245), outline=VANG + (255,), width=8)
            text_c(d, 430, 50, C["cta"][0], SERIF(92 if os.name == "nt" else 78), DO)
            d.rounded_rectangle([110, 210, 750, 340], 65, fill=NAU + (255,)); text_c(d, 430, 232, C["cta"][1], SANS(66 if os.name == "nt" else 54), (255, 255, 255))
            bob = math.sin(lt * 5) * 8; s2 = stc.resize((max(1, int(860 * pr)), max(1, int(420 * pr)))); cs, pad = shadow(s2)
            im.alpha_composite(cs, (int((W - s2.width) / 2 - pad), int(260 + bob - pad)))
            if lt > 0.8:
                cl = (lt - 0.8) % 1.2; d = ImageDraw.Draw(im); x0, y0 = 720, 600 + bob; sc = 0.85 if cl < 0.15 else 1.0
                d.polygon([(x0 + px * sc, y0 + py * sc) for px, py in [(0, 0), (0, 70), (18, 54), (32, 84), (44, 78), (30, 49), (54, 49)]], fill=(255, 255, 255), outline=(30, 30, 30))
            sparkle(im, tt, 0.8)
        else:
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            big = Image.open(LOGO).convert("RGBA"); big = big.resize((420, int(420 * big.height / big.width)))
            pr = ease(min(1, lt / 0.5)); big.putalpha(big.split()[-1].point(lambda v: int(v * pr))); im.alpha_composite(big, ((W - big.width) // 2, 560))
            text_c(d, W / 2, 1060, "MERAH BEAUTY", SERIF(86), NAU); text_c(d, W / 2, 1180, "Makati City  ·  {{SO_DIEN_THOAI}}", SANS(44), (110, 80, 50))
            text_c(d, W / 2, 1270, "Message us to book", SANSI(46), DO)
        if k not in ("logo",):
            im.alpha_composite(logo, (W - logo.width - 40, 40))
        im = tho(im.convert("RGB"), lt, dur[k])
        im.convert("RGB").save(os.path.join(fr, f"{i:05d}.jpg"), quality=90)
    vid = os.path.join(tmp, "v.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "%05d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", vid], check=True)
    ins, flt, n, labs = ["-i", vid], [], 1, []
    if C.get("giong") and os.path.exists(P(C["giong"])):
        acc = 0
        for j, dd in enumerate(vo):
            ins += ["-ss", f"{acc:.3f}", "-t", f"{dd:.3f}", "-i", P(C["giong"])]; acc += dd
            ms = int(vo_at[j] * 1000); flt.append(f"[{n}:a]adelay={ms}|{ms},volume=1.15[v{j}]"); labs.append(f"[v{j}]"); n += 1
    # ---- HIỆU ỨNG ÂM THANH (sếp yêu cầu 10/11/2026: chỗ nào cần sống động thì có SFX) ----
    from sfx import lam_sfx
    ev = [(0.25, "pop", -9)]
    ev += [(st["the"] + 0.55 * per + j * per, "whoosh", -7) for j in range(n_cards - 1)] + [(st["the"] + 0.05, "pop", -10)]
    ev += [(st["glitch"], "glitch", -6), (st["dongho"] + 0.05, "swoosh_up", -9)]
    dd = dur["dongho"]; t_ = 0.0
    while t_ < dd * 0.85:
        ev.append((st["dongho"] + t_, "tick", -4)); t_ += 0.5
    for s0 in (0.15, 0.42, 0.69):  # 3 pill lợi ích hiện ra
        t_ = next((x / 100 for x in range(int(dd * 100)) if ease(min(1, (x / 100) / (dd * 0.85))) > s0), None)
        if t_ is not None:
            ev.append((st["dongho"] + t_, "pop", -8))
    ev += [(st["dongho"] + dd * 0.85, "ding", -8), (st["dep"] - 0.6, "riser", -10), (st["dep"], "impact", -3), (st["dep"] + 0.3, "sparkle", -9), (st["dep"] + 0.55, "ding", -9)]
    ev += [(st["ss"], "whoosh", -6), (st["ss"] + 0.35, "pop", -9), (st["ss"] + 0.5, "pop", -9)]
    each = dur["that"] / max(1, len(reals))
    ev += [(st["that"] + 0.05, "shutter", -6)] + [(st["that"] + j * each, "whoosh", -8) for j in range(1, len(reals))]
    ev += [(st["qua"] + 0.05, "swoosh_up", -9), (st["qua"] + 0.35, "cash", -3)] + [(st["qua"] + t0, "pop", -8) for t0 in (0.5, 1.0, 1.5)]
    ev += [(st["km"] + 0.1, "impact", -5), (st["km"] + 0.45, "ding", -6), (st["km"] + 0.6, "sparkle", -10)]
    ev += [(st["cta"] + 0.15, "pop", -6)] + [(st["cta"] + 0.8 + k * 1.2, "click", 0) for k in range(int(max(0, dur["cta"] - 0.8) / 1.2) + 1)]
    ev += [(st["logo"], "swoosh_up", -10), (st["logo"] + 0.4, "ding", -10)]
    sfx_wav = lam_sfx(ev, total, os.path.join(tmp, "sfx.wav"))
    beat_wav = lam_sfx([], total, os.path.join(tmp, "beat.wav"), nhip_bpm=168, nhip_tu=st["hook"], nhip_den=st["logo"], nhip_db=-6)
    half = total / 2
    subprocess.run([sys.executable, os.path.join(HERE, "nhac_giang_sinh.py"), f"{half:.2f}", "0-0.05:0"], cwd=tmp, check=True)
    nh = next((c for c in [os.path.join(tmp, "NHAC_GIANG_SINH.wav"), os.path.join(HERE, "NHAC_GIANG_SINH.wav")] if os.path.exists(c)), None)
    if nh:
        ins += ["-stream_loop", "2", "-i", nh, "-i", beat_wav, "-i", sfx_wav]
        vmix = "".join(labs) + f"amix=inputs={len(labs)}:normalize=0,asplit=2[vo][sc]"
        flt.append(vmix); flt.append(f"[{n}:a]volume=0.6[mz];[{n + 1}:a]volume=0.55[bt];[mz][bt]amix=inputs=2:normalize=0[m0]")
        flt.append("[m0][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[m]")
        flt.append(f"[{n + 2}:a]volume=0.9[fx]")
        labs = ["[vo]", "[m]", "[fx]"]
    flt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", out], check=True)
    print(f"Xong {out}: {total:.1f}s; " + ", ".join(f"{k}={st[k]:.1f}" for k, _ in seg))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
