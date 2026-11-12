"""Bộ hiệu ứng âm thanh (SFX) + nhịp trống tự tạo bằng code cho video quảng cáo MERAH (không bản quyền).
Dùng trong script dựng:  from sfx import lam_sfx
   lam_sfx([(giay, "whoosh", -6), (giay, "pop", -8), ...], tong_giay, "sfx.wav", nhip_bpm=112, nhip_tu=0.0, nhip_den=None)
Tên hiệu ứng: whoosh (lướt qua), swoosh_up (vút lên), pop (bong bóng), click, ding (ting), sparkle (lấp lánh), tick (tích tắc),
  glitch (rè điện), impact (thùm nhấn), cash (ka-ching tiền thưởng), shutter (chụp ảnh), riser (dâng lên trước cao trào).
Nhịp trống nhẹ (kick + clap + hi-hat) để video sôi động hơn, tự nhỏ đi khi có giọng đọc nhờ sidechain trong script dựng.
Chạy thử:  python sfx.py demo  -> SFX_DEMO.wav nghe lần lượt từng hiệu ứng."""
import sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def _t(d):
    return np.arange(int(SR * d)) / SR


def _env(n, a=0.005, r=0.2, curve=4.0):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    return att * np.exp(-curve * t / max(r, 1e-3))


def _bp(x, lo, hi):
    """Lọc dải thông đơn giản bằng FFT."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def _norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def whoosh(d=0.45, up=False):
    n = int(SR * d); t = np.arange(n) / SR; noise = rng.standard_normal(n)
    out = np.zeros(n); seg = 512
    for i in range(0, n, seg):  # quét dải lọc theo thời gian
        p = i / n; c = (300 + 4200 * (p if up else 1 - abs(2 * p - 1)))
        out[i:i + seg] = _bp(noise[i:i + seg] if len(noise[i:i + seg]) == seg else np.pad(noise[i:i + seg], (0, seg - len(noise[i:i + seg])))[:len(noise[i:i + seg])], c * 0.5, c * 1.6)[:len(out[i:i + seg])]
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** (1.5 if not up else 0.8)
    if up:
        env = (t / d) ** 2
    return _norm(out * env, 0.8)


def pop(d=0.12):
    t = _t(d); f = 900 * np.exp(-t * 30) + 300
    return _norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.002, 0.05), 0.85)


def click(d=0.05):
    t = _t(d); x = rng.standard_normal(len(t)) * _env(len(t), 0.0005, 0.008, 6)
    return _norm(_bp(x, 2000, 9000) + 0.4 * np.sin(2 * np.pi * 2200 * t) * _env(len(t), 0.0005, 0.01), 0.7)


def ding(d=1.2, f0=1568):
    t = _t(d); x = sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t * (3 + k)) for k, a in [(1, 1), (2.76, .35), (5.4, .15)])
    return _norm(x * _env(len(t), 0.002, d, 1.0), 0.8)


def sparkle(d=0.9):
    out = np.zeros(int(SR * d))
    for i in range(9):
        st = int(SR * (i * d / 11)); f = rng.choice([2093, 2349, 2637, 3136, 3520, 4186])
        tt = _t(0.35); s = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14)
        out[st:st + len(s)] += s[:len(out) - st] * (0.9 - i * 0.06)
    return _norm(out, 0.6)


def tick(d=0.06):
    t = _t(d); x = np.sin(2 * np.pi * 3200 * t) * _env(len(t), 0.0005, 0.012, 6) + 0.5 * rng.standard_normal(len(t)) * _env(len(t), 0.0003, 0.004, 6)
    return _norm(x, 0.6)


def glitch(d=0.35):
    t = _t(d); sq = np.sign(np.sin(2 * np.pi * (180 + 900 * rng.random(len(t)) * (np.arange(len(t)) % 1600 < 800)) * t))
    x = (sq * 0.5 + rng.standard_normal(len(t)) * 0.5) * (np.arange(len(t)) // 900 % 2)
    return _norm(_bp(x, 200, 6000) * _env(len(t), 0.001, d, 1.5), 0.7)


def impact(d=0.9):
    t = _t(d); f = 120 * np.exp(-t * 7) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.002, 0.5, 3)
    hit = _bp(rng.standard_normal(len(t)), 80, 3000) * _env(len(t), 0.001, 0.08, 6)
    return _norm(body + 0.5 * hit, 0.95)


def cash(d=1.1):
    out = np.zeros(int(SR * d)); c = click(0.04); out[:len(c)] += c
    b = ding(1.0, 2637) * 0.8 + ding(1.0, 3322) * 0.6; st = int(SR * 0.06); out[st:st + len(b)] += b[:len(out) - st]
    co = sparkle(0.6) * 0.5; st = int(SR * 0.12); out[st:st + len(co)] += co[:len(out) - st]
    return _norm(out, 0.85)


def shutter(d=0.18):
    a = click(0.04); b = click(0.05) * 0.8; out = np.zeros(int(SR * d)); out[:len(a)] += a; st = int(SR * 0.08); out[st:st + len(b)] += b
    return out


def riser(d=1.2):
    return _norm(whoosh(d, up=True) * 0.7 + np.sin(2 * np.pi * np.cumsum(300 + 900 * (_t(d) / d) ** 2) / SR) * (_t(d) / d) ** 2 * 0.3, 0.7)


SFX = {"whoosh": whoosh, "swoosh_up": lambda: whoosh(0.5, True), "pop": pop, "click": click, "ding": ding, "sparkle": sparkle,
       "tick": tick, "glitch": glitch, "impact": impact, "cash": cash, "shutter": shutter, "riser": riser}


def _kick():
    t = _t(0.35); f = 110 * np.exp(-t * 22) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.001, 0.25, 4)


def _clap():
    t = _t(0.22); x = _bp(rng.standard_normal(len(t)), 900, 5000)
    e = sum(_env(len(t), 0.001, 0.02, 6) * (np.arange(len(t)) >= int(SR * k)) for k in (0, .012, .024)) + _env(len(t), 0.001, 0.15, 4) * 0.6
    return x * e * 0.6


def _hat():
    t = _t(0.05); return _bp(rng.standard_normal(len(t)), 7000, 15000) * _env(len(t), 0.0005, 0.03, 6) * 0.35


def nhip(tong, bpm=112, tu=0.0, den=None):
    out = np.zeros(int(SR * tong)); den = tong if den is None else den; b = 60 / bpm; k, h, c = _kick(), _hat(), _clap()
    i = 0; tt = tu
    while tt < den:
        st = int(SR * tt)
        def add(x, g):
            e = min(len(out), st + len(x)); out[st:e] += x[:e - st] * g
        if i % 4 in (0, 2): add(k, 0.9)
        if i % 4 in (1, 3): add(c, 0.55)
        add(h, 0.5)
        st = int(SR * (tt + b / 2))
        if tt + b / 2 < den: add(h, 0.35)
        i += 1; tt += b
    return out


def lam_sfx(events, tong, out, nhip_bpm=None, nhip_tu=0.0, nhip_den=None, nhip_db=-14):
    mix = np.zeros(int(SR * tong) + SR)
    cache = {}
    for t0, name, db in events:
        if name not in cache:
            cache[name] = SFX[name]()
        x = cache[name] * 10 ** (db / 20); st = int(SR * max(0, t0)); e = min(len(mix), st + len(x)); mix[st:e] += x[:e - st]
    if nhip_bpm:
        mix[:int(SR * tong)] += nhip(tong, nhip_bpm, nhip_tu, nhip_den) * 10 ** (nhip_db / 20)
    mix = mix[:int(SR * tong)]
    pk = np.max(np.abs(mix)) or 1
    if pk > 0.98:
        mix = mix / pk * 0.98
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return out


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "demo":
    ev, t = [], 0.3
    for k in SFX:
        ev.append((t, k, -4)); t += 1.4
    lam_sfx(ev, t + 1, "SFX_DEMO.wav", nhip_bpm=112, nhip_tu=t - 5.6, nhip_db=-10)
    print("SFX_DEMO.wav", round(t + 1, 1), "giây:", ", ".join(SFX))
