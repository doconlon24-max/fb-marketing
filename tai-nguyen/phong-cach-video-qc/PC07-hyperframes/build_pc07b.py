"""PC07 builder chung (13/11/2026): python build_pc07.py <hf_dir> <pc07_index.html> <cfg.json>
cfg: vo (mp3 1 file, cắt theo _doan.json 6 đoạn: hook, khuyết điểm, sau, so sánh, ưu đãi, CTA), hook (text), defs, glow (4 pill), media."""
import io, json, math, re, subprocess, sys
W, PC07, CF = sys.argv[1], sys.argv[2], sys.argv[3]
C = json.load(io.open(CF, encoding="utf-8"))
css = re.search(r"<style>(.*?)</style>", io.open(PC07, encoding="utf-8").read(), re.S).group(1)
doan = json.load(io.open(C["doan"], encoding="utf-8")); g = [x["giay"] for x in doan]
off = 0.0
for i, x in enumerate(g):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.3f}", "-t", f"{x:.3f}", "-i", C["vo"], "-c:a", "libmp3lame", "-b:a", "160k", f"{W}/assets/vo{i+1}.mp3"], check=True); off += x
r2 = lambda x: f"{x:.2f}"
AL = C.get("aft_len", 1.3)
s1 = 0.0; L1 = max(g[0] + 0.4, 3.2)
sB = s1 + L1; LB = g[1] + 0.5
sA = sB + LB; LA = g[2] + 1.0
sT2 = sA + LA; LT = max(g[3] + 0.4, 2.6)
s3 = sT2 + LT; L3 = max(g[4] + 0.5, 3.4)
s4 = s3 + L3; L4 = max(g[5] + 0.4, 5.5)
s5 = s4 + L4; L5 = max(g[6] + 0.6, 4.5)
s6 = s5 + L5; L6 = 2.6
s7 = s6 + L6; L7 = g[7] + 0.4
s8 = s7 + L7; L8 = g[8] + 0.8
T = s8 + L8
VO = [(s1, 1), (sB, 2), (sA, 3), (sT2, 4), (s3, 5), (s4, 6), (s5, 7), (s7, 8), (s8, 9)]
step = g[2] / 4
defs = [tuple(x) for x in C["defs"]]
PCOL = [(60, 1600), (60, 1700), (560, 1600), (560, 1700)]
def arrow(i, k, x, y, lab):
    px, py = PCOL[i]; sx = px + 230; sy = py
    cx = (sx + x) / 2 + (90 if x < sx else -90); cy = (sy + y) / 2
    return (f'<div id="g-{k}" style="opacity:0"><svg style="position:absolute; left:0; top:0; width:1080px; height:1920px" viewBox="0 0 1080 1920" data-layout-ignore>'
            f'<defs><marker id="ah{k}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#e8cfa0"/></marker></defs>'
            f'<path id="ar-{k}" d="M{sx} {sy} Q {cx:.0f} {cy:.0f} {x} {y}" fill="none" stroke="#e8cfa0" stroke-width="6" stroke-linecap="round" marker-end="url(#ah{k})" style="filter:drop-shadow(0 2px 4px rgba(30,15,5,0.6))"/></svg>'
            f'<div id="p-{k}" class="pill" style="left:{px}px; top:{py}px; width:460px; justify-content:center; font-size:30px"><span class="dot"></span>{lab}</div></div>')
TL = C.get("talk_len", 2.6)
media = [("v_aft1.mp4", 0, AL, "v"), ("s_bef.png", sB, sT2 - sB, "i"),
         ("v_aft1.mp4", s4, AL, "v"), ("v_aft2.mp4", s4 + AL, AL, "v"), ("s_aft.png", s4 + 2 * AL, L4 - 2 * AL, "i"),
         ("v_aft2.mp4", AL, AL, "v"), ("s_aft.png", 2 * AL, L1 - 2 * AL, "i"),
         ("v_talk.mp4", sT2, min(TL, LT), "v"), ("v_talk_r.mp4", sT2 + TL, max(LT - TL, 0.01), "v")]
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
<div class="wrap" id="w-bef" style="z-index:1"><img class="clip full" src="assets/s_bef.png" alt="" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="1"></div>
<div class="wrap" id="w-aft" style="z-index:2"><img class="clip full" src="assets/s_aft.png" alt="" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="1"></div>

<!-- S1 HOOK: cảnh ĐẸP + No makeup -->
<div id="s1" class="clip full" data-start="0" data-duration="{r2(L1)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:620px"></div>
  <div class="top"><div id="s1-k" class="kick">{C["kick"]}</div><div id="s1-a" class="big" style="margin-top:22px; font-size:86px">{C["hook"]}</div></div>
</div>
<!-- S2 TRƯỚC KHI LÀM ĐẸP TẠI MERAH -->
<div id="sb" class="clip full" data-start="{r2(sB)}" data-duration="{r2(LB)}" data-track-index="2" style="z-index:5">
  <div class="shade-top" style="height:620px"></div>
  <div class="top"><div id="sb-k" class="kick" style="background:rgba(156,74,58,0.9); color:#fff3d6">BEFORE MERAH</div><div id="sb-a" class="big" style="margin-top:22px; font-size:78px">{C.get("before_h", "This was her<br><em>before MERAH</em>")}</div></div>
</div>
<!-- S3 MŨI TÊN CHỈ VẤN ĐỀ -->
<div id="sa" class="clip full" data-start="{r2(sA)}" data-duration="{r2(LA)}" data-track-index="2" style="z-index:5" data-layout-allow-overlap>
  <div class="shade-top" style="height:420px"></div><div class="shade-bot" style="height:560px"></div>
  <div class="top" style="top:150px"><div class="kick">BEFORE · WHERE IT SHOWS</div></div>
  {"".join(arrow(i, k, x, y, lab) for i, (k, x, y, lab) in enumerate(defs))}
</div>
<!-- S4 KHÁCH NÓI -->
<div id="st" class="clip full" data-start="{r2(sT2)}" data-duration="{r2(LT)}" data-track-index="2" style="z-index:5">
  <div class="shade-bot" style="height:520px"></div>
  <div class="bot" style="top:1600px"><div id="st-q" class="big" style="font-size:60px">{C.get("quote", "&ldquo;I wanted a <em>fuller, softer</em> look.&rdquo;")}</div></div>
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
<!-- S4 GLOW – giữ 5s, chữ dải trên -->
<div id="s4" class="clip full" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="2" style="z-index:5" data-layout-allow-overflow>
  <div class="shade-top" style="height:560px"></div><div id="sweep" class="sweep"></div>
  <div class="top" style="top:200px"><div id="g-h" class="big" style="font-size:86px">Hello, <em>new glow!</em></div></div>
  <svg class="spark" style="left:200px; top:560px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#fff3d6"/></svg>
  <svg class="spark" style="left:820px; top:520px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#e8cfa0"/></svg>
  <svg class="spark" style="left:720px; top:430px" viewBox="0 0 46 46"><path d="M23 0 L27 19 L46 23 L27 27 L23 46 L19 27 L0 23 L19 19 Z" fill="#fff3d6"/></svg>
  <div class="shade-bot" style="height:460px"></div>
  <div class="bot" style="top:1640px"><div style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap">
    {"".join(f'<div id="b{i+1}" class="pill" style="position:relative; font-size:30px">✓ {t}</div>' for i, t in enumerate(C["glow"]))}</div></div>
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

{"".join(f'<audio class="clip" src="assets/vo{n}.mp3" data-start="{r2(t + 0.08)}" data-duration="{r2(g[n-1])}" data-volume="1" data-track-index="10"></audio>' for t, n in VO)}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(sA + 0.3 + i * step)}" data-duration="0.5" data-volume="0.6" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(sB - 0.2)}" data-duration="1.4" data-volume="0.5" data-track-index="16"></audio>
<audio class="clip" src="assets/sfx/impact-bass-2.mp3" data-start="{r2(sB)}" data-duration="1.0" data-volume="0.45" data-track-index="17"></audio>
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(s3 - 0.15)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s3 + 0.1)}" data-duration="1.0" data-volume="0.45" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s3 + 0.9)}" data-duration="1.2" data-volume="0.45" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s3 + 1.6 + i * 0.55)}" data-duration="0.5" data-volume="0.55" data-track-index="{13 + i % 2}"></audio>' for i in range(3))}
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
// đẹp -> xấu: lật nhanh + mờ
tl.to("#w-m6", {{ filter:"blur(16px)", scale:1.08, duration:0.3, ease:"power2.in" }}, {r2(sB - 0.3)});
tl.fromTo("#w-m1", {{ filter:"blur(16px)", scale:1.12 }}, {{ filter:"blur(0px)", scale:1.0, duration:0.45, ease:"power3.out" }}, {r2(sB)});
tl.fromTo("#sb-k", {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:0.35, ease:X }}, {r2(sB + 0.15)});
tl.fromTo("#sb-a", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(sB + 0.3)});
// mũi tên chỉ vấn đề (giữ lại tất cả)
{"".join(f'tl.set("#g-{k}", {{ opacity:1 }}, {r2(sA + 0.2 + i * step)}); tl.fromTo("#ar-{k}", {{ attr:{{ "stroke-dasharray":"1400", "stroke-dashoffset":"1400" }} }}, {{ attr:{{ "stroke-dashoffset":"0" }}, duration:0.5, ease:"power2.out" }}, {r2(sA + 0.25 + i * step)}); tl.fromTo("#p-{k}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.35, ease:"back.out(2)" }}, {r2(sA + 0.2 + i * step)});' for i, (k, *_r) in enumerate(defs))}
tl.fromTo("#w-m1", {{ scale:1.0 }}, {{ scale:1.04, duration:{r2(LA)}, ease:"none" }}, {r2(sA)});
// khách nói
tl.fromTo("#st-q", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(sT2 + 0.2)});
tl.to("#w-m7, #w-m8", {{ filter:"blur(14px)", duration:0.3, ease:"power2.in" }}, {r2(s3 - 0.3)});
// cơ chế
tl.fromTo("#m-num", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:0.45, ease:"power4.out" }}, {r2(s3 + 0.1)});
tl.fromTo("#m-sub", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:E }}, {r2(s3 + 0.4)});
tl.fromTo("#illus", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:E }}, {r2(s3 + 0.6)});
tl.fromTo(".drop", {{ opacity:0, y:-260 }}, {{ opacity:1, y:0, duration:0.6, ease:"power2.in", stagger:0.08 }}, {r2(s3 + 0.9)});
tl.to("#epi", {{ attr:{{ d:"M0 200 C 150 200, 300 200, 380 200 C 420 200, 480 200, 520 200 C 600 200, 750 200, 900 200 L 900 310 L 0 310 Z" }}, duration:1.0, ease:"power2.inOut" }}, {r2(s3 + 1.6)});
tl.to("#lblVol", {{ opacity:0, duration:0.3 }}, {r2(s3 + 1.3)});
tl.fromTo(".fib", {{ opacity:0.4 }}, {{ opacity:1, stroke:"#c9a46a", duration:0.8, stagger:0.15 }}, {r2(s3 + 1.9)});
{"".join(f'tl.fromTo("#ck{i+1}", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:0.35, ease:E }}, {r2(s3 + 1.6 + i * 0.55)});' for i in range(3))}
// glow: lấy nét mờ sang cảnh đẹp
tl.fromTo("#w-m2", {{ filter:"blur(14px)", scale:1.1 }}, {{ filter:"blur(0px)", scale:1.0, duration:0.5, ease:"power2.out" }}, {r2(s4)});
tl.fromTo("#g-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s4 + 0.1)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:2100, duration:1.1, ease:"power2.inOut" }}, {r2(s4 + 0.2)});
tl.fromTo(".spark", {{ opacity:0, scale:0, rotation:-60, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1.2, rotation:0, duration:0.4, ease:"back.out(3)", stagger:0.15 }}, {r2(s4 + 0.3)});
{"".join(f'tl.fromTo("#b{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s4 + 1.4 + i * 0.8)});' for i in range(4))}
tl.fromTo("#w-m4", {{ scale:1.0 }}, {{ scale:1.06, duration:{r2(L4 - 2 * AL)}, ease:"none" }}, {r2(s4 + 2 * AL)});
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
print("T=%.2f" % T, [r2(x) for x in (s1, sB, sA, sT2, s3, s4, s5, s6, s7, s8)])
