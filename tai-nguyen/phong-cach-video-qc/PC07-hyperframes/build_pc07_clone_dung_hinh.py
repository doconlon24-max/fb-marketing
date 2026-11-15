"""QC-20261114-VD3 v3 – CLONE TOÀN BỘ video gốc theo Sếp (15/11): chạy cảnh đầu full mặt -> DỪNG nói 3 vấn đề -> chạy tiếp ->
cảnh đẹp gần hết DỪNG nói đã khắc phục -> chuyển 3D -> so sánh khác biệt -> chạy phần video còn lại -> khách thật -> ưu đãi -> CTA.
PC07 dải đáy 15%.  python build_vd3_clone.py <hf_dir> <pc07_index.html> <vo.mp3> <vo_doan.json>"""
import io, json, math, re, subprocess, sys
W, PC07, VO, DOAN = sys.argv[1:5]
css = re.search(r"<style>(.*?)</style>", io.open(PC07, encoding="utf-8").read(), re.S).group(1)
g = [x["giay"] for x in json.load(io.open(DOAN, encoding="utf-8"))]
off = 0.0
for i, x in enumerate(g):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.3f}", "-t", f"{x:.3f}", "-i", VO, "-c:a", "libmp3lame", "-b:a", "160k", f"{W}/assets/vo{i+1}.mp3"], check=True); off += x
r2 = lambda x: f"{x:.2f}"
P1, P2, P2B, P3 = 1.0667, 3.8, 1.4333, 0.5333
t_p1 = 0.0
t_f1 = P1; v2 = max(g[0] + 0.25, P1 + 0.9); L_f1 = v2 + g[1] + 0.45 - t_f1
t_p2 = t_f1 + L_f1
t_f2 = t_p2 + P2 + P2B; L_f2 = g[3] + 0.55
t_3d = t_f2 + L_f2; L_cmp = max(0.75 + g[4] + 0.15 + g[5] + 0.45, 4.4)
t_p3 = t_3d + L_cmp
t_cl = t_p3 + P3; L_cl = 2.4
t_of = t_cl + L_cl; L_of = g[6] + 0.5
t_cta = t_of + L_of; L_cta = g[7] + 0.9
T = t_cta + L_cta
vs = [0.05, v2, t_p2 + 0.1, t_f2 + 0.12, t_3d + 0.75, t_3d + 0.75 + g[4] + 0.15, t_of + 0.08, t_cta + 0.08]
w1 = g[1] / 5.36
c_hol = v2 + 0.05; c_smi = v2 + 1.35 * w1; c_bal = v2 + 2.9 * w1


def ring(id_, cx, cy, r):
    dd = int(2 * math.pi * (r - 8)) + 1; sz = 2 * r
    return f'<svg id="{id_}" style="position:absolute; left:{cx-r}px; top:{cy-r}px; width:{sz}px; height:{sz}px" viewBox="0 0 {sz} {sz}"><circle cx="{r}" cy="{r}" r="{r-8}" fill="none" stroke="#e8cfa0" stroke-width="7" stroke-dasharray="{dd}" stroke-dashoffset="{dd}" stroke-linecap="round"/></svg>'


SPARK = '<path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="{}"/>'
html = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{css}
.top {{ position:absolute; left:70px; right:70px; top:170px; text-align:center; }}
.bot {{ position:absolute; left:60px; right:60px; top:1665px; text-align:center; }}
.band {{ position:absolute; left:0; top:1632px; width:1080px; height:288px; z-index:4; background:linear-gradient(180deg,#4a2d1b 0%,#3b2416 100%); border-top:3px solid #c9a46a }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{r2(T)}" data-width="1080" data-height="1920" style="perspective:1800px; background:#3b2416">
<div class="wrap" id="w-p1" style="z-index:1"><video class="clip full" src="assets/v_p1.mp4" muted playsinline data-start="{r2(t_p1)}" data-duration="{r2(P1)}" data-track-index="1"></video></div>
<div class="wrap" id="w-f1" style="z-index:1; transform-origin:540px 816px"><img class="clip full" src="assets/s_f1.png" alt="" data-start="{r2(t_f1)}" data-duration="{r2(L_f1)}" data-track-index="1"></div>
<div class="wrap" id="w-p2" style="z-index:1"><video class="clip full" src="assets/v_p2.mp4" muted playsinline data-start="{r2(t_p2)}" data-duration="{r2(P2)}" data-track-index="1"></video></div>
<div class="wrap" id="w-p2b" style="z-index:1"><video class="clip full" src="assets/v_p2b.mp4" muted playsinline data-start="{r2(t_p2 + P2)}" data-duration="{r2(P2B)}" data-track-index="1"></video></div>
<div class="wrap" id="w-f2" style="z-index:1; transform-origin:540px 816px"><img class="clip full" src="assets/s_f2.png" alt="" data-start="{r2(t_f2)}" data-duration="{r2(L_f2 + 0.7)}" data-track-index="1"></div>
<div class="wrap" id="w-cmp" style="z-index:2; transform-origin:540px 816px; opacity:0">
  <img class="clip full" src="assets/s_bef.png" alt="" data-start="{r2(t_3d)}" data-duration="{r2(L_cmp)}" data-track-index="5">
  <div id="w-aft" style="position:absolute; inset:0"><img class="clip full" src="assets/s_aft.png" alt="" data-start="{r2(t_3d)}" data-duration="{r2(L_cmp)}" data-track-index="6"></div>
</div>
<div class="wrap" id="w-p3" style="z-index:1"><video class="clip full" src="assets/v_p3.mp4" muted playsinline data-start="{r2(t_p3)}" data-duration="{r2(P3)}" data-track-index="1"></video></div>

<div class="band clip" data-start="0" data-duration="{r2(t_cl)}" data-track-index="3"></div>

<!-- HOOK (đang chạy cảnh đầu) -->
<div id="s1" class="clip full" data-start="0" data-duration="{r2(v2)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:560px"></div>
  <div class="top"><div id="s1-k" class="kick">MAXFILL · HA COLLAGEN</div><div id="s1-a" class="big" style="margin-top:22px; font-size:80px">Sunken cheeks making<br>you look <em>tired?</em></div></div>
  <div class="bot" style="top:1700px"><div class="serif" style="font-weight:700; font-size:54px; color:#fff3d6">Maxfill <em style="color:#e8cfa0">from ₱2,999</em></div><div style="font-family:Montserrat; font-weight:700; font-size:24px; letter-spacing:6px; color:#e8cfa0; margin-top:10px">MERAH BEAUTY · MAKATI</div></div>
</div>
<!-- DỪNG 1: 3 vấn đề -->
<div id="s2" class="clip full" data-start="{r2(v2)}" data-duration="{r2(t_p2 - v2)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:420px"></div>
  <div class="top" style="top:190px"><div class="kick">BEFORE · HER CONCERNS</div></div>
  {ring("r-a1", 215, 805, 76)}{ring("r-a2", 962, 735, 62)}
  {ring("r-b1", 520, 790, 54)}{ring("r-b2", 792, 792, 48)}
  <svg id="mid" style="position:absolute; left:0; top:0; width:1080px; height:1920px; opacity:0" viewBox="0 0 1080 1920"><line id="mid-l" x1="680" y1="300" x2="680" y2="1240" stroke="#fff3d6" stroke-width="4" stroke-dasharray="14 12"/><line x1="330" y1="420" x2="1000" y2="395" stroke="#e8cfa0" stroke-width="3" stroke-dasharray="6 10"/><line x1="380" y1="905" x2="900" y2="890" stroke="#e8cfa0" stroke-width="3" stroke-dasharray="6 10"/></svg>
  <div class="bot" style="top:1672px"><div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">
    <div id="p-a" class="pill" style="position:relative; font-size:30px"><span class="dot"></span>HOLLOW CHEEKS</div>
    <div id="p-b" class="pill" style="position:relative; font-size:30px"><span class="dot"></span>DEEP SMILE LINES</div>
    <div id="p-c" class="pill" style="position:relative; font-size:30px"><span class="dot"></span>UNBALANCED FACE</div></div></div>
</div>
<!-- CHẠY TIẾP -->
<div id="s3" class="clip full" data-start="{r2(t_p2)}" data-duration="{r2(P2 + P2B)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:420px"></div>
  <div class="top" style="top:190px"><div id="s3-k" class="kick">ONE MAXFILL SESSION</div></div>
  <div id="t3-bef" class="tag" style="left:60px; top:300px; background:rgba(59,36,22,0.85); opacity:0">BEFORE</div>
  <div id="t3-aft" class="tag" style="right:60px; top:300px; background:linear-gradient(90deg,#c9a46a,#e8cfa0); color:#3b2416; opacity:0">AFTER</div>
  <div class="bot" style="top:1700px"><div id="s3-a" class="serif" style="font-weight:700; font-size:58px; color:#fff3d6">at <em style="color:#e8cfa0">MERAH Beauty</em></div></div>
</div>
<!-- DỪNG 2: đã khắc phục -->
<div id="s4" class="clip full" data-start="{r2(t_f2)}" data-duration="{r2(L_f2)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="shade-top" style="height:500px"></div><div id="sweep" class="sweep"></div>
  <div class="top" style="top:190px"><div id="g-h" class="big" style="font-size:80px">Concerns <em>fixed!</em></div></div>
  <svg class="spark" style="left:230px; top:520px" viewBox="0 0 46 46">{SPARK.format("#fff3d6")}</svg>
  <svg class="spark" style="left:860px; top:600px" viewBox="0 0 46 46">{SPARK.format("#e8cfa0")}</svg>
  <svg class="spark" style="left:700px; top:430px" viewBox="0 0 46 46">{SPARK.format("#fff3d6")}</svg>
  <div class="bot" style="top:1672px"><div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">
    <div id="b1" class="pill" style="position:relative; font-size:30px">✓ FULLER CHEEKS</div><div id="b2" class="pill" style="position:relative; font-size:30px">✓ SOFTER SMILE LINES</div><div id="b3" class="pill" style="position:relative; font-size:30px">✓ BALANCED FACE</div></div></div>
</div>
<!-- SO SÁNH -->
<div id="s5" class="clip full" data-start="{r2(t_3d + 0.6)}" data-duration="{r2(L_cmp - 0.6)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:380px"></div>
  <div id="ba-bar" class="ba-bar" style="left:1080px; height:1632px"></div>
  <div id="t-bef" class="tag" style="left:60px; top:200px; background:rgba(59,36,22,0.85)">BEFORE</div>
  <div id="t-aft" class="tag" style="right:60px; top:200px; background:linear-gradient(90deg,#c9a46a,#e8cfa0); color:#3b2416">AFTER</div>
  <div class="bot" style="top:1712px"><div id="ba-h" class="big" style="font-size:62px">See the <em>difference</em></div></div>
  <div class="bot" style="top:1712px"><div id="ba-h2" class="big" style="font-size:62px; opacity:0">Same face, <em>just refreshed</em></div></div>
</div>
<!-- CHẠY NỐT phần còn lại -->
<div id="s6" class="clip full" data-start="{r2(t_p3)}" data-duration="{r2(P3)}" data-track-index="2" style="z-index:5">
</div>
<!-- KHÁCH THẬT -->
<div id="s7" class="clip full" data-start="{r2(t_cl)}" data-duration="{r2(L_cl)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 30%, #fbf5ec 0%, #f6eee4 55%, #efe3d3 100%)" data-layout-allow-overlap>
  <div class="cl-title"><div class="kick" style="background:var(--choc)">REAL MERAH CLIENTS</div><div class="serif" style="font-weight:700; font-size:84px; margin-top:28px; color:var(--choc)">They love <em style="color:var(--bronze2)">their results</em></div></div>
  <div id="c1" class="card" style="left:60px; top:620px"><img src="assets/5_ba.png" alt=""></div>
  <div id="c2" class="card" style="left:460px; top:700px"><img src="assets/6_ba.png" alt=""></div>
  <div id="c3" class="card" style="left:260px; top:860px"><img src="assets/7_ba.png" alt=""></div>
</div>
<!-- ƯU ĐÃI -->
<div id="s8" class="clip full" data-start="{r2(t_of)}" data-duration="{r2(L_of)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="offer-bg"></div><div id="sweep2" class="sweep"></div>
  <div class="offer-top"><div id="o-x" class="xmas">CHRISTMAS DEAL</div><div id="o-svc" class="svc">MAXFILL</div><div id="o-from" class="from">STARTING FROM</div><div id="o-price" class="price">₱2,999</div><div id="o-off" class="off">40% OFF · until Nov 30</div></div>
  <div id="o-gift" class="gift"><img src="assets/qua_10k.jpg" alt=""><div><div class="gift-t1">+ CHRISTMAS GIFTS</div><div class="gift-t2">Up to<br>₱10,000</div><div class="gift-t3">Real ₱10,000 cash winner!</div></div></div>
</div>
<!-- CTA -->
<div id="s9" class="clip full" data-start="{r2(t_cta)}" data-duration="{r2(L_cta)}" data-track-index="2" style="z-index:5; background: radial-gradient(ellipse at 50% 35%, #fbf5ec 0%, #f6eee4 55%, #efe3d3 100%)">
  <img id="cta-logo" class="cta-logo" src="assets/logo.png" alt="MERAH Beauty"><div id="cta-h" class="cta-h">Gifts are<br><em>limited!</em></div>
  <div id="cta-btn" class="btn"><span>💬</span>MESSAGE US NOW</div><div id="cta-addr" class="addr">MERAH BEAUTY · MAKATI</div>
</div>
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{r2(t_cl)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(t_cl)}" data-duration="{r2(L_cl)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(t_of)}" data-duration="{r2(L_of)}" data-track-index="4" style="position:absolute; left:36px; top:34px; width:220px; z-index:9">

{"".join(f'<audio class="clip" src="assets/vo{i+1}.mp3" data-start="{r2(vs[i])}" data-duration="{r2(g[i])}" data-volume="1" data-track-index="{10 + i % 2 * 6}"></audio>' for i in range(8))}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(t_f1)}" data-duration="1.0" data-volume="0.4" data-track-index="12"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(t)}" data-duration="0.5" data-volume="0.6" data-track-index="{13 + i % 2}"></audio>' for i, t in enumerate((c_hol + 0.1, c_smi + 0.1, c_bal + 0.1)))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(t_p2 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(t_f2 + 0.15)}" data-duration="1.2" data-volume="0.6" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(t_f2 + 1.0 + i * 1.1)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(t_3d - 0.1)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{r2(t_3d + 1.2)}" data-duration="0.57" data-volume="0.5" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(t_cl - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(t_cl + 0.3 + i * 0.6)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
<audio class="clip" src="assets/sfx/riser.mp3" data-start="{r2(t_of - 1.3)}" data-duration="1.4" data-volume="0.4" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(t_of)}" data-duration="1.0" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/chime.mp3" data-start="{r2(t_of + 1.3)}" data-duration="1.2" data-volume="0.55" data-track-index="13"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(t_of + 4.0)}" data-duration="1.2" data-volume="0.55" data-track-index="15"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(t_cta - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/click.mp3" data-start="{r2(t_cta + 1.8)}" data-duration="0.4" data-volume="0.6" data-track-index="13"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused:true }}); const E = "power3.out", X = "expo.out";
tl.fromTo("#s1-k", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.1);
tl.fromTo("#s1-a", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, 0.25);
tl.fromTo("#w-f1", {{ filter:"brightness(1.5)" }}, {{ filter:"brightness(1)", duration:0.35, ease:"power2.out" }}, {r2(t_f1)});
tl.fromTo("#w-f1", {{ scale:1.0 }}, {{ scale:1.04, duration:{r2(L_f1)}, ease:"none" }}, {r2(t_f1)});
const ring = (sel, t) => tl.fromTo(sel + " circle", {{ attr:{{ "stroke-dashoffset": parseFloat(document.querySelector(sel + " circle").getAttribute("stroke-dasharray")) }} }}, {{ attr:{{ "stroke-dashoffset":0 }}, duration:0.45, ease:"power2.out" }}, t);
ring("#r-a1", {r2(c_hol)}); ring("#r-a2", {r2(c_hol + 0.12)});
tl.fromTo("#p-a", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(c_hol + 0.1)});
ring("#r-b1", {r2(c_smi)}); ring("#r-b2", {r2(c_smi + 0.12)});
tl.fromTo("#p-b", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(c_smi + 0.1)});
tl.fromTo("#mid", {{ opacity:0 }}, {{ opacity:1, duration:0.35 }}, {r2(c_bal)});
tl.fromTo("#mid-l", {{ attr:{{ y2:300 }} }}, {{ attr:{{ y2:1240 }}, duration:0.6, ease:"power2.out" }}, {r2(c_bal)});
tl.fromTo("#p-c", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(c_bal + 0.1)});
tl.fromTo("#s3-k", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(t_p2 + 0.15)});
tl.fromTo("#s3-a", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(t_p2 + 0.4)});
tl.fromTo("#t3-bef", {{ opacity:0, x:-30 }}, {{ opacity:1, x:0, duration:0.3, ease:X }}, {r2(t_p2 + 2.5)});
tl.to("#t3-bef", {{ opacity:0, duration:0.15 }}, {r2(t_p2 + P2 + 0.17)});
tl.fromTo("#t3-aft", {{ opacity:0, x:30 }}, {{ opacity:1, x:0, duration:0.3, ease:X }}, {r2(t_p2 + P2 + 0.22)});
tl.fromTo("#w-f2", {{ filter:"brightness(1.5)" }}, {{ filter:"brightness(1)", duration:0.35, ease:"power2.out" }}, {r2(t_f2)});
tl.fromTo("#w-f2", {{ scale:1.0 }}, {{ scale:1.04, duration:{r2(L_f2)}, ease:"none" }}, {r2(t_f2)});
tl.fromTo("#g-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(t_f2 + 0.1)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:2100, duration:1.1, ease:"power2.inOut" }}, {r2(t_f2 + 0.2)});
tl.fromTo(".spark", {{ opacity:0, scale:0, rotation:-60, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1.2, rotation:0, duration:0.4, ease:"back.out(3)", stagger:0.15 }}, {r2(t_f2 + 0.3)});
{"".join(f'tl.fromTo("#b{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(t_f2 + 0.9 + i * 1.1)});' for i in range(3))}
// chuyển cảnh 3D: lật khối sang so sánh
tl.fromTo("#w-f2", {{ rotationY:0, z:0 }}, {{ rotationY:-90, z:-300, duration:0.6, ease:"power2.in", immediateRender:false }}, {r2(t_3d)});
tl.fromTo("#w-cmp", {{ opacity:1, rotationY:90, z:-300 }}, {{ opacity:1, rotationY:0, z:0, duration:0.6, ease:"power2.out", immediateRender:false }}, {r2(t_3d + 0.6)});
tl.fromTo("#w-aft", {{ clipPath:"inset(0px 0px 0px 1080px)" }}, {{ clipPath:"inset(0px 0px 0px 0px)", duration:1.3, ease:"power2.inOut" }}, {r2(t_3d + 1.3)});
tl.fromTo("#ba-bar", {{ x:0 }}, {{ x:-1090, duration:1.3, ease:"power2.inOut" }}, {r2(t_3d + 1.3)});
tl.fromTo("#t-aft", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(t_3d + 2.0)});
tl.to("#t-bef", {{ opacity:0, duration:0.3 }}, {r2(t_3d + 2.4)});
tl.fromTo("#ba-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(t_3d + 0.8)});
tl.set("#w-cmp", {{ opacity:0 }}, {r2(t_p3)});
tl.to("#ba-h", {{ opacity:0, y:-20, duration:0.3 }}, {r2(vs[5] - 0.2)});
tl.fromTo("#ba-h2", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(vs[5])});
tl.fromTo("#c1", {{ opacity:0, y:200, rotation:-14 }}, {{ opacity:1, y:0, rotation:-6, duration:0.5, ease:"back.out(1.6)" }}, {r2(t_cl + 0.2)});
tl.fromTo("#c2", {{ opacity:0, y:200, rotation:14 }}, {{ opacity:1, y:0, rotation:5, duration:0.5, ease:"back.out(1.6)" }}, {r2(t_cl + 0.8)});
tl.fromTo("#c3", {{ opacity:0, y:200, rotation:-4 }}, {{ opacity:1, y:0, rotation:0, duration:0.5, ease:"back.out(1.6)" }}, {r2(t_cl + 1.4)});
tl.fromTo("#o-x", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.35, ease:E }}, {r2(t_of + 0.05)});
tl.fromTo("#o-svc", {{ opacity:0, scale:1.3 }}, {{ opacity:1, scale:1, duration:0.45, ease:"power4.out" }}, {r2(t_of + 0.25)});
tl.fromTo("#o-from", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(t_of + 0.8)});
tl.fromTo("#o-price", {{ opacity:0, scale:0.6 }}, {{ opacity:1, scale:1, duration:0.5, ease:"back.out(2)" }}, {r2(t_of + 1.3)});
tl.fromTo("#o-off", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.35, ease:E }}, {r2(t_of + 2.2)});
tl.fromTo("#sweep2", {{ x:0 }}, {{ x:2100, duration:1.2, ease:"power2.inOut" }}, {r2(t_of + 1.4)});
tl.fromTo("#o-gift", {{ opacity:0, y:140 }}, {{ opacity:1, y:0, duration:0.55, ease:"back.out(1.4)" }}, {r2(t_of + 4.0)});
tl.fromTo("#cta-logo", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(t_cta + 0.05)});
tl.fromTo("#cta-h", {{ opacity:0, scale:0.85 }}, {{ opacity:1, scale:1, duration:0.45, ease:"back.out(1.8)" }}, {r2(t_cta + 0.2)});
tl.fromTo("#cta-btn", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(t_cta + 1.3)});
tl.fromTo("#cta-addr", {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, {r2(t_cta + 1.7)});
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>
'''
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(html)
print("T=%.2f" % T, dict(f1=r2(t_f1), p2=r2(t_p2), f2=r2(t_f2), d3=r2(t_3d), p3=r2(t_p3), cl=r2(t_cl), of=r2(t_of), cta=r2(t_cta), hol=r2(c_hol), smi=r2(c_smi), bal=r2(c_bal)))
