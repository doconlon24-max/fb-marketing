"""Bộ dựng video quảng cáo MERAH – nhiều phong cách (sếp yêu cầu đa dạng hoá 10/11/2026).
python dung_qc_pc.py <cau_hinh.json> <ra.mp4>
  "phong_cach": "PC02" – Nỗi đau → Ưu đãi → Quà → Quy trình ✓ → Kết quả → Chứng thực → CTA (học từ Ngọc Dung xoá nhăn)
                "PC03" – Chồng thẻ → Glitch → Morph trước→sau → Thẻ ưu đãi collage → Lớp da CG → Pill quét → Chia 4 ô → Sticker khan hiếm (học từ Ngọc Dung HIFU)
Cấu hình chung giống dung_qc_v2.py: nguon, truoc[a,b] (đoạn BEFORE – khách đang xấu), sau[a,b] (đoạn AFTER), the[[giây,x,y,w,h,nhãn]...] (CHỈ trong đoạn before),
  vong[x,y,r], uu_dai{dich_vu,nhan,tu,gia,dong1,dong2}, loi_ich[...], cta[2 dòng], ghi_chu_ket_qua, giong, giong_doan (8 đoạn), anh_that[...], anh_qua[...],
  hook ["DÒNG 1","DÒNG 2"] (PC02), khuech_dai ["...","..."] (PC02), chung_thuc ["LIFTED","FIRMER","YOUNGER"] (PC02).
Giọng 8 đoạn khớp 8 phần: PC02 = hook, khuếch đại, ưu đãi, quà, quy trình, kết quả, chứng thực, CTA · PC03 = thẻ, morph, ưu đãi, lớp da, pill, chia ô+kết quả, quà, CTA.
Thẻ vấn đề tự kẹp vào đoạn before; nguồn đã làm nét (dung_qc_hifu.Src). Nhạc Giáng sinh + nhịp trống + SFX (sfx.py)."""
import json, math, os, random, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dung_qc_hifu import chay, tho, W, H, FPS, LOGO, SERIF, SANS, SANSI, NAU, VANG, KEM, DO, ease, back, rounded, shadow, text_c, gold_text, pill, Src
import dung_qc_v2 as V2
from sfx import lam_sfx

HERE = os.path.dirname(os.path.abspath(__file__))
XANH = (47, 157, 95)


def sparkle(im, tt, k=1.0, seed=3):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(55):
        x, y, r, ph = rnd.random() * W, rnd.random() * H, rnd.random() * 6 + 2, rnd.random() * 6.28
        a = (math.sin(tt * 4 + ph) + 1) / 2
        if a > 0.55:
            yy = (y - tt * 60) % H; rr = r * a * k; d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=(255, 236, 180, int(200 * a)))


def typewriter(d, txt, lt, speed, x, y, f, fill):
    n = max(0, min(len(txt), int(lt * speed))); text_c(d, x, y, txt[:n], f, fill)


def red_circle(d, cx, cy, r, prog):
    if prog <= 0:
        return
    d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], -90, -90 + 360 * min(1, prog), fill=(220, 40, 40), width=10)
    if prog > 0.8:  # mũi tên cong
        a = (prog - 0.8) / 0.2; x0, y0 = cx + r + 140, cy - r - 120
        d.line([(x0, y0), (x0 - 90 * a, y0 + 70 * a)], fill=(220, 40, 40), width=9)


def card_img(img, w, h, r=36, border=VANG):
    return V2.fit_card(img, w, h, r, border)


def cover(img, w, h):
    im = img.convert("RGB"); k = max(w / im.width, h / im.height); im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))


def main(cfg_path, out):
    C = json.load(open(cfg_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(cfg_path)); P = lambda v: os.path.join(base, v)
    PC = C.get("phong_cach", "PC02"); tmp = os.path.join(base, "_dungpc_" + PC); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    S = Src(P(C["nguon"]), tmp); fr = os.path.join(tmp, "f"); os.makedirs(fr)
    logo = Image.open(LOGO).convert("RGBA"); logo = logo.resize((150, int(150 * logo.height / logo.width)))
    tb0, tb1 = C["truoc"]; ta0, ta1 = C["sau"]; U = C["uu_dai"]; V2.SERVICE = U.get("dich_vu", "MAXFILL").upper()
    vo = [3.0, 3.0, 5.0, 3.0, 6.0, 3.0, 4.0, 3.5]
    if C.get("giong_doan") and os.path.exists(P(C["giong_doan"])):
        vo = [x["giay"] for x in json.load(open(P(C["giong_doan"]), encoding="utf-8"))][:8] + [3.0] * 8
    reals = [Image.open(P(f)).convert("RGB") for f in C.get("anh_that", [])]
    quas = [Image.open(P(f)).convert("RGB") for f in C.get("anh_qua", [])] or reals[:1]
    the = [[min(max(c[0], tb0 + 0.2), tb1 - 0.3)] + list(c[1:]) for c in C.get("the", [])]
    cards = [V2.sharp_card(S, *c[:5]) for c in the]
    lois = C.get("loi_ich", ["Instant volume", "Firmer, lifted skin", "Smoother lines", "Quick treatment"])
    blur_b = S.at(tb0 + 0.3).filter(ImageFilter.GaussianBlur(28))
    if PC == "PC02":
        seg = [("hook", max(3.0, vo[0] + .4)), ("amp", max(2.4, vo[1] + .3)), ("whip", .45), ("offer", max(5.0, vo[2] + .5)), ("gift", max(3.0, vo[3] + .4)),
               ("proc", max(5.5, vo[4] + .5)), ("result", max(3.0, vo[5] + .4)), ("proof", max(3.6, vo[6] + .4, len(reals) * .8)), ("cta", max(3.6, vo[7] + .6)), ("logo", 1.6)]
        vo_keys = ["hook", "amp", "offer", "gift", "proc", "result", "proof", "cta"]
    else:
        n = max(1, len(cards)); per = max(1.1, (vo[0] + .3) / n)
        seg = [("stack", per * n), ("glitch", .35), ("morph", max(3.0, vo[1] + .4)), ("offer", max(5.0, vo[2] + .5)), ("skin", max(4.0, vo[3] + .4)),
               ("pills", max(5.0, vo[4] + .4)), ("split", max(3.0, vo[5] + .3)), ("gift", max(3.0, vo[6] + .4)), ("cta", max(3.6, vo[7] + .6)), ("logo", 1.6)]
        vo_keys = ["stack", "morph", "offer", "skin", "pills", "split", "gift", "cta"]
    st, t = {}, 0
    for k, dd in seg:
        st[k] = t; t += dd
    total = t; dur = dict(seg); order = [k for k, _ in seg]
    ev = []  # SFX

    def offer_card(lt):
        card = Image.new("RGBA", (900, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, 899, 999], 48, fill=(255, 251, 244, 245), outline=VANG + (255,), width=8)
        fn = SANS(40); pw = d.textlength(U["nhan"], font=fn) + 80
        d.rounded_rectangle([450 - pw / 2, 46, 450 + pw / 2, 118], 36, fill=DO + (255,)); text_c(d, 450, 56, U["nhan"], fn, (255, 255, 255))
        text_c(d, 450, 150, U.get("dich_vu", "MAXFILL").upper(), SERIF(100), NAU); text_c(d, 450, 290, U["tu"], SANS(50), (110, 80, 50))
        pr = back(min(1, max(0, (lt - .35) / .5)))
        if pr > 0:
            g = gold_text(U["gia"], SANS(200)); g = g.resize((max(1, int(g.width * pr)), max(1, int(g.height * pr)))); card.alpha_composite(g, (int(450 - g.width / 2), int(470 - g.height / 2 + 10)))
        text_c(d, 450, 700, U["dong1"], SANS(50), DO); text_c(d, 450, 785, U["dong2"], SANS(46), NAU)
        d.rounded_rectangle([200, 880, 700, 960], 40, fill=NAU + (255,)); text_c(d, 450, 893, "MESSAGE US", SANS(46), (255, 255, 255))
        return card

    for i in range(int(total * FPS)):
        tt = i / FPS; k = [kk for kk in order if st[kk] <= tt][-1]; lt = tt - st[k]; D = dur[k]
        if k == "hook":  # mặt before, vòng đỏ tự vẽ, chữ đánh máy trên dải đỏ
            z = 1 + .06 * ease(lt / D); f = S.at(chay(tb0, tb1 - .1, lt)); cw, ch = int(W / z), int(H / z)
            im = f.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H)).convert("RGBA")
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70))); d = ImageDraw.Draw(im)
            vx, vy, vr = C.get("vong", [540, 1000, 140]); red_circle(d, vx, vy, vr, (lt - .3) / 1.0)
            hk = C.get("hook", ["TIRED, SAGGING SKIN?", "LOOKING OLDER THAN YOU ARE?"])
            d.rectangle([60, 250, W - 60, 400], fill=(150, 20, 28, 235)); typewriter(d, hk[0], lt, 18, W / 2, 285, SANS(64), (255, 255, 255))
            if lt > 1.4:
                typewriter(ImageDraw.Draw(im), hk[1], lt - 1.4, 22, W / 2, 430, SANS(50), (255, 255, 255))
        elif k == "amp":  # zoom chậm + chữ IN HOA hiện mờ
            z = 1.05 + .1 * ease(lt / D); f = S.at(chay(tb0, tb1 - .1, lt)); cw, ch = int(W / z), int(H / z)  # chỉ đoạn BEFORE
            im = f.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H)).convert("RGBA"); d = ImageDraw.Draw(im)
            ka = C.get("khuech_dai", ["DULL. TIRED.", "OLDER-LOOKING."]); j = 0 if lt < D / 2 else 1; a = int(255 * min(1, (lt - j * D / 2) / .4))
            text_c(d, W / 2, 1500, ka[j], SERIF(96), (255, 255, 255, a), 4, (40, 20, 10, a))
        elif k == "whip":
            a = S.at(tb1 - .2); b = S.at(ta0 + .3); p = lt / D; im = Image.blend(a, b, p).filter(ImageFilter.BoxBlur(int(40 * math.sin(math.pi * p)) + 1)).convert("RGBA")
        elif k in ("offer",) and PC == "PC02":  # trước »» sau + thẻ ưu đãi
            im = S.at(chay(ta0, ta1 - .05, .5 + lt)).filter(ImageFilter.GaussianBlur(20)).convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, H), KEM + (140,)))
            pr = back(min(1, lt / .5))
            for j, (src_t, lab) in enumerate([(tb0 + .4, "BEFORE"), (ta0 + .8, "AFTER")]):
                c = card_img(cover(S.at(src_t).crop((140, 300, 940, 1300)), 400, 500), 400, 500, 30)
                c = c.resize((max(1, int(400 * pr)), max(1, int(500 * pr)))); cs, pad = shadow(c); im.alpha_composite(cs, (int(60 + j * 560 + (400 - c.width) / 2 - pad), int(160 - pad)))
                if pr > .9:
                    pl = pill(lab, SANS(36), 220, min(1, (lt - .4) / .5), bg=(90, 70, 60) if j == 0 else NAU); im.alpha_composite(pl, (int(150 + j * 560), 610))
            d = ImageDraw.Draw(im); text_c(d, W / 2, 330, "»»", SANS(90), VANG)
            text_c(d, W / 2, 680, C.get("ghi_chu_ket_qua", ""), SANSI(28), (110, 80, 50))
            oc = offer_card(lt); oc = oc.resize((800, 889)); cs, pad = shadow(oc, 30, 18, 130); im.alpha_composite(cs, (int((W - 800) / 2 - pad), int(760 - pad)))
            sparkle(im, tt, 1.1)
        elif k == "offer":  # PC03: collage 4 ô nghiêng + tab dọc + giá vàng
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            tiles = [S.at(chay(tb0, tb1 - .1, .2 + q * .2 + lt)) if q % 2 == 0 else S.at(chay(ta0, ta1 - .05, .5 + q * .4 + lt)) for q in range(4)]
            for q, tl in enumerate(tiles):
                c = card_img(cover(tl, 380, 460), 380, 460, 26).rotate([-5, 4, 3, -4][q], expand=True, resample=Image.BICUBIC)
                pr = back(min(1, max(0, (lt - q * .12) / .45)))
                if pr > 0:
                    c = c.resize((max(1, int(c.width * pr)), max(1, int(c.height * pr)))); cs, pad = shadow(c); im.alpha_composite(cs, (int([70, 470, 70, 470][q] - pad), int([130, 160, 610, 640][q] - pad)))
            for q, tab in enumerate(C.get("tab", ["Cheeks", "Jawline", "Chin", "Lines"])):
                d.rounded_rectangle([900, 200 + q * 190, 1060, 360 + q * 190], 24, fill=NAU + (255,)); text_c(d, 980, 255 + q * 190, tab, SANS(32), (255, 255, 255))
            oc = offer_card(lt).resize((760, 844)); cs, pad = shadow(oc, 30, 18, 130); im.alpha_composite(cs, (int((W - 760) / 2 - pad), int(1060 - pad)))
            sparkle(im, tt, 1.2)
        elif k == "gift":  # quà Giáng sinh – ảnh khách trúng thưởng thật
            im = Image.new("RGBA", (W, H), (122, 22, 28, 255)); d = ImageDraw.Draw(im)
            g = gold_text("CHRISTMAS GIFTS", SERIF(96)); im.alpha_composite(g, (int((W - g.width) / 2), 150)); text_c(d, W / 2, 290, "LUCKY DRAW AT MERAH", SANS(54), (255, 240, 215))
            ph = card_img(quas[0], 960, 860, 40); pr = back(min(1, lt / .5)); c2 = ph.resize((max(1, int(ph.width * (.8 + .2 * pr))), max(1, int(ph.height * (.8 + .2 * pr)))))
            cs, pad = shadow(c2, 30, 18, 150); im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(400 + (860 - c2.height) / 2 - pad)))
            for n2, (txt, y0, t0) in enumerate([("₱10,000 CASH WINNER!", 1360, .4), ("Gifts up to ₱10,000", 1490, .9), ("Limited gifts only", 1620, 1.4)]):
                if lt > t0:
                    pl = pill(txt, SANS(54 if n2 < 2 else 44), 760, min(1, (lt - t0) / .4), bg=NAU); im.alpha_composite(pl, (int((W - pl.width) / 2), y0))
            sparkle(im, tt, 1.6)
        elif k == "proc":  # PC02: cảnh after chậm + lợi ích có dấu ✓ xanh
            im = S.at(chay(ta0, ta1 - .05, lt)).convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, 700), (0, 0, 0, 0)), (0, 0))
            grad = Image.new("RGBA", (W, 760), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
            for yy in range(760):
                gd.line([(0, yy), (W, yy)], fill=(30, 18, 10, int(190 * yy / 760)))
            im.alpha_composite(grad, (0, H - 760)); d = ImageDraw.Draw(im); step = D / max(1, len(lois))
            for q, lb in enumerate(lois):
                if lt > q * step:
                    a = min(1, (lt - q * step) / .35); y = 1280 + q * 110; r = 30 * back(a)
                    d.ellipse([150 - r, y + 32 - r, 150 + r, y + 32 + r], fill=XANH + (255,)); text_c(d, 150, y + 8, "✓", SANS(40), (255, 255, 255, int(255 * a)))
                    d.text((205, y), lb, font=SANS(58), fill=(255, 255, 255, int(255 * a)), stroke_width=3, stroke_fill=(30, 18, 10))
        elif k in ("result", "morph"):  # hoà tan trước → sau trên cùng khuôn mặt
            p = ease(min(1, max(0, (lt - .3) / (D * .6)))); a = S.at(chay(tb0, tb1 - .1, .2 + lt)); b = S.at(chay(ta0, ta1 - .05, .3 + lt))
            im = Image.blend(a, b, p).convert("RGBA"); d = ImageDraw.Draw(im)
            text_c(d, W / 2, 230, "BEFORE" if p < .5 else "AFTER", SERIF(90), (255, 255, 255), 4, (40, 20, 10))
            text_c(d, W / 2, H - 230, C.get("ghi_chu_ket_qua", ""), SANSI(32), (255, 255, 255), 2, (40, 20, 10))
            sparkle(im, tt, .8 * p)
        elif k == "proof":  # PC02: ảnh thật MERAH + chữ IN HOA từng ý
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im); text_c(d, W / 2, 140, "REAL MERAH CLIENTS", SERIF(84), NAU)
            if reals:
                each = D / len(reals); j = min(len(reals) - 1, int(lt / each)); q = (lt - j * each) / each
                c = card_img(reals[j], 960, 1180, 40); pr = back(min(1, q / .35)); c2 = c.resize((max(1, int(c.width * (.86 + .14 * pr))), max(1, int(c.height * (.86 + .14 * pr)))))
                cs, pad = shadow(c2); im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(300 + (1180 - c2.height) / 2 - pad)))
            ws = C.get("chung_thuc", ["LIFTED", "FIRMER", "YOUNGER-LOOKING"]); jj = min(len(ws) - 1, int(lt / (D / len(ws))))
            text_c(d, W / 2, 1560, "  ·  ".join(ws[:jj + 1]), SANS(60), DO)
        elif k == "stack":  # PC03: chồng thẻ 3D (chỉ khung before)
            im = blur_b.copy().convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, H), (40, 24, 12, 90)))
            for j in range(len(cards) - 1, -1, -1):
                card = rounded(cards[j], 46); dd = ImageDraw.Draw(card)
                for yy in range(600, 900):
                    dd.line([(0, yy), (700, yy)], fill=NAU + (int(225 * (yy - 600) / 300),))
                off = j - max(0.0, lt - .55 * per) / per
                if j == len(cards) - 1:
                    off = max(off, 0.0)
                if off < -1:
                    continue
                dx, rot = ((-ease(-off) * 1100, ease(-off) * 18) if off < 0 else (off * 26, -off * 4))
                c2 = card.rotate(rot, expand=True, resample=Image.BICUBIC)
                if off < .5:
                    dl = ImageDraw.Draw(c2); fn = SANS(60); lab = the[j][5]; dl.text((c2.width / 2 - dl.textlength(lab, font=fn) / 2, c2.height - 150), lab, font=fn, fill=(255, 255, 255))
                cs, pad = shadow(c2); im.alpha_composite(cs, (int((W - c2.width) / 2 + dx - pad), int(430 + off * 22 - pad)))
        elif k == "glitch":
            a = S.at(ta0); im = a.copy(); rnd = random.Random(i)
            for s in range(14):
                y0 = rnd.randint(0, H - 60); hh = rnd.randint(20, 90); im.paste(a.crop((0, y0, W, y0 + hh)), (rnd.randint(-120, 120), y0))
            r_, g_, b_ = im.split(); im = Image.merge("RGB", (ImageChops.offset(r_, 12, 0), g_, b_)).convert("RGBA")
        elif k == "skin":  # PC03: hoạt hình lớp da (đồng hồ + HA collagen)
            im = V2.skin_anim(lt, D); sparkle(im, tt, .6)
        elif k == "pills":  # PC03: cảnh after + pill quét từng ý, cắt cảnh theo ý
            step = D / max(1, len(lois)); q = min(len(lois) - 1, int(lt / step)); im = S.at(chay(ta0, ta1 - .05, .4 + lt)).convert("RGBA")
            pl = pill(lois[q].upper(), SANS(54), 900, min(1, (lt - q * step) / .5), bg=NAU); im.alpha_composite(pl, (int((W - 900) / 2), 1450))
        elif k == "split":  # PC03: chia 4 ô chạy cùng lúc + sticker giá
            im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
            for q in range(4):
                src_t = chay(ta0, ta1 - .05, .3 + q * .8 + lt) if q % 2 else chay(tb0, tb1 - .1, .2 + q * .2 + lt)
                im.paste(cover(S.at(src_t), W // 2 - 6, H // 2 - 6), ((q % 2) * (W // 2) + 3, (q // 2) * (H // 2) + 3))
            stc = Image.new("RGBA", (700, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(stc)
            d.rounded_rectangle([0, 0, 699, 329], 50, fill=(255, 251, 244, 245), outline=VANG + (255,), width=7); text_c(d, 350, 30, U.get("dich_vu", "").upper(), SERIF(64), NAU)
            g = gold_text(U["gia"], SANS(130)); stc.alpha_composite(g, (int(350 - g.width / 2), 120))
            pr = back(min(1, lt / .45)); s2 = stc.resize((max(1, int(700 * pr)), max(1, int(330 * pr)))); cs, pad = shadow(s2); im.alpha_composite(cs, (int((W - s2.width) / 2 - pad), int((H - s2.height) / 2 - pad)))
        elif k == "cta":
            im = S.at(ta1 - .2).convert("RGBA"); pr = back(min(1, lt / .5)); bob = math.sin(lt * 5) * 8
            stc = Image.new("RGBA", (860, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(stc)
            d.rounded_rectangle([0, 0, 859, 419], 60, fill=(255, 251, 244, 245), outline=VANG + (255,), width=8)
            text_c(d, 430, 50, C.get("cta", ["LIMITED GIFTS", "MESSAGE US NOW"])[0], SERIF(88), DO)
            d.rounded_rectangle([110, 210, 750, 340], 65, fill=NAU + (255,)); text_c(d, 430, 232, C.get("cta", ["", "MESSAGE US NOW"])[1], SANS(62), (255, 255, 255))
            s2 = stc.resize((max(1, int(860 * pr)), max(1, int(420 * pr)))); cs, pad = shadow(s2); im.alpha_composite(cs, (int((W - s2.width) / 2 - pad), int(260 + bob - pad)))
            if PC == "PC02":
                text_c(ImageDraw.Draw(im), W / 2, 740, "Free consultation", SANSI(52), (255, 255, 255), 3, (40, 20, 10))
            if lt > .8:
                cl = (lt - .8) % 1.2; d2 = ImageDraw.Draw(im); x0, y0 = 720, 600 + bob; sc = .85 if cl < .15 else 1.0
                d2.polygon([(x0 + px * sc, y0 + py * sc) for px, py in [(0, 0), (0, 70), (18, 54), (32, 84), (44, 78), (30, 49), (54, 49)]], fill=(255, 255, 255), outline=(30, 30, 30))
            sparkle(im, tt, .8)
        else:  # logo
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            big = Image.open(LOGO).convert("RGBA"); big = big.resize((420, int(420 * big.height / big.width))); pr = ease(min(1, lt / .5))
            big.putalpha(big.split()[-1].point(lambda v: int(v * pr))); im.alpha_composite(big, ((W - big.width) // 2, 560))
            text_c(d, W / 2, 1060, "MERAH BEAUTY", SERIF(86), NAU); text_c(d, W / 2, 1180, "Makati City  ·  {{SO_DIEN_THOAI}}", SANS(44), (110, 80, 50))
        if k != "logo":
            im.alpha_composite(logo, (W - logo.width - 40, 40))
        im = tho(im.convert("RGB"), lt, dur[k])
        im.convert("RGB").save(os.path.join(fr, f"{i:05d}.jpg"), quality=90)
    # SFX theo phong cách
    for k in order:
        s0 = st[k]
        ev += {"hook": [(s0 + .3, "pop", -8), (s0 + .6, "riser", -12)], "amp": [(s0, "whoosh", -8)], "whip": [(s0, "whoosh", -4)],
               "offer": [(s0 + .1, "pop", -6), (s0 + .45, "impact", -5), (s0 + .7, "ding", -6), (s0 + .8, "sparkle", -10)],
               "gift": [(s0 + .1, "swoosh_up", -9), (s0 + .35, "cash", -3), (s0 + .4, "pop", -8), (s0 + .9, "pop", -8)],
               "proc": [(s0 + q * dur[k] / max(1, len(lois)), "pop", -7) for q in range(len(lois))],
               "result": [(s0 + .2, "riser", -10), (s0 + dur[k] * .6, "sparkle", -8)], "morph": [(s0 + .2, "riser", -10), (s0 + dur[k] * .6, "sparkle", -8)],
               "proof": [(s0 + .05, "shutter", -6)], "stack": [(s0 + .55 * (dur[k] / max(1, len(cards))) + j * dur[k] / max(1, len(cards)), "whoosh", -7) for j in range(max(0, len(cards) - 1))],
               "glitch": [(s0, "glitch", -6)], "skin": [(s0 + q * .5, "tick", -4) for q in range(int(dur[k] * .85 / .5))],
               "pills": [(s0 + q * dur[k] / max(1, len(lois)), "whoosh", -9) for q in range(len(lois))], "split": [(s0, "impact", -5), (s0 + .4, "ding", -7)],
               "cta": [(s0 + .15, "pop", -6)] + [(s0 + .8 + q * 1.2, "click", 0) for q in range(int(max(0, dur[k] - .8) / 1.2) + 1)],
               "logo": [(s0, "swoosh_up", -10), (s0 + .4, "ding", -10)]}.get(k, [])
    sfx_wav = lam_sfx(ev, total, os.path.join(tmp, "sfx.wav"))
    beat_wav = lam_sfx([], total, os.path.join(tmp, "beat.wav"), nhip_bpm=168, nhip_tu=0, nhip_den=st["logo"], nhip_db=-6)
    vid = os.path.join(tmp, "v.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "%05d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", vid], check=True)
    ins, flt, n, labs = ["-i", vid], [], 1, []
    if C.get("giong") and os.path.exists(P(C["giong"])):
        acc = 0
        for j, kk in enumerate(vo_keys):
            dd = vo[j]; ins += ["-ss", f"{acc:.3f}", "-t", f"{dd:.3f}", "-i", P(C["giong"])]; acc += dd
            ms = int((st[kk] + .2) * 1000); flt.append(f"[{n}:a]adelay={ms}|{ms},volume=1.15[v{j}]"); labs.append(f"[v{j}]"); n += 1
    subprocess.run([sys.executable, os.path.join(HERE, "nhac_giang_sinh.py"), f"{total / 2:.2f}", "0-0.05:0"], cwd=tmp, check=True)
    nh = next((c for c in [os.path.join(tmp, "NHAC_GIANG_SINH.wav"), os.path.join(HERE, "NHAC_GIANG_SINH.wav")] if os.path.exists(c)), None)
    if nh and labs:
        ins += ["-stream_loop", "2", "-i", nh, "-i", beat_wav, "-i", sfx_wav]
        flt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,asplit=2[vo][sc]")
        flt.append(f"[{n}:a]volume=0.6[mz];[{n + 1}:a]volume=0.55[bt];[mz][bt]amix=inputs=2:normalize=0[m0]")
        flt.append("[m0][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[m]"); flt.append(f"[{n + 2}:a]volume=0.9[fx]"); labs = ["[vo]", "[m]", "[fx]"]
    flt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", out], check=True)
    print(f"Xong {out} ({PC}): {total:.1f}s; " + ", ".join(f"{k}={st[k]:.1f}" for k, _ in seg))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
