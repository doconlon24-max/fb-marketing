"""VD3 v8 – giữ phong cách PC07 (VD3 v7 sếp chấm đẹp nhất) + sửa: video chuyển động, khoanh đúng khuyết điểm,
giữ cảnh đẹp 5s + trượt trước/sau 4.5s, chữ chỉ ở dải trên / dưới.  python build_vd3.py <hf_dir> <pc07_index.html>"""
import io, math, re, subprocess, sys
W, PC07 = sys.argv[1], sys.argv[2]
css = re.search(r"<style>(.*?)</style>", io.open(PC07, encoding="utf-8").read(), re.S).group(1)
def du(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
d = [du(f"{W}/assets/vo{i}.mp3") for i in range(1, 9)]
r2 = lambda x: f"{x:.2f}"
s1 = 0.0; L1 = max(d[0] + 0.35, 3.3)
s2 = s1 + L1; L2 = d[1] + 0.6
s3 = s2 + L2; L3 = d[2] + 0.5
s4 = s3 + L3; L4 = 5.0
s5 = s4 + L4; L5 = 4.5
s6 = s5 + L5; L6 = d[5] + 0.3
s7 = s6 + L6; L7 = d[6] + 0.4
s8 = s7 + L7; L8 = d[7] + 0.6
T = s8 + L8
step = d[1] / 4
# khuyết điểm trên ảnh s0.4 (toạ độ khung 1080x1920)
defs = [("a", 675, 832, 72, "PUFFY UNDER-EYES"), ("b", 450, 1028, 60, "DEEP SMILE LINES"), ("c", 752, 950, 58, "HOLLOW CHEEKS"), ("d", 388, 1180, 70, "SAGGING JAWLINE")]
PY = 1560  # nhãn pill ở dải dưới (dưới cằm)

def grp(k, cx, cy, r, lab, first):
    dd = int(2 * math.pi * (r - 8)) + 1; sz = 2 * r
    hid = "" if first else ' style="opacity:0"'
    return (f'<div id="g-{k}"{hid}>'
            f'<svg style="position:absolute; left:0; top:0; width:1080px; height:1920px" viewBox="0 0 1080 1920" data-layout-ignore><line x1="{cx}" y1="{cy + r}" x2="540" y2="{PY}" stroke="#e8cfa0" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/></svg>'
            f'<svg id="r-{k}" style="position:absolute; left:{cx - r}px; top:{cy - r}px; width:{sz}px; height:{sz}px" viewBox="0 0 {sz} {sz}"><circle cx="{r}" cy="{r}" r="{r - 8}" fill="none" stroke="#e8cfa0" stroke-width="7" stroke-dasharray="{dd}" stroke-dashoffset="{dd}" stroke-linecap="round"/></svg>'
            f'<div style="position:absolute; left:0; right:0; top:{PY}px; display:flex; justify-content:center"><div id="p-{k}" class="pill" style="position:relative"><span class="dot"></span>{lab}</div></div></div>')

media = [("v_bef1.mp4", 0, 0.85, "v"), ("v_bef2.mp4", 0.85, 1.45, "v"), ("s0.4.png", 2.3, s3 - 2.3, "i"),
         ("v_aft1.mp4", s4, 1.45, "v"), ("v_aft2.mp4", s4 + 1.45, 0.9, "v"), ("v_aft3.mp4", s4 + 2.35, 1.0, "v"), ("s8.9.png", s4 + 3.35, L4 - 3.35, "i")]
mhtml = ""
for i, (f, st, du_, kind) in enumerate(media):
    tag = (f'<video class="clip full" src="assets/{f}" muted playsinline data-start="{r2(st)}" data-duration="{r2(du_)}" data-track-index="1"></video>' if kind == "v"
           else f'<img class="clip full" src="assets/{f}" alt="" data-start="{r2(st)}" data-duration="{r2(du_)}" data-track-index="1">')
    mhtml += f'<div class="wrap" id="w-m{i}" style="transform-origin:540px 960px; z-index:1">{tag}</div>\n'

html = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{css}
.top {{ position:absolute; left:70px; right:70px; top:170px; text-align:center; }}
.bot {{ position:absolute; left:70px; right:70px; top:1560px; text-align:center; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{r2(T)}" data-width="1080" data-height="1920">
{mhtml}
<div class="wrap" id="w-bef" style="z-index:1"><img class="clip full" src="assets/s0.4.png" alt="" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="1"></div>
<div class="wrap" id="w-aft" style="z-index:2"><img class="clip full" src="assets/s4.7.png" alt="" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="1"></div>

<!-- S1 HOOK: chữ dải trên -->
<div id="s1" class="clip full" data-start="0" data-duration="{r2(L1)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:620px"></div>
  <div class="top"><div id="s1-k" class="kick">MAXFILL · HA COLLAGEN</div><div id="s1-a" class="big" style="margin-top:22px; font-size:82px">Is this what you see<br>in the <em>mirror?</em></div></div>
</div>
<!-- S2 KHUYẾT ĐIỂM -->
<div id="s2" class="clip full" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:480px"></div><div class="shade-bot" style="height:520px"></div>
  <div class="top" style="top:300px"><div class="kick">BEFORE · WHERE IT SHOWS</div></div>
  {"".join(grp(k, x, y, r, lab, i == 0) for i, (k, x, y, r, lab) in enumerate(defs))}
</div>
<!-- S3 CƠ CHẾ (giữ nguyên kiểu PC07) -->
<div id="s3" class="clip full" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 20%, #fbf5ec 0%, #f6eee4 50%, #efe3d3 100%)">
  <div class="mech-title"><div id="m-num" class="mech-num"><span>30</span><small>min</small></div><div id="m-sub" class="mech-sub">MAXFILL · HA COLLAGEN</div></div>
  <div id="illus" class="illus"><svg width="900" height="560" viewBox="0 0 900 560"><defs>
    <linearGradient id="gDerm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2cdb4"/><stop offset="1" stop-color="#e3a98a"/></linearGradient>
    <linearGradient id="gEpi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8e2cf"/><stop offset="1" stop-color="#efcdb2"/></linearGradient>
    <radialGradient id="gDrop" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#fff6dd"/><stop offset="0.5" stop-color="#e8cfa0"/><stop offset="1" stop-color="#c9a46a"/></radialGradient></defs>
    <rect x="0" y="300" width="900" height="260" fill="url(#gDerm)"/>
    <path id="epi" d="M0 200 C 150 200, 300 200, 380 230 C 420 300, 480 300, 520 230 C 600 200, 750 200, 900 200 L 900 310 L 0 310 Z" fill="url(#gEpi)"/>
    <g stroke="#c98f6d" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.55"><path class="fib" d="M30 380 C 120 350, 200 410, 290 380 S 470 350, 560 380 S 760 410, 870 380"/><path class="fib" d="M30 440 C 140 410, 230 470, 330 440 S 520 410, 620 440 S 790 470, 870 440"/><path class="fib" d="M30 500 C 110 470, 210 530, 300 500 S 480 470, 580 500 S 770 530, 870 500"/></g>
    <g><circle class="drop" cx="420" cy="330" r="20" fill="url(#gDrop)"/><circle class="drop" cx="470" cy="350" r="16" fill="url(#gDrop)"/><circle class="drop" cx="380" cy="365" r="14" fill="url(#gDrop)"/><circle class="drop" cx="510" cy="320" r="13" fill="url(#gDrop)"/><circle class="drop" cx="450" cy="395" r="18" fill="url(#gDrop)"/><circle class="drop" cx="350" cy="330" r="11" fill="url(#gDrop)"/></g>
    <text id="lblVol" x="450" y="150" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="34" letter-spacing="4" fill="#8a5a32">LOST VOLUME</text></svg><div class="illus-tag">Illustration</div></div>
  <div class="checks"><div id="ck1" class="check"><b>✓</b>FIRMER</div><div id="ck2" class="check"><b>✓</b>SMOOTHER</div><div id="ck3" class="check"><b>✓</b>YOUNGER-LOOKING</div></div>
</div>
<!-- S4 GLOW – giữ 5s, chữ dải trên -->
<div id="s4" class="clip full" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="shade-top" style="height:560px"></div><div id="sweep" class="sweep"></div>
  <div class="top" style="top:200px"><div id="g-h" class="big" style="font-size:86px">Hello, <em>new glow!</em></div></div>
  <svg class="spark" style="left:200px; top:560px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#fff3d6"/></svg>
  <svg class="spark" style="left:820px; top:520px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#e8cfa0"/></svg>
  <svg class="spark" style="left:720px; top:430px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#fff3d6"/></svg>
  <div class="shade-bot" style="height:460px"></div>
  <div class="bot" style="top:1640px"><div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap">
    <div id="b1" class="pill" style="position:relative; font-size:30px">✓ SMOOTHER UNDER-EYES</div><div id="b2" class="pill" style="position:relative; font-size:30px">✓ SOFTER SMILE LINES</div>
    <div id="b3" class="pill" style="position:relative; font-size:30px">✓ FULLER CHEEKS</div><div id="b4" class="pill" style="position:relative; font-size:30px">✓ LIFTED JAWLINE</div></div></div>
</div>
<!-- S5 TRƯỚC/SAU trượt – giữ 4.5s -->
<div id="s5" class="clip full" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:380px"></div>
  <div id="ba-bar" class="ba-bar" style="left:1080px"></div>
  <div class="tag" style="left:60px; top:230px; background:rgba(59,36,22,0.85)">BEFORE</div>
  <div id="t-aft" class="tag" style="right:60px; top:230px; background:linear-gradient(90deg,#c9a46a,#e8cfa0); color:#3b2416">AFTER</div>
  <div class="shade-bot" style="height:420px"></div>
  <div class="bot" style="top:1660px"><div id="ba-h" class="big" style="font-size:72px">See the <em>difference</em></div></div>
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
  <div class="offer-top"><div id="o-x" class="xmas">CHRISTMAS DEAL</div><div id="o-svc" class="svc">MAXFILL</div><div id="o-from" class="from">STARTING FROM</div><div id="o-price" class="price">₱2,999</div><div id="o-off" class="off">40% OFF · until Nov 30</div></div>
  <div id="o-gift" class="gift"><img src="assets/qua_10k.jpg" alt=""><div><div class="gift-t1">+ CHRISTMAS GIFTS</div><div class="gift-t2">Up to<br>₱10,000</div><div class="gift-t3">Real ₱10,000 cash winner!</div></div></div>
</div>
<!-- S8 CTA -->
<div id="s8" class="clip full" data-start="{r2(s8)}" data-duration="{r2(L8)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 35%, #fbf5ec 0%, #f6eee4 55%, #efe3d3 100%)">
  <img id="cta-logo" class="cta-logo" src="assets/logo.png" alt="MERAH Beauty"><div id="cta-h" class="cta-h">Gifts are<br><em>limited!</em></div>
  <div id="cta-btn" class="btn"><span>💬</span>MESSAGE US NOW</div><div id="cta-addr" class="addr">MERAH BEAUTY · MAKATI</div>
</div>
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{r2(s3)}" data-track-index="4" style="position:absolute; left:40px; top:56px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="4" style="position:absolute; left:40px; top:56px; width:220px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s4)}" data-duration="{r2(L4 + L5)}" data-track-index="4" style="position:absolute; left:40px; top:56px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s6)}" data-duration="{r2(L6)}" data-track-index="4" style="position:absolute; left:40px; top:56px; width:220px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s7)}" data-duration="{r2(L7)}" data-track-index="4" style="position:absolute; left:40px; top:56px; width:220px; z-index:9">

{"".join(f'<audio class="clip" src="assets/vo{i+1}.mp3" data-start="{r2(t + 0.08)}" data-duration="{r2(d[i])}" data-volume="1" data-track-index="10"></audio>' for i, t in enumerate((s1, s2, s3, s4, s5, s6, s7, s8)))}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s2 + 0.2 + i * step)}" data-duration="0.5" data-volume="0.6" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(s3 - 0.15)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s3 + 0.1)}" data-duration="1.0" data-volume="0.45" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s3 + 3.3)}" data-duration="1.2" data-volume="0.45" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s3 + 6.1 + i)}" data-duration="0.5" data-volume="0.55" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s4 - 0.1)}" data-duration="0.57" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s4 + 0.15)}" data-duration="1.2" data-volume="0.6" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s4 + 1.4 + i * 0.8)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{r2(s5 + 0.2)}" data-duration="0.57" data-volume="0.55" data-track-index="12"></audio>
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
// khuyết điểm lần lượt theo lời đọc
{"".join(f'tl.set("#g-{k}", {{ opacity:1 }}, {r2(s2 + i * step)});' + (f' tl.set("#g-{defs[i-1][0]}", {{ opacity:0 }}, {r2(s2 + i * step)});' if i else '') + f' tl.fromTo("#r-{k} circle", {{ attr:{{ "stroke-dashoffset": parseFloat(document.querySelector("#r-{k} circle").getAttribute("stroke-dasharray")) }} }}, {{ attr:{{ "stroke-dashoffset":0 }}, duration:0.45, ease:"power2.out" }}, {r2(s2 + 0.15 + i * step)}); tl.fromTo("#p-{k}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(s2 + 0.25 + i * step)});' for i, (k, *_r) in enumerate(defs))}
tl.to("#w-m2", {{ filter:"blur(14px)", duration:0.3, ease:"power2.in" }}, {r2(s3 - 0.3)});
// cơ chế
tl.fromTo("#m-num", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:0.45, ease:"power4.out" }}, {r2(s3 + 0.1)});
tl.fromTo("#m-sub", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(s3 + 0.4)});
tl.fromTo("#illus", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:E }}, {r2(s3 + 0.6)});
tl.fromTo(".drop", {{ opacity:0, y:-260 }}, {{ opacity:1, y:0, duration:0.8, ease:"power2.in", stagger:0.12 }}, {r2(s3 + 3.3)});
tl.to("#epi", {{ attr:{{ d:"M0 200 C 150 200, 300 200, 380 200 C 420 200, 480 200, 520 200 C 600 200, 750 200, 900 200 L 900 310 L 0 310 Z" }}, duration:1.8, ease:"power2.inOut" }}, {r2(s3 + 4.3)});
tl.to("#lblVol", {{ opacity:0, duration:0.3 }}, {r2(s3 + 3.9)});
tl.fromTo(".fib", {{ opacity:0.4 }}, {{ opacity:1, stroke:"#c9a46a", duration:1.2, stagger:0.2 }}, {r2(s3 + 4.7)});
{"".join(f'tl.fromTo("#ck{i+1}", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:0.35, ease:E }}, {r2(s3 + 6.1 + i)});' for i in range(3))}
// glow: lấy nét mờ sang cảnh đẹp
tl.fromTo("#w-m3", {{ filter:"blur(14px)", scale:1.1 }}, {{ filter:"blur(0px)", scale:1.0, duration:0.5, ease:"power2.out" }}, {r2(s4)});
tl.fromTo("#g-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s4 + 0.1)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:2100, duration:1.1, ease:"power2.inOut" }}, {r2(s4 + 0.2)});
tl.fromTo(".spark", {{ opacity:0, scale:0, rotation:-60, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1.2, rotation:0, duration:0.4, ease:"back.out(3)", stagger:0.15 }}, {r2(s4 + 0.3)});
{"".join(f'tl.fromTo("#b{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s4 + 1.4 + i * 0.8)});' for i in range(4))}
tl.fromTo("#w-m6", {{ scale:1.0 }}, {{ scale:1.06, duration:{r2(L4 - 3.35)}, ease:"none" }}, {r2(s4 + 3.35)});
// trượt trước/sau, giữ lâu
tl.fromTo("#w-aft", {{ clipPath:"inset(0px 0px 0px 1080px)" }}, {{ clipPath:"inset(0px 0px 0px 0px)", duration:1.2, ease:"power2.inOut" }}, {r2(s5 + 0.3)});
tl.fromTo("#ba-bar", {{ x:0 }}, {{ x:-1090, duration:1.2, ease:"power2.inOut" }}, {r2(s5 + 0.3)});
tl.fromTo("#t-aft", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s5 + 1.0)});
tl.fromTo("#ba-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s5 + 0.2)});
tl.fromTo("#w-bef, #w-aft", {{ scale:1.0 }}, {{ scale:1.05, duration:{r2(L5)}, ease:"none" }}, {r2(s5)});
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
</script></body></html>
'''
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(html)
print("T=%.2f" % T, [r2(x) for x in (s1, s2, s3, s4, s5, s6, s7, s8)])
