"""PC07 kịch bản "XẤU CHẠY" (sếp 16/11, QC-20261115-VD3 v2):
   video khách XẤU chạy 1x (hook) → DỪNG HÌNH khung cuối, khoanh + giữ cùng lúc các vấn đề thật → 3D collagen (cơ chế 30 phút)
   → LẬT 3D ảnh trước sang ảnh sau → so sánh BEFORE | AFTER → video khách SAU khi đẹp chạy 1x → khách thật → ưu đãi → CTA.
   Ảnh tĩnh CHỈ ở đoạn nêu vấn đề và so sánh; còn lại là video.
python build_pc07_xau_chay.py <hf_dir> <pc07_index.html> <cfg.json>
assets: v_hook.mp4 (video xấu, khung cuối = s_bef.png), s_bef.png, s_aft.png, v_aft.mp4 (video sau khi đẹp), s_aft_end.png (khung cuối v_aft),
        music.mp3, 5_ba/6_ba/7_ba.png, qua_10k.jpg, logo*.png, sfx/
voice 1 file 7 đoạn (+ _doan.json): hook, vấn đề, cơ chế, so sánh, sau khi đẹp, ưu đãi, CTA.
cfg: vo, doan, kick, hook, defs [{"lab":..,"t":giây trong đoạn 2,"o":[[x,y,r],..]}], aft_h, glow, mech_sub, mech_lbl, checks, svc, from, price, off, bef_pos
Dải đáy ≤ 15% (luật B2): pill/chữ đáy từ y≥1690, nền đáy cao 290px."""
import io, json, re, subprocess, sys
W, PC07, CF = sys.argv[1], sys.argv[2], sys.argv[3]
C = json.load(io.open(CF, encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", io.open(PC07, encoding="utf-8").read(), re.S).group(1)
doan = json.load(io.open(C["doan"], encoding="utf-8")); g = [x["giay"] for x in doan]
off = 0.0
for i, x in enumerate(g):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.3f}", "-t", f"{x:.3f}", "-i", C["vo"], "-c:a", "libmp3lame", "-b:a", "160k", f"{W}/assets/vo{i+1}.mp3"], check=True); off += x
def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{W}/assets/{f}"], capture_output=True, text=True).stdout)
r2 = lambda x: f"{x:.2f}"
HV, AV = dur("v_hook.mp4"), dur("v_aft.mp4")
s1 = 0.0; L1 = max(HV, g[0] + 0.3)
s2 = s1 + L1; L2 = g[1] + 0.5
s3 = s2 + L2; L3 = max(3.6, g[2] + 0.4)
s4 = s3 + L3; L4 = max(4.4, g[3] + 2.6)
s5 = s4 + L4; L5 = max(AV, g[4] + 0.2)
s6 = s5 + L5; L6 = 2.6
s7 = s6 + L6; L7 = g[5] + 0.4
s8 = s7 + L7; L8 = g[6] + 0.8
T = s8 + L8
defs = C["defs"]
def circ(i, j, x, y, r):
    dd = int(2 * 3.14159 * (r - 8)) + 1
    return (f'<svg id="r{i}-{j}" class="rc{i}" style="position:absolute; left:{x - r}px; top:{y - r}px; width:{2*r}px; height:{2*r}px" viewBox="0 0 {2*r} {2*r}">'
            f'<circle cx="{r}" cy="{r}" r="{r - 8}" fill="none" stroke="#e8cfa0" stroke-width="7" stroke-dasharray="{dd}" stroke-dashoffset="{dd}" stroke-linecap="round"/></svg>')
CIR = "".join(circ(i, j, *o) for i, d in enumerate(defs) for j, o in enumerate(d["o"]))
PILLS = "".join(f'<div id="p{i}" class="pill" style="position:relative; font-size:30px; padding:8px 18px"><span class="dot"></span>{d["lab"]}</div>' for i, d in enumerate(defs))
TRK = ""
for i, d in enumerate(defs):
    t0 = s2 + d["t"]
    TRK += f'tl.to(".rc{i} circle", {{ attr:{{ "stroke-dashoffset":0 }}, duration:0.45, ease:"power2.out" }}, {r2(t0 + 0.1)}); tl.fromTo("#p{i}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(t0 + 0.2)});\n'
html = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{css}
.top {{ position:absolute; left:70px; right:70px; top:170px; text-align:center; }}
.bot {{ position:absolute; left:40px; right:40px; top:1690px; text-align:center; }}
.sb {{ position:absolute; left:0; bottom:0; width:1080px; height:290px; background:linear-gradient(0deg, rgba(40,22,12,0.85) 0%, rgba(40,22,12,0.55) 60%, rgba(40,22,12,0) 100%); }}
.face {{ position:absolute; left:0; top:0; width:1080px; height:1920px; backface-visibility:hidden; -webkit-backface-visibility:hidden; }}
.face img {{ width:1080px; height:1920px; object-fit:cover; display:block; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{r2(T)}" data-width="1080" data-height="1920" style="background:#2a170d">
<div class="wrap" id="w-hook" style="z-index:1"><video class="clip full" src="assets/v_hook.mp4" muted playsinline data-start="0" data-duration="{r2(HV)}" data-track-index="1"></video></div>
<div class="wrap" id="w-bef" style="z-index:1; transform-origin:540px 960px"><img class="clip full" src="assets/s_bef.png" alt="" data-start="{r2(HV)}" data-duration="{r2(s3 - HV)}" data-track-index="1"></div>
<div class="wrap" id="w-aft" style="z-index:1"><video class="clip full" src="assets/v_aft.mp4" muted playsinline data-start="{r2(s5)}" data-duration="{r2(AV)}" data-track-index="1"></video></div>
<div class="wrap" id="w-aend" style="z-index:1; transform-origin:540px 900px"><img class="clip full" src="assets/s_aft_end.png" alt="" data-start="{r2(s5 + AV)}" data-duration="{r2(max(0.1, L5 - AV))}" data-track-index="1"></div>

<!-- S1 HOOK: video xấu chạy -->
<div id="s1" class="clip full" data-start="0" data-duration="{r2(L1)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:620px"></div>
  <div class="top"><div id="s1-k" class="kick">{C["kick"]}</div><div id="s1-a" class="big" style="margin-top:22px; font-size:82px">{C["hook"]}</div></div>
</div>
<!-- S2 DỪNG HÌNH – khoanh vấn đề, giữ cùng lúc -->
<div id="s2" class="clip full" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:420px"></div><div class="sb"></div>
  <div class="top" style="top:200px"><div class="kick">BEFORE · WHERE IT SHOWS</div></div>
  {CIR}
  <div class="bot"><div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">{PILLS}</div></div>
</div>
<!-- S3 CƠ CHẾ (giữ nguyên kiểu PC07) -->
<div id="s3" class="clip full" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 20%, #fbf5ec 0%, #f6eee4 50%, #efe3d3 100%)">
  <div class="mech-title"><div id="m-num" class="mech-num"><span>30</span><small>min</small></div><div id="m-sub" class="mech-sub">{C.get("mech_sub","MAXFILL · HA COLLAGEN")}</div></div>
  <div id="illus" class="illus"><svg width="900" height="560" viewBox="0 0 900 560"><defs>
    <linearGradient id="gDerm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2cdb4"/><stop offset="1" stop-color="#e3a98a"/></linearGradient>
    <linearGradient id="gEpi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8e2cf"/><stop offset="1" stop-color="#efcdb2"/></linearGradient>
    <radialGradient id="gDrop" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#fff6dd"/><stop offset="0.5" stop-color="#e8cfa0"/><stop offset="1" stop-color="#c9a46a"/></radialGradient></defs>
    <rect x="0" y="300" width="900" height="260" fill="url(#gDerm)"/>
    <path id="epi" d="M0 200 C 150 200, 300 200, 380 230 C 420 300, 480 300, 520 230 C 600 200, 750 200, 900 200 L 900 310 L 0 310 Z" fill="url(#gEpi)"/>
    <g stroke="#c98f6d" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.55"><path class="fib" d="M30 380 C 120 350, 200 410, 290 380 S 470 350, 560 380 S 760 410, 870 380"/><path class="fib" d="M30 440 C 140 410, 230 470, 330 440 S 520 410, 620 440 S 790 470, 870 440"/><path class="fib" d="M30 500 C 110 470, 210 530, 300 500 S 480 470, 580 500 S 770 530, 870 500"/></g>
    <g><circle class="drop" cx="420" cy="330" r="20" fill="url(#gDrop)"/><circle class="drop" cx="470" cy="350" r="16" fill="url(#gDrop)"/><circle class="drop" cx="380" cy="365" r="14" fill="url(#gDrop)"/><circle class="drop" cx="510" cy="320" r="13" fill="url(#gDrop)"/><circle class="drop" cx="450" cy="395" r="18" fill="url(#gDrop)"/><circle class="drop" cx="350" cy="330" r="11" fill="url(#gDrop)"/></g>
    <text id="lblVol" x="450" y="150" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="34" letter-spacing="4" fill="#8a5a32">{C.get("mech_lbl","LOST VOLUME")}</text></svg><div class="illus-tag">Illustration</div></div>
  <div class="checks">{"".join(f'<div id="ck{i+1}" class="check"><b>✓</b>{t}</div>' for i, t in enumerate(C.get("checks", ["FIRMER", "SMOOTHER", "YOUNGER-LOOKING"])))}</div>
</div>
<!-- S4 LẬT 3D trước → sau, rồi so sánh BEFORE | AFTER -->
<div id="s4" class="clip full" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="2" style="z-index:5; background:#2a170d; perspective:2200px" data-layout-allow-overflow>
  <div id="flip" style="position:absolute; left:0; top:0; width:1080px; height:1920px; transform-style:preserve-3d; transform-origin:540px 960px">
    <div class="face"><img src="assets/s_bef.png" alt=""></div>
    <div class="face" style="transform:rotateY(180deg)"><img src="assets/s_aft.png" alt=""></div>
  </div>
  <div id="cmp-bef" style="position:absolute; left:0; top:0; width:1080px; height:1920px; clip-path:inset(0px 1080px 0px 0px)"><img src="assets/s_bef.png" alt="" style="width:1080px; height:1920px; object-fit:cover; transform:translateX({C.get("bef_dx", 0)}px)"></div>
  <div id="ba-bar" class="ba-bar" style="left:-12px"></div>
  <div class="shade-top" style="height:380px"></div><div class="sb"></div>
  <div id="t-bef" class="tag" style="left:50px; top:230px; background:rgba(59,36,22,0.85); opacity:0">BEFORE</div>
  <div id="t-aft" class="tag" style="right:50px; top:230px; background:linear-gradient(90deg,#c9a46a,#e8cfa0); color:#3b2416; opacity:0">AFTER</div>
  <div class="bot" style="top:1700px"><div id="ba-h" class="big" style="font-size:70px">See the <em>difference</em></div></div>
</div>
<!-- S5 VIDEO SAU KHI ĐẸP chạy -->
<div id="s5" class="clip full" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="shade-top" style="height:520px"></div><div id="sweep" class="sweep"></div>
  <div class="top" style="top:190px"><div id="g-k" class="kick">{C.get("aft_k", "ONE MAXFILL SESSION · AFTER")}</div><div id="g-h" class="big" style="font-size:86px; margin-top:20px">{C.get("aft_h", "Sharper. <em>Younger.</em>")}</div></div>
  <div class="sb"></div>
  <div class="bot"><div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">
    {"".join(f'<div id="b{i+1}" class="pill" style="position:relative; font-size:30px; padding:8px 18px">✓ {t}</div>' for i, t in enumerate(C["glow"]))}</div></div>
</div>
<!-- S6 KHÁCH THẬT -->
<div id="s6" class="clip full" data-start="{r2(s6)}" data-duration="{r2(L6)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 30%, #fbf5ec 0%, #f6eee4 55%, #efe3d3 100%)" data-layout-allow-overlap>
  <div class="cl-title"><div class="kick" style="background:var(--choc)">REAL MERAH CLIENTS</div><div class="serif" style="font-weight:700; font-size:84px; margin-top:28px; color:var(--choc)">They love <em style="color:var(--bronze2)">their results</em></div></div>
  <div id="c1" class="card" style="left:60px; top:620px"><img src="assets/5_ba.png" alt=""></div>
  <div id="c2" class="card" style="left:460px; top:700px"><img src="assets/6_ba.png" alt=""></div>
  <div id="c3" class="card" style="left:260px; top:860px"><img src="assets/7_ba.png" alt=""></div>
</div>
<!-- S7 ƯU ĐÃI -->
<div id="s7" class="clip full" data-start="{r2(s7)}" data-duration="{r2(L7)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="offer-bg"></div><div id="sweep2" class="sweep"></div>
  <div class="offer-top"><div id="o-x" class="xmas">CHRISTMAS DEAL</div><div id="o-svc" class="svc">{C.get("svc","MAXFILL")}</div><div id="o-from" class="from">{C.get("from","STARTING FROM")}</div><div id="o-price" class="price">{C.get("price","₱2,999")}</div><div id="o-off" class="off">{C.get("off","40% OFF · until Nov 30")}</div></div>
  <div id="o-gift" class="gift"><img src="assets/qua_10k.jpg" alt=""><div><div class="gift-t1">+ CHRISTMAS GIFTS</div><div class="gift-t2">Up to<br>₱10,000</div><div class="gift-t3">Real ₱10,000 cash winner!</div></div></div>
</div>
<!-- S8 CTA -->
<div id="s8" class="clip full" data-start="{r2(s8)}" data-duration="{r2(L8)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 35%, #fbf5ec 0%, #f6eee4 55%, #efe3d3 100%)">
  <img id="cta-logo" class="cta-logo" src="assets/logo.png" alt="MERAH Beauty"><div id="cta-h" class="cta-h">Gifts are<br><em>limited!</em></div>
  <div id="cta-btn" class="btn"><span>💬</span>MESSAGE US NOW</div><div id="cta-addr" class="addr">MERAH BEAUTY · MAKATI</div>
</div>
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{r2(s3)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s4)}" data-duration="{r2(L4 + L5)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s6)}" data-duration="{r2(L6)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s7)}" data-duration="{r2(L7)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9">

{"".join(f'<audio class="clip" src="assets/vo{n}.mp3" data-start="{r2(t)}" data-duration="{r2(g[n-1])}" data-volume="1" data-track-index="10"></audio>' for n, t in ((1, s1 + 0.08), (2, s2 + 0.02), (3, s3 + 0.08), (4, s4 + 1.5), (5, s5 + 0.08), (6, s7 + 0.08), (7, s8 + 0.08)))}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s2 + 0.2 + d["t"])}" data-duration="0.5" data-volume="0.6" data-track-index="{13 + i % 2}"></audio>' for i, d in enumerate(defs))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(s3 - 0.15)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s3 + 0.1)}" data-duration="1.0" data-volume="0.45" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s3 + 0.9)}" data-duration="1.2" data-volume="0.45" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s3 + 1.6 + i * 0.55)}" data-duration="0.5" data-volume="0.55" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s4 + 0.2)}" data-duration="0.57" data-volume="0.55" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s4 + 1.0)}" data-duration="1.2" data-volume="0.55" data-track-index="15"></audio>
<audio class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{r2(s4 + 1.7)}" data-duration="0.57" data-volume="0.55" data-track-index="13"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s5 - 0.1)}" data-duration="0.57" data-volume="0.5" data-track-index="12"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s5 + 1.2 + i * 0.8)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(len(C["glow"])))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s6 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s6 + 0.3 + i * 0.6)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
<audio class="clip" src="assets/sfx/riser.mp3" data-start="{r2(s7 - 1.3)}" data-duration="1.4" data-volume="0.4" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s7)}" data-duration="1.0" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/chime.mp3" data-start="{r2(s7 + 1.3)}" data-duration="1.2" data-volume="0.55" data-track-index="13"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s7 + 4.0)}" data-duration="1.2" data-volume="0.55" data-track-index="15"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s8 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/click.mp3" data-start="{r2(s8 + 1.8)}" data-duration="0.4" data-volume="0.6" data-track-index="13"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused:true }}); const E = "power3.out", X = "expo.out";
tl.fromTo("#s1-k", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.1);
tl.fromTo("#s1-a", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, 0.25);
// dừng hình + khoanh lần lượt, giữ tất cả
{TRK}
tl.fromTo("#w-bef", {{ scale:1.0 }}, {{ scale:1.04, duration:{r2(L2)}, ease:"none" }}, {r2(s2)});
tl.to("#w-bef", {{ filter:"blur(14px)", duration:0.3, ease:"power2.in" }}, {r2(s3 - 0.3)});
// cơ chế
tl.fromTo("#m-num", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:0.45, ease:"power4.out" }}, {r2(s3 + 0.1)});
tl.fromTo("#m-sub", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(s3 + 0.4)});
tl.fromTo("#illus", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:E }}, {r2(s3 + 0.6)});
tl.fromTo(".drop", {{ opacity:0, y:-260 }}, {{ opacity:1, y:0, duration:0.6, ease:"power2.in", stagger:0.08 }}, {r2(s3 + 0.9)});
tl.to("#epi", {{ attr:{{ d:"M0 200 C 150 200, 300 200, 380 200 C 420 200, 480 200, 520 200 C 600 200, 750 200, 900 200 L 900 310 L 0 310 Z" }}, duration:1.0, ease:"power2.inOut" }}, {r2(s3 + 1.6)});
tl.to("#lblVol", {{ opacity:0, duration:0.3 }}, {r2(s3 + 1.3)});
tl.fromTo(".fib", {{ opacity:0.4 }}, {{ opacity:1, stroke:"#c9a46a", duration:0.8, stagger:0.15 }}, {r2(s3 + 1.9)});
{"".join(f'tl.fromTo("#ck{i+1}", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:0.35, ease:E }}, {r2(s3 + 1.6 + i * 0.55)});' for i in range(3))}
// lật 3D trước → sau, rồi trượt so sánh
tl.fromTo("#flip", {{ rotationY:0, scale:0.92 }}, {{ rotationY:180, scale:1, duration:1.1, ease:"power3.inOut" }}, {r2(s4 + 0.15)});
tl.fromTo("#t-aft", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s4 + 1.1)});
tl.fromTo("#cmp-bef", {{ clipPath:"inset(0px 1080px 0px 0px)" }}, {{ clipPath:"inset(0px 540px 0px 0px)", duration:1.0, ease:"power2.inOut" }}, {r2(s4 + 1.6)});
tl.fromTo("#ba-bar", {{ x:0 }}, {{ x:547, duration:1.0, ease:"power2.inOut" }}, {r2(s4 + 1.6)});
tl.fromTo("#t-bef", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s4 + 2.2)});
tl.fromTo("#ba-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s4 + 1.7)});
// video sau khi đẹp chạy
tl.fromTo("#g-k", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s5 + 0.1)});
tl.fromTo("#g-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s5 + 0.25)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:2100, duration:1.1, ease:"power2.inOut" }}, {r2(s5 + 0.2)});
{"".join(f'tl.fromTo("#b{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s5 + 1.2 + i * 0.8)});' for i in range(len(C["glow"])))}
tl.fromTo("#w-aend", {{ scale:1.0 }}, {{ scale:1.12, duration:{r2(max(0.1, L5 - AV))}, ease:"none" }}, {r2(s5 + AV)});
// khách thật
tl.fromTo("#c1", {{ opacity:0, y:200, rotation:-14 }}, {{ opacity:1, y:0, rotation:-6, duration:0.5, ease:"back.out(1.6)" }}, {r2(s6 + 0.2)});
tl.fromTo("#c2", {{ opacity:0, y:200, rotation:14 }}, {{ opacity:1, y:0, rotation:5, duration:0.5, ease:"back.out(1.6)" }}, {r2(s6 + 0.8)});
tl.fromTo("#c3", {{ opacity:0, y:200, rotation:-4 }}, {{ opacity:1, y:0, rotation:0, duration:0.5, ease:"back.out(1.6)" }}, {r2(s6 + 1.4)});
// ưu đãi
tl.fromTo("#o-x", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.35, ease:E }}, {r2(s7 + 0.05)});
tl.fromTo("#o-svc", {{ opacity:0, scale:1.3 }}, {{ opacity:1, scale:1, duration:0.45, ease:"power4.out" }}, {r2(s7 + 0.25)});
tl.fromTo("#o-from", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s7 + 0.8)});
tl.fromTo("#o-price", {{ opacity:0, scale:0.6 }}, {{ opacity:1, scale:1, duration:0.5, ease:"back.out(2)" }}, {r2(s7 + 1.3)});
tl.fromTo("#o-off", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.35, ease:E }}, {r2(s7 + 2.2)});
tl.fromTo("#sweep2", {{ x:0 }}, {{ x:2100, duration:1.2, ease:"power2.inOut" }}, {r2(s7 + 1.4)});
tl.fromTo("#o-gift", {{ opacity:0, y:140 }}, {{ opacity:1, y:0, duration:0.55, ease:"back.out(1.4)" }}, {r2(s7 + 4.0)});
// CTA
tl.fromTo("#cta-logo", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(s8 + 0.05)});
tl.fromTo("#cta-h", {{ opacity:0, scale:0.85 }}, {{ opacity:1, scale:1, duration:0.45, ease:"back.out(1.8)" }}, {r2(s8 + 0.2)});
tl.fromTo("#cta-btn", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(s8 + 1.3)});
tl.fromTo("#cta-addr", {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, {r2(s8 + 1.7)});
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
'''
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(html)
print("T=%.2f" % T, [r2(x) for x in (s1, s2, s3, s4, s5, s6, s7, s8)])
_h = io.open(W + "/index.html", encoding="utf-8").read(); _n = [0]
def _addid(m):
    _n[0] += 1; return f'<{m.group(1)} id="m{_n[0]}-{m.group(1)}" '
_h = re.sub(r'<(video|audio|img) (?![^>]*\bid=)', _addid, _h)
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(_h)
