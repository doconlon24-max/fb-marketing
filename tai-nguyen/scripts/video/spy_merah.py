"""CLONE video SPY thành video MERAH – sếp chốt 10/11/2026 (bản 2):
GIỮ NGUYÊN cảnh quay, thứ tự, nhịp, tốc độ gốc (1x). KHÔNG làm mờ / vá chữ cũ (vỡ nét) –
viết kịch bản chữ MERAH mới và đặt KHUNG CHỮ chuyên nghiệp CHE ĐÚNG vùng chữ cũ
(trượt vào + bóng + viền vàng + vệt sáng lướt); logo cũ che bằng huy hiệu logo MERAH.
Luôn có VOICE (giọng Mely, ElevenLabs) + nhạc thẩm mỹ (thư viện tai-nguyen/am-nhac/tham-my) + SFX.
Áo/logo spa khác trên người khách -> bản vá AI Higgsfield (`thay_ai`).
Cắt outro + khuyến mãi cũ, nối thẻ ưu đãi MERAH + outro MERAH.

Chạy:  python spy_merah.py <cau_hinh.json> <ra.mp4>
{
 "nguon": "spy.mp4",
 "giu": [0, 15.4],                                  # đoạn giữ lại (bỏ outro/khuyến mãi cũ)
 "che": [                                           # mỗi vùng chữ cũ -> 1 khung chữ MERAH phủ kín (x,y,w,h theo khung 1080x1920)
   {"t0": 0, "t1": 11.3, "vung": [210,1525,660,100], "text": "MAXFILL · Full-face refresh", "mau": "nau"}
 ],                                                 # mau: nau | kem | do ; vung tự nới 14px mỗi phía
 "nhan": [ {"t0":0.2,"t1":2.9,"x":540,"y":260,"text":"Tired, hollow-looking face?","mau":"nau"} ],   # chữ MERAH thêm
 "logo_che": [[x,y,w,h,t0,t1]],                     # logo/watermark cũ -> huy hiệu logo MERAH
 "thay_ai": [ {"file":"ai/ao_merah.mp4","x":0,"y":700,"t0":2.0,"t1":5.0} ],
 "loi": [ {"t": 0.3, "text": "Does your face look tired and hollow?"} ],   # VOICE bắt buộc, tiếng Anh, lời MERAH mới
 "nhac": "ten_bai.mp3" | null,                      # null = lấy bài trong tai-nguyen/am-nhac/tham-my (xoay vòng); "giang_sinh" = nhạc Noel tự soạn
 "nhan_mau": false,                                 # 11/11: mặc định KHÔNG in "Sample result" lên video
 "uu_dai": {"dich_vu":"MAXFILL","nhan":"CHRISTMAS DEAL","tu":"FROM ONLY","tu":"STARTING FROM ONLY","gia":"₱2,999","dong1":"40% OFF · until Nov 30","dong2":"Gifts up to ₱10,000"},
 "outro": null,                                   # mặc định không nối outro thương hiệu (phần cuối đã có ảnh thật + quà + ưu đãi + logo)
 "anh_that": null, "anh_qua": null, "kieu_nhac": "sang"   # null = ảnh thật/quà mặc định trong thuong-hieu/outro-qc
}
Chữ: 2–6 từ, đúng ý cảnh; KHÔNG viết "non-surgical / non-invasive / no needles / no botox".
Cuối cùng tự chạy kiem_tra_muot.py – GIẬT thì không được nộp."""
import hashlib, json, math, os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from dung_qc_hifu import W, H, FPS, LOGO, SERIF, SANS, NAU, VANG, KEM, DO, ease, back, rounded, shadow, text_c, gold_text, pill, tho
from sfx import lam_sfx

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
THU_VIEN_NHAC = os.path.join(ROOT, "am-nhac", "tham-my")
PAD = 6   # 11/11 sếp: khung chỉ vừa đủ – nới rất ít
MAUS = {"nau": ((120, 80, 44), (165, 116, 66), (255, 255, 255)), "kem": ((250, 243, 233), (238, 224, 204), NAU),
        "do": ((150, 22, 32), (196, 44, 56), (255, 255, 255))}


def run(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())


def wrap(d, s, f, maxw):
    out, line = [], ""
    for w in s.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not line:
            line = t
        else:
            out.append(line); line = w
    return out + ([line] if line else [])


def fit(s, w, h, start):
    if not s.strip():
        return SANS(int(max(18, start))), []  # khung rỗng (chữ vẽ riêng)
    d = ImageDraw.Draw(Image.new("L", (8, 8)))
    for sz in range(int(start), 17, -2):
        f = SANS(sz); ls = wrap(d, s, f, w)
        if len(ls) * sz * 1.18 <= h and max(d.textlength(l, font=f) for l in ls) <= w:
            return f, ls
    f = SANS(18); return f, wrap(d, s, f, w)


def khung_chu(w, h, text, mau="nau"):
    """Khung chữ MERAH: nền chuyển màu, viền vàng, thanh nhấn vàng, bóng đổ. Trả về (ảnh RGBA có lề bóng, lề, mặt nạ khung)."""
    c0, c1, tc = MAUS.get(mau, MAUS["nau"]); r = int(min(h / 2.2, 34)); m = 24
    g = Image.new("RGBA", (w, h)); gd = ImageDraw.Draw(g)
    for y in range(h):
        k = y / max(1, h - 1); gd.line([(0, y), (w, y)], fill=tuple(int(c0[i] * (1 - k) + c1[i] * k) for i in range(3)) + (255,))
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0)); card.paste(g, (0, 0), mask); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([1, 1, w - 2, h - 2], r, outline=VANG + (255,), width=3)
    bar = max(6, h // 12); cd.rounded_rectangle([14, h * .22, 14 + bar, h * .78], bar // 2, fill=VANG + (255,))
    f, ls = fit(text, w - 2 * (22 + bar), h - 14, min(h * .72, 132)); lh = f.size * 1.18; y0 = (h - lh * len(ls)) / 2 + f.size * .06
    for i, l in enumerate(ls):
        tw = cd.textlength(l, font=f); cd.text((w / 2 + bar / 2 - tw / 2, y0 + i * lh), l, font=f, fill=tc)
    out = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([m, m + 8, m + w, m + h + 8], r, fill=(30, 15, 5, 120))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); out.alpha_composite(card, (m, m))
    return out, m, mask


def huy_hieu_logo(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], int(min(w, h) / 2.4), fill=(250, 243, 233, 245), outline=VANG + (255,), width=3)
    lg = Image.open(LOGO).convert("RGBA"); k = min((w - 20) / lg.width, (h - 14) / lg.height)
    lg = lg.resize((max(1, int(lg.width * k)), max(1, int(lg.height * k))), Image.LANCZOS)
    im.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2)); return im


def p2in(x): return max(0.0, min(1.0, x)) ** 2
def p3in(x): return max(0.0, min(1.0, x)) ** 3
def p2out(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 2
def expo_out(x): x = max(0.0, min(1.0, x)); return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)


def zoom_mo(im, sc=1.0, blur=0.0):
    """Phóng/thu cả khung quanh tâm + làm mờ ống kính. sc<1: nền là chính khung phóng to mờ (không viền đen)."""
    im = im.convert("RGB")
    if sc > 1.001:
        cw, ch = W / sc, H / sc; x0, y0 = (W - cw) / 2, (H - ch) / 2
        im = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
    elif sc < .999:
        bg = im.resize((W // 4, H // 4)).filter(ImageFilter.GaussianBlur(8)).resize((W, H), Image.BICUBIC)
        fg = im.resize((int(W * sc), int(H * sc)), Image.BICUBIC); bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2)); im = bg
    if blur > .3:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im


ZT_RA, ZT_VAO = .2, .5   # zoom-through: ra 0.2s (1->1.2, mờ 0->10, power3.in) | vào 0.5s (0.85->1, mờ 10->0, expo.out)


def zt_ra(im, con_lai):
    """Cuối cảnh: lao về phía camera trước mối nối."""
    if con_lai >= ZT_RA:
        return im
    q = p3in(1 - con_lai / ZT_RA); return zoom_mo(im, 1 + .2 * q, 10 * q)


def zt_vao(im, da_qua):
    """Đầu cảnh: tiếp tục lớn dần vào mặt phẳng nét (cùng chiều Z với cảnh trước)."""
    if da_qua >= ZT_VAO:
        return im
    q = expo_out(da_qua / ZT_VAO); return zoom_mo(im, .85 + .15 * q, 10 * (1 - q))


def chu_thac(text, lt, y, co=64, mau="nau"):
    """Waterfall entry: từng chữ trồi từ dưới lên (40px, expo.out 0.45s), cách nhau 0.07s, trên 1 khung MERAH. Trả về ảnh RGBA cỡ khung hình."""
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); f = SANS(co); d = ImageDraw.Draw(out)
    words = text.split(); gap = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]
    tw = sum(ws) + gap * (len(words) - 1); bw, bh = int(tw + 120), int(co * 1.9)
    q0 = expo_out(lt / .35)
    if q0 > 0:
        img, m, _ = khung_chu(bw, bh, " ", mau); sc = .9 + .1 * q0
        img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc)))); img.putalpha(img.getchannel("A").point(lambda v: int(v * q0)))
        out.alpha_composite(img, (int(W / 2 - img.width / 2), int(y + bh / 2 - img.height / 2)))
    x = W / 2 - tw / 2; tc = MAUS.get(mau, MAUS["nau"])[2]
    for j, w in enumerate(words):
        q = expo_out((lt - .12 - j * .07) / .45)
        if q > 0:
            lay = Image.new("RGBA", (int(ws[j]) + 8, int(co * 1.4)), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((2, 0), w, font=f, fill=tc + (255,))
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * q)))
            out.alpha_composite(lay, (int(x), int(y + (bh - co * 1.2) / 2 + 40 * (1 - q))))
        x += ws[j] + gap
    return out


class Lop:
    """1 lớp chữ/khung có hoạt hình: trượt vào 0.35s (nảy nhẹ), vệt sáng lướt qua, mờ ra 0.2s."""
    def __init__(self, img, x, y, t0, t1, shine_mask=None, m=0, vao=True):
        self.img, self.x, self.y, self.t0, self.t1, self.m, self.vao, self.sm = img, x, y, t0, t1, m, vao, shine_mask; self.goc = False

    def ve(self, im, t):
        if t < self.t0 or t > self.t1:
            return
        a = t - self.t0; b = self.t1 - t
        p = min(1, a / .35) if self.vao else 1; al = min(p * 1.4, 1, b / .2 if b < .2 else 1)
        if al <= 0:
            return
        layer = self.img
        if self.sm is not None and .35 < a < 1.0:
            layer = layer.copy(); w, h = self.sm.size; s = (a - .35) / .65
            band = Image.new("L", (w, h), 0); cx = -w * .3 + s * w * 1.6
            ImageDraw.Draw(band).polygon([(cx, 0), (cx + 70, 0), (cx + 20, h), (cx - 50, h)], fill=110)
            band = ImageChops.multiply(band.filter(ImageFilter.GaussianBlur(8)), self.sm)
            white = Image.new("RGBA", (w, h), (255, 255, 255, 0)); white.putalpha(band)
            layer.alpha_composite(white, (self.m, self.m))
        dy = int((1 - expo_out(a / .45)) * 40) if self.vao else 0  # waterfall entry: trồi từ dưới lên
        if al < 1:
            layer = layer.copy(); layer.putalpha(layer.getchannel("A").point(lambda v: int(v * al)))
        im.alpha_composite(layer, (self.x, self.y + dy))


_NET = {}
def net_nhat(S, s0, s1):
    """Khung nét nhất trong [s0, s1] (độ nét cạnh) – dùng làm ảnh tĩnh thay cho quay chậm."""
    k = (round(s0, 3), round(s1, 3))
    if k not in _NET:
        from PIL import ImageStat
        n = max(2, int((s1 - s0) * 10)); ts = [s0 + (s1 - s0) * i / n for i in range(n + 1)]
        _NET[k] = max(ts, key=lambda t: ImageStat.Stat(S.at(t).convert("L").resize((270, 480)).filter(ImageFilter.FIND_EDGES)).var[0])
    return _NET[k]


LOGO_DIR = os.path.join(ROOT, "thuong-hieu", "logo")
def logo_tach_nen(mau, rong=240):
    lg = Image.open(os.path.join(LOGO_DIR, f"LOGO_MERAH_{mau}_tach_nen.png")).convert("RGBA")
    lg = lg.resize((rong, int(rong * lg.height / lg.width)), Image.LANCZOS)
    if mau != "kem": return lg
    m = 12; out = Image.new("RGBA", (lg.width + 2 * m, lg.height + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.paste((30, 15, 5, 150), (m, m + 2), lg.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5))); out.alpha_composite(lg, (m, m)); return out


def lop_tu_cfg(C, L):
    lops = []
    for c in C.get("che", []):
        x, y, w, h = c["vung"]; x, y, w, h = x - PAD, y - PAD, w + 2 * PAD, h + 2 * PAD
        img, m, mask = khung_chu(w, h, c["text"], c.get("mau", "nau")); t0 = c.get("t0", 0); t1 = c.get("t1", L)
        vao = t0 >= .35  # phủ kín TRƯỚC khi chữ cũ hiện: vào sớm 0.35s, ra muộn 0.2s
        lops.append(Lop(img, x - m, y - m, max(0, t0 - .35) if vao else 0, min(L, t1 + .2), mask, m, vao)); lops[-1].goc = True
    for c in C.get("nhan", []):
        d = ImageDraw.Draw(Image.new("L", (8, 8))); f = SANS(int(c.get("co", 64))); tw = d.textlength(c["text"], font=f)
        w, h = int(min(W - 80, tw + 76)), int(f.size * 1.55)
        img, m, mask = khung_chu(w, h, c["text"], c.get("mau", "nau"))
        yy = int(c.get("y", 1440)); xx = int(c.get("x", W // 2) - w / 2)   # mặc định vùng ngực – không đè mặt
        if C.get("logo_goc", True) and yy < 320 and xx < 300: yy = 320   # né logo góc trái trên
        lops.append(Lop(img, xx - m, yy - m, c.get("t0", 0), c.get("t1", L), mask, m, True))
    for v in C.get("logo_che", []):
        x, y, w, h = v[:4]; t0, t1 = (v[4], v[5]) if len(v) >= 6 else (0, L)
        lops.append(Lop(huy_hieu_logo(w + 2 * PAD, h + 2 * PAD), x - PAD, y - PAD, t0, t1, None, 0, False)); lops[-1].goc = True
    if C.get("logo_goc", True):   # 11/11 sếp: logo MERAH tách nền, góc TRÁI TRÊN, to hơn – video nào cũng có
        lg = logo_tach_nen(C.get("_logo_mau", "kem")); off = 12 if C.get("_logo_mau", "kem") == "kem" else 0
        lops.append(Lop(lg, 40 - off, 176 - off, 0, L, None, 0, False))
    if C.get("nhan_mau", False):   # 11/11 sếp: bỏ chữ "Sample result" trên video (ghi trong caption)
        img = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
        text_c(ImageDraw.Draw(img), W // 2, 8, "Sample result · Results may vary", SANS(32), (255, 255, 255), 4, (60, 35, 20))
        lops.append(Lop(img, 0, 1820, 0, L, None, 0, False))
    return lops


OUTRO_DIR = os.path.join(ROOT, "thuong-hieu", "outro-qc")
ANH_THAT = ["1_checkin_anh.jpg", "2_phone.webp", "4_chat.png", "5_ba.png", "6_ba.png", "7_ba.png"]   # ảnh THẬT của MERAH
ANH_QUA = ["qua_10k.jpg"]                                                                          # khách thật trúng ₱10,000


def fit_card(img, w, h, r=40):
    im = img.convert("RGB"); k = min(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    c = rounded(im, r); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], r, outline=VANG + (255,), width=4); return c


def sparkle(im, t, k=1.0):
    d = ImageDraw.Draw(im)
    for j in range(int(14 * k)):
        x = (j * 197 + 60) % W; y = (j * 331 + t * 90 * (1 + j % 3)) % H; a = .5 + .5 * math.sin(t * 5 + j)
        if a > .55:
            rr = 4 + (j % 4) * 2 * a; d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 236, 180, int(200 * a)))


def tho_troi(im, lt, amp=.05):
    """Zoom nhẹ + trôi ngang/dọc dạng sin (±8px) – luôn chuyển động, chữ không bị cắt."""
    z = 1.03 + amp * 0.4 * lt; cw, ch = W / z, H / z
    x0 = (W - cw) / 2 + 8 * math.sin(lt * 4.1); y0 = (H - ch) / 2 + 8 * math.cos(lt * 3.3)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))


def doan_cuoi(U, path, anh_that=None, anh_qua=None):
    """Phần cuối MERAH (sếp yêu cầu 10/11): (1) ảnh THẬT – feedback khách + before/after khách MERAH,
    (2) khách thật trúng ₱10,000, (3) thẻ ưu đãi – giá ghi rõ 'CHỈ TỪ' (STARTING FROM), logo + nút nhắn tin. Trả về {đoạn: giây bắt đầu}."""
    reals = [Image.open(f if os.path.isabs(f) else os.path.join(OUTRO_DIR, f)).convert("RGB") for f in (anh_that or ANH_THAT)]
    quas = [Image.open(f if os.path.isabs(f) else os.path.join(OUTRO_DIR, f)).convert("RGB") for f in (anh_qua or ANH_QUA)]
    seg = [("that", .95 * len(reals)), ("qua", 3.4), ("km", 4.4)]; st, t = {}, 0
    for k, dd in seg:
        st[k] = t; t += dd
    total, dur = t, dict(seg)
    bg0 = Image.open(os.path.join(OUTRO_DIR, "1_checkin_anh.jpg")).convert("RGB")
    k0 = max(W / bg0.width, H / bg0.height); bg0 = bg0.resize((int(bg0.width * k0) + 1, int(bg0.height * k0) + 1), Image.LANCZOS)
    bg0 = bg0.crop(((bg0.width - W) // 2, (bg0.height - H) // 2, (bg0.width - W) // 2 + W, (bg0.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(14))
    bg0 = Image.blend(bg0, Image.new("RGB", (W, H), KEM), .35)
    logo = Image.open(LOGO).convert("RGBA"); logo = logo.resize((230, int(230 * logo.height / logo.width)))
    fr = tempfile.mkdtemp()
    for i in range(int(total * FPS)):
        tt = i / FPS; k = [kk for kk, _ in seg if st[kk] <= tt][-1]; lt = tt - st[k]
        if k == "that":
            im = Image.new("RGBA", (W, H), KEM + (255,)); d = ImageDraw.Draw(im)
            text_c(d, W / 2, 130, "REAL RESULTS · REAL CLIENTS", SANS(48), (120, 85, 50)); text_c(d, W / 2, 200, "LOVED AT MERAH", SERIF(96), NAU)
            each = dur[k] / len(reals); j = min(len(reals) - 1, int(lt / each)); q = (lt - j * each) / each
            if j > 0:
                prev = fit_card(reals[j - 1], 960, 1300); pr = ease(min(1, q / .35))
                if pr < 1:
                    p2 = prev.rotate(-6 * pr, expand=True, resample=Image.BICUBIC); cs, pad = shadow(p2)
                    im.alpha_composite(cs, (int((W - p2.width) / 2 - pr * 1100 - pad), int(340 + (1300 - p2.height) / 2 - pad)))
            cur = fit_card(reals[j], 960, 1300); pr = back(min(1, q / .35)); sc = .85 + .15 * pr
            c2 = cur.resize((max(1, int(cur.width * sc)), max(1, int(cur.height * sc)))).rotate(2 * (1 - pr), expand=True, resample=Image.BICUBIC); cs, pad = shadow(c2)
            im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(340 + (1300 - c2.height) / 2 - pad)))
            text_c(d, W / 2, 1720, "Actual MERAH clients · Results may vary", SANS(34), (120, 85, 50))
            sparkle(im, tt, .7)
        elif k == "qua":
            im = Image.new("RGBA", (W, H), (122, 22, 28, 255)); d = ImageDraw.Draw(im)
            g = gold_text("CHRISTMAS", SERIF(110)); im.alpha_composite(g, (int((W - g.width) / 2), 150))
            text_c(d, W / 2, 300, "LUCKY DRAW AT MERAH", SANS(58), (255, 240, 215))
            ph = fit_card(quas[int(lt / (dur[k] / len(quas))) % len(quas)], 980, 900, 44); pr = back(min(1, lt / .5)); sc = .8 + .2 * pr
            c2 = ph.resize((max(1, int(ph.width * sc)), max(1, int(ph.height * sc)))); cs, pad = shadow(c2, 30, 18, 150)
            im.alpha_composite(cs, (int((W - c2.width) / 2 - pad), int(430 + (900 - c2.height) / 2 - pad)))
            for n2, (txt, y0, t0) in enumerate([("₱10,000 CASH WINNER!", 1400, .5), ("Could you be next?", 1530, 1.0), ("Limited gifts only", 1660, 1.5)]):
                if lt > t0:
                    pl = pill(txt, SANS(56 if n2 < 2 else 46), 760, min(1, (lt - t0) / .4), bg=NAU); im.alpha_composite(pl, (int((W - pl.width) / 2), y0))
            sparkle(im, tt, 1.6)
        else:
            im = bg0.copy().convert("RGBA"); im.alpha_composite(logo, ((W - logo.width) // 2, 170))
            pr = back(min(1, lt / .55))
            card = Image.new("RGBA", (900, 1060), (255, 255, 255, 0)); cd = ImageDraw.Draw(card)
            cd.rounded_rectangle([0, 0, 899, 1059], 60, fill=(255, 250, 244, 250), outline=VANG + (255,), width=6)
            text_c(cd, 450, 60, U.get("nhan", "CHRISTMAS DEAL"), SANS(52), DO)
            text_c(cd, 450, 145, U.get("dich_vu", "MAXFILL"), SERIF(110), NAU)
            text_c(cd, 450, 305, U.get("tu", "STARTING FROM ONLY"), SANS(50), NAU)
            gia = U.get("gia", "")
            g = gold_text(gia, SANS(180)); card.alpha_composite(g, (int(450 - g.width / 2), 370))
            text_c(cd, 450, 615, U.get("ghi_chu_gia", "*starting price · final price after consultation"), SANS(30), (120, 85, 50))
            text_c(cd, 450, 690, U.get("dong1", ""), SANS(50), DO); text_c(cd, 450, 775, U.get("dong2", ""), SANS(46), NAU)
            pulse = 1 + .04 * math.sin(lt * 6) if lt > .8 else 1
            cd.rounded_rectangle([180, 900, 720, 1000], 50, fill=NAU + (255,)); text_c(cd, 450, 918, "MESSAGE US NOW", SANS(48), (255, 255, 255))
            sc = max(.05, pr) * pulse; c2 = card.resize((max(1, int(900 * sc)), max(1, int(1060 * sc))), Image.BICUBIC)
            im.alpha_composite(c2, (int(W / 2 - c2.width / 2), int(1090 - c2.height / 2)))
            sparkle(im, tt, .8)
        im = tho(im.convert("RGB"), lt, dur[k], .05)  # đẩy cận đều (camera tiến), không lắc lư vô nghĩa – theo motion-doctrine
        im = zt_vao(im, lt)                      # đoạn nào cũng vào bằng zoom-through (đoạn đầu nối từ cảnh gốc)
        if k != seg[-1][0]:
            im = zt_ra(im, dur[k] - lt)          # ra trước mối nối sang đoạn sau
        im.save(os.path.join(fr, f"{i:05d}.jpg"), quality=92)
    run("-framerate", str(FPS), "-i", os.path.join(fr, "%05d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", path)
    shutil.rmtree(fr, ignore_errors=True); return st, dur, len(reals)


def dong_thoi_gian(C, L):
    """Dòng thời gian ra -> thời gian gốc. Có "truoc_sau": phát gốc tới hết đoạn BEFORE, rồi GIỮ đoạn BEFORE thêm `giu` giây
    (chạy tới-lùi 1x, khoanh từng vấn đề cho người xem thấy rõ), chuyển cảnh "30 MINUTES LATER", rồi phát tiếp từ đoạn AFTER."""
    ts = C.get("truoc_sau")
    if not ts:
        return [("goc", 0.0, L, L)], L
    a, b = ts["truoc"]; c = ts.get("sau", [b, L])[0]; giu = max(3.0, ts.get("giu", 4.0)); cv = ts.get("chuyen_giay", .8)
    seg = [("goc", 0.0, b, 0.0), ("giu", a, b, giu), ("chuyen", c, c + cv, cv), ("goc", c + cv, L, 0.0)]
    out, t = [], 0.0
    for k, s0, s1, d in seg:
        d = d or max(0.0, s1 - s0)
        if d > 0:
            out.append((k, s0, s1, d)); t += d
    return out, t


def van_de_lop(im, lt, ts):
    """Khoanh vùng vấn đề lúc khách CHƯA làm: vòng tròn vẽ dần + đường dẫn + nhãn, hiện lần lượt."""
    d = ImageDraw.Draw(im); vs = ts.get("van_de", [])
    if lt < .3:
        return
    tieu_de = ts.get("tieu_de", "BEFORE · WHERE IT SHOWS")
    pl = pill(tieu_de, SANS(46), 760, min(1, (lt - .3) / .4), bg=DO); im.alpha_composite(pl, ((W - pl.width) // 2, 150))
    step = max(.6, (ts.get("giu", 4.0) - 1.2) / max(1, len(vs)))
    for j, v in enumerate(vs):
        t0 = .5 + j * step
        if lt < t0:
            break
        p = min(1, (lt - t0) / .45); x, y, r = v["x"], v["y"], v.get("r", 90)
        d.arc([x - r, y - r, x + r, y + r], -90, -90 + 360 * ease(p), fill=(255, 255, 255, 255), width=7)
        d.arc([x - r - 4, y - r - 4, x + r + 4, y + r + 4], -90, -90 + 360 * ease(p), fill=DO + (255,), width=3)
        if p >= .6:
            BW, BH = 420, 76; phai = x >= W / 2  # nhãn nằm CÙNG PHÍA với vòng khoanh, không kéo đường cắt ngang mặt
            lx = v.get("lx", W - 40 - BW if phai else 40); ly = v.get("ly", y - BH - r * .6)
            q = min(1, (p - .6) / .4); ex, ey = (x + r * .7, y - r * .7) if phai else (x - r * .7, y - r * .7)
            tx, ty = (lx, ly + BH / 2) if phai else (lx + BW, ly + BH / 2)
            d.line([(ex, ey), (ex + (tx - ex) * q, ey + (ty - ey) * q)], fill=(255, 255, 255, 255), width=4)
            if q >= 1:
                img, m, _ = khung_chu(BW, BH, v["text"], "do"); im.alpha_composite(img, (int(lx - m), int(ly - m)))


def lam_giong(C, tmp):
    """VOICE bắt buộc: mỗi câu trong "loi" đọc riêng bằng giọng Mely, đặt đúng giây t. Trả về [(file, t, giây)]."""
    if os.environ.get("THU_KHONG_GIONG"):  # chỉ để thử hình trên máy không có khoá ElevenLabs – KHÔNG dùng cho bản nộp
        print("CẢNH BÁO: bản thử KHÔNG có voice"); return []
    import giong_doc as G
    loi = C.get("loi") or []
    if not loi:
        sys.exit("LỖI: thiếu \"loi\" (voice bắt buộc cho video SPY clone) – viết 3–6 câu tiếng Anh ngắn theo cảnh.")
    v = C.get("voice") or G.default_voice(); out = []
    for i, x in enumerate(loi):
        f = os.path.join(tmp, f"loi{i}.mp3"); G.tts(x["text"], f, v, C.get("toc_do", 1.05), "tuoi"); out.append((f, x["t"], G.dur(f)))
    for (f, t, d), nxt in zip(out, out[1:] + [None]):
        if nxt and t + d > nxt[1] + .05:
            print(f"CẢNH BÁO: câu ở {t}s dài {d:.1f}s đè câu sau ({nxt[1]}s) – rút ngắn lời hoặc dời t")
    return out


def chon_nhac(C, base, tmp, seed):
    """Nhạc nền: bài chỉ định -> thư viện nhạc thẩm mỹ (xoay vòng theo tên video) -> nhạc Noel tự soạn (dự phòng)."""
    n = C.get("nhac")
    if n and n != "giang_sinh":
        for p in (n if os.path.isabs(n) else os.path.join(base, n), os.path.join(THU_VIEN_NHAC, n)):
            if os.path.exists(p):
                return p
    if n != "giang_sinh" and os.path.isdir(THU_VIEN_NHAC):
        ds = sorted(f for f in os.listdir(THU_VIEN_NHAC) if f.lower().endswith((".mp3", ".wav", ".m4a")))
        if ds:
            return os.path.join(THU_VIEN_NHAC, ds[int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(ds)])
    if n != "giang_sinh":
        try:
            import nhac_ai
            return nhac_ai.tao(C.get("kieu_nhac", "sang"))
        except BaseException as e:  # không có khoá / lỗi mạng -> dự phòng
            print("CẢNH BÁO: chưa có nhạc thẩm mỹ (thư viện trống, nhạc AI lỗi:", e, ") – dùng tạm nhạc Noel tự soạn")
    subprocess.run([sys.executable, os.path.join(HERE, "nhac_giang_sinh.py"), "24", "0-0.05:0"], cwd=tmp, check=True)
    p = os.path.join(tmp, "NHAC_GIANG_SINH.wav"); return p if os.path.exists(p) else os.path.join(HERE, "NHAC_GIANG_SINH.wav")


def main(cfg_path, out):
    C = json.load(open(cfg_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(cfg_path))
    P = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    tmp = tempfile.mkdtemp(prefix="spymerah_")
    giong = lam_giong(C, tmp)  # làm trước: thiếu khoá/lỗi thì dừng sớm
    # 1) chuẩn hoá 1080x1920 30fps, giữ tốc độ gốc, bỏ âm thanh gốc, cắt đoạn giữ (+ bản vá AI)
    src_d = dur(P(C["nguon"])); g0, g1 = C.get("giu", [0, src_d]); g1 = min(g1, src_d); L = g1 - g0
    ins = ["-ss", f"{g0:.3f}", "-t", f"{L:.3f}", "-i", P(C["nguon"])]
    flt, last, n = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1[b]"], "b", 1
    for j, a in enumerate(C.get("thay_ai", [])):
        f = P(a["file"]); t0, t1 = a.get("t0", 0), a.get("t1", L)
        ins += (["-loop", "1", "-t", f"{L:.3f}", "-i", f] if f.lower().endswith((".png", ".jpg", ".webp")) else ["-itsoffset", f"{t0:.3f}", "-i", f])
        flt.append(f"[{last}][{n}:v]overlay={a.get('x', 0)}:{a.get('y', 0)}:enable='between(t,{t0},{t1})'[ai{j}]"); last = f"ai{j}"; n += 1
    goc = os.path.join(tmp, "goc.mp4")
    run(*ins, "-filter_complex", ";".join(flt), "-map", f"[{last}]", "-an", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-t", f"{L:.3f}", goc)
    # 2) dựng theo dòng thời gian: cảnh gốc 1x + giữ đoạn BEFORE khoanh vấn đề + chuyển cảnh + khung chữ MERAH
    from dung_qc_hifu import Src, chay
    S = Src(goc, tmp); tl, LO = dong_thoi_gian(C, L); ts = C.get("truoc_sau") or {}
    print("Dòng thời gian (giây ra):", ", ".join(f"{k} {sum(x[3] for x in tl[:i]):.1f}-{sum(x[3] for x in tl[:i + 1]):.1f}" for i, (k, *_r) in enumerate(tl)))
    try:
        from PIL import ImageStat
        vung = [S.at(L * k).convert("L").crop((40, 176, 300, 320)) for k in (.2, .5, .8)]
        C["_logo_mau"] = "nau" if sum(ImageStat.Stat(v).mean[0] for v in vung) / 3 > 165 else "kem"
    except Exception:
        C["_logo_mau"] = "kem"
    lops = lop_tu_cfg(C, LO); than = os.path.join(tmp, "than.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", than], stdin=subprocess.PIPE)
    st0 = 0.0; cst_vao = bool(C.get("uu_dai"))
    t_the = next((sum(x[3] for x in tl[:i]) + .3 for i, x in enumerate(tl) if x[0] == "chuyen"), None)
    for k, s0, s1, d in tl:
        for n in range(int(round(d * FPS))):
            lt = n / FPS; t = st0 + lt
            if k == "goc":
                sg = s0 + lt; im = S.at(sg).convert("RGBA")
            elif k == "giu":
                sg = net_nhat(S, s0, s1); im = tho(S.at(sg), lt, d, .04).convert("RGBA")  # 11/11 sếp: KHÔNG quay chậm – ảnh tĩnh nét nhất + zoom mượt
                vg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(vg).rectangle([0, 0, W, H], fill=(20, 8, 0, 40)); im.alpha_composite(vg)
                van_de_lop(im, lt, ts)
            else:  # rack-focus blur-cut: cùng khuôn mặt đổi trạng thái XẤU -> ĐẸP, cắt ở đỉnh mờ
                sg = s0 + lt; im = S.at(sg).convert("RGBA")
            for lp in lops:
                lp.ve(im, sg if lp.goc else t)
            if k == "giu" and d - lt < .3:  # mờ dần lên (power2.in) tới 12px, khung vẫn rõ màu – cắt ở đỉnh
                im = zoom_mo(im, 1.0, 12 * p2in(1 - (d - lt) / .3)).convert("RGBA")
            if k == "chuyen":
                im = zoom_mo(im, 1.0, 12 * (1 - p2out(lt / .35))).convert("RGBA")
            if t_the is not None and t_the <= t < t_the + 1.6:  # thẻ thời gian: chữ hiện dồn từ dưới lên, mờ ra 0.25s cuối
                lay = chu_thac(ts.get("chuyen", "30 MINUTES LATER"), t - t_the, 860, 64, "nau"); con = t_the + 1.6 - t
                if con < .25:
                    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * con / .25)))
                im.alpha_composite(lay)
            if cst_vao:
                im = zt_ra(im, LO - t).convert("RGBA")  # zoom-through ra ở mối nối sang phần cuối
            enc.stdin.write(im.convert("RGB").tobytes())
        st0 += d
    enc.stdin.close(); enc.wait(); L = LO
    # 3) thẻ ưu đãi MERAH + outro MERAH
    parts = [than]; t_ud = L; cst = None
    if C.get("uu_dai"):
        ud = os.path.join(tmp, "cuoi.mp4"); cst, cdur, nreal = doan_cuoi(C["uu_dai"], ud, C.get("anh_that"), C.get("anh_qua")); parts.append(ud)
    o = C.get("outro")
    if o:
        o = P(o) if os.path.exists(P(o)) else os.path.join(ROOT, "thuong-hieu", "video", o)
        if os.path.exists(o):
            parts.append(o)
    cin = sum((["-i", p] for p in parts), [])
    cc = "".join(f"[{k}:v]scale={W}:{H},fps={FPS},setsar=1[v{k}];" for k in range(len(parts))) + "".join(f"[v{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v]"
    vid = os.path.join(tmp, "vid.mp4"); run(*cin, "-filter_complex", cc, "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", vid)
    total = dur(vid)
    # 4) âm thanh: VOICE Mely + nhạc thẩm mỹ (tự giảm khi có giọng) + SFX
    ev = [(max(0, lp.t0) + .02, "swoosh_up" if lp.sm is not None else "pop", -11) for lp in lops if lp.vao]
    ev += [(a.get("t0", 0), "sparkle", -12) for a in C.get("thay_ai", [])]
    if cst:
        each = cdur["that"] / max(1, nreal); tq, tk = t_ud + cst["qua"], t_ud + cst["km"]
        ev += [(t_ud, "whoosh", -6), (t_ud + .05, "shutter", -7)] + [(t_ud + j * each, "whoosh", -9) for j in range(1, nreal)]
        ev += [(tq + .05, "swoosh_up", -9), (tq + .35, "cash", -4)] + [(tq + x, "pop", -8) for x in (.5, 1.0, 1.5)]
        ev += [(tk - .5, "riser", -10), (tk + .35, "impact", -5), (tk + .6, "ding", -8), (tk + .8, "sparkle", -10)]
    sfx_wav = lam_sfx(ev, total, os.path.join(tmp, "sfx.wav"))
    nh = chon_nhac(C, base, tmp, os.path.basename(out)); print("Nhạc:", os.path.basename(nh))
    ins = ["-i", vid, "-stream_loop", "-1", "-i", nh, "-i", sfx_wav]; flt, labs = [], []
    for j, (f, t, d) in enumerate(giong):
        ins += ["-i", f]; ms = int(t * 1000); flt.append(f"[{3 + j}:a]adelay={ms}|{ms},volume=1.2[g{j}]"); labs.append(f"[g{j}]")
    flt.append(f"[1:a]volume=0.6,afade=t=out:st={max(0, total - 1.2):.2f}:d=1.2[m0]")
    if labs:
        flt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,asplit=2[vo][sc]")
        flt.append("[m0][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[m]")
        flt.append("[2:a]volume=0.85[fx];[vo][m][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    else:
        flt.append("[2:a]volume=0.85[fx];[m0][fx]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(*ins, "-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Xong {out}: {total:.1f}s (giữ {L:.1f}s cảnh gốc, {len(giong)} câu voice, {len(lops)} lớp chữ + ưu đãi/outro MERAH)")
    import kiem_tra_muot
    return kiem_tra_muot.main(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
