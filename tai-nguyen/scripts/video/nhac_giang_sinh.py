"""Tự soạn nhạc nền «Jingle Bells» (bài dân gian 1857 — public domain) bằng code: chuông glockenspiel, chuông xe tuần lộc,
pad hợp âm, bass. Có sẵn giảm nhạc (ducking) khi có voice / tiếng khách. Ra NHAC_GIANG_SINH.wav đúng độ dài video.
python nhac_giang_sinh.py <tổng giây> "<a-b:dB,...>" """
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TONG = float(sys.argv[1]) if len(sys.argv) > 1 else 24.45
DUCK = sys.argv[2] if len(sys.argv) > 2 else "0-5.8:-14,5.8-16.35:-12,18.25-21.85:-14"

N = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(note, octv):
    return 440.0 * 2 ** ((N[note] + 12 * (octv + 1) - 69) / 12)


L1 = [("E", 1), ("E", 1), ("E", 2), ("E", 1), ("E", 1), ("E", 2), ("E", 1), ("G", 1), ("C", 1.5), ("D", .5), ("E", 4)]
L2 = [("F", 1), ("F", 1), ("F", 1.5), ("F", .5), ("F", 1), ("E", 1), ("E", 1), ("E", .5), ("E", .5),
      ("E", 1), ("D", 1), ("D", 1), ("E", 1), ("D", 2), ("G", 2)]
L4 = [("F", 1), ("F", 1), ("F", 1.5), ("F", .5), ("F", 1), ("E", 1), ("E", 1), ("E", .5), ("E", .5),
      ("G", 1), ("G", 1), ("F", 1), ("D", 1), ("C", 4)]
MEL = L1 + L2 + L1 + L4
HOP = ["C", "C", "C", "C", "F", "C", "D7", "G7", "C", "C", "C", "C", "F", "C", "G7", "C"]
CHORD = {"C": ["C", "E", "G"], "F": ["F", "A", "C"], "G7": ["G", "B", "F"], "D7": ["D", "F", "A"]}
BEATS = sum(d for _, d in MEL)               # 64 phách
BEAT = TONG / BEATS
n = int(TONG * SR) + SR
L = np.zeros(n)
R = np.zeros(n)
t_all = np.arange(n) / SR


def add(sig, at, pan=0.0, g=1.0):
    i = int(at * SR)
    j = min(n, i + len(sig))
    if j <= i:
        return
    L[i:j] += sig[:j - i] * g * (1 - pan) ** 0.5
    R[i:j] += sig[:j - i] * g * (1 + pan) ** 0.5 / 1.0


def chuong(f, dur):
    t = np.arange(int(min(dur + 1.2, 2.0) * SR)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
         + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 10))
    s[:120] *= np.linspace(0, 1, 120)
    return s


def pad(fs, dur):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 0.3) for f in fs)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.3).clip(0)
    return s * env / len(fs)


def bass(f, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s * np.exp(-t * 3.5) * np.minimum(1, t / 0.005)


rng = np.random.default_rng(3)


def leng_keng(dur=0.12, g=1.0):
    t = np.arange(int(dur * SR)) / SR
    x = rng.standard_normal(len(t))
    x = np.diff(np.concatenate([[0], x]))              # nhấn tần cao
    x = np.diff(np.concatenate([[0], x]))
    jingle = sum(np.sin(2 * np.pi * f * t) for f in (5200, 6300, 7400, 8800)) * 0.15
    return (x * 0.35 + jingle) * np.exp(-t * 38) * g


# giai điệu (chuông, quãng tám 6)
pos = 0.0
for note, d in MEL:
    add(chuong(hz(note, 6), d * BEAT), pos * BEAT, pan=0.15, g=0.32)
    pos += d
# hợp âm + bass theo ô nhịp (4 phách)
for k, h in enumerate(HOP):
    at = k * 4 * BEAT
    fs = [hz(x, 4) for x in CHORD[h]]
    add(pad(fs, 4 * BEAT), at, pan=-0.25, g=0.11)
    root = hz(CHORD[h][0], 2)
    add(bass(root, 2 * BEAT), at, g=0.30)
    add(bass(hz(CHORD[h][2], 2) if h != "G7" else hz("D", 3), 2 * BEAT), at + 2 * BEAT, g=0.24)
# chuông xe tuần lộc mỗi nửa phách
for k in range(int(BEATS * 2)):
    add(leng_keng(g=1.0 if k % 2 == 0 else 0.55), k * BEAT / 2, pan=0.35 * (1 if k % 4 < 2 else -1), g=0.16)

# vang nhẹ
ir = rng.standard_normal(int(0.9 * SR)) * np.exp(-np.arange(int(0.9 * SR)) / SR * 5.5)
ir /= np.abs(ir).sum() / 6


def vang(x):
    m = len(x) + len(ir)
    nfft = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x)]


L, R = L + 0.22 * vang(L), R + 0.22 * vang(np.roll(R, 400))
L, R = L[:int(TONG * SR)], R[:int(TONG * SR)]
t = np.arange(len(L)) / SR

# giảm nhạc khi có voice / tiếng khách (đường bao mượt 0.3s)
db = np.zeros(len(L))
for part in DUCK.split(","):
    rg, v = part.split(":")
    a, b = map(float, rg.split("-"))
    db[(t >= a) & (t < b)] = float(v)
k = int(0.3 * SR)
db = np.convolve(np.pad(db, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
g = 10 ** (db / 20)
g *= np.minimum(1, t / 0.4) * np.minimum(1, (TONG - t) / 1.2)   # vào nhẹ, kết mờ dần
L, R = L * g, R * g
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.85, R / peak * 0.85
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
import wave  # noqa: E402
out = os.path.join(HERE, "NHAC_GIANG_SINH.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", out, f"{TONG:.2f}s, {BEATS} phách, {60 / BEAT:.0f} bpm")
