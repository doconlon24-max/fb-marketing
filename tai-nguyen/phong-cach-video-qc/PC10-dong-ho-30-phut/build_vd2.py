"""PC10 'Đồng hồ 30 phút': thanh thông tin cố định ở đáy (che chữ gốc) + vòng đồng hồ 0→30 phút + 2 thẻ polaroid so sánh.
python build_vd2.py <hf_dir> <doan.json>"""
import io, json, math, sys
W = sys.argv[1]
d = [x["giay"] for x in json.load(open(sys.argv[2], encoding="utf-8"))]
r2 = lambda x: f"{x:.2f}"
s1 = 0.0; L1 = d[0] + 0.45
s2 = s1 + L1; L2 = d[1] + 0.6
s3 = s2 + L2; L3 = d[2] + 0.5
s4 = s3 + L3; L4 = max(d[3] + 1.2, 6.2)
s5 = s4 + L4; L5 = 5.0            # so sánh polaroid (nhạc + chữ)
s6 = s5 + L5; L6 = d[4] + 0.5     # khách thật
s7 = s6 + L6; L7 = d[5] + 0.5     # ưu đãi
s8 = s7 + L7; L8 = d[6] + 1.0     # CTA
T = s8 + L8
voice_at = [s1, s2, s3, s4, s6, s7, s8]
defects = [("c1", 645, 1113, 62, "DEEP SMILE LINES"), ("c2", 417, 975, 66, "UNDER-EYE HOLLOWS"), ("c3", 790, 1060, 64, "HOLLOW CHEEKS"), ("c4", 480, 1232, 52, "DROOPY MOUTH CORNERS")]
fixes = ["✓ SOFTER SMILE LINES", "✓ BRIGHTER UNDER-EYES", "✓ FULLER CHEEKS", "✓ LIFTED MOUTH CORNERS"]
step = d[1] / 4

def circ(cid, cx, cy, r):
    k = int(2 * math.pi * r) + 1
    return f'<circle id="{cid}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e8cfa0" stroke-width="7" stroke-dasharray="{k}" stroke-dashoffset="{k}" stroke-linecap="round"/>'

RING = 2 * math.pi * 210
html = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root {{ --cream:#f6eee4; --choc:#4a2e22; --gold:#c9a46a; --gold2:#e8cfa0; --bronze1:#3b2416; --bronze2:#8a5a32; --brick:#9c4a3a; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#1c120b; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:Montserrat, sans-serif; color:var(--choc); }}
.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
.wrap {{ position:absolute; inset:0; }}
.shade-top {{ position:absolute; left:0; top:0; width:1080px; height:560px; background:linear-gradient(180deg, rgba(28,16,8,0.9) 0%, rgba(28,16,8,0.5) 60%, rgba(28,16,8,0) 100%); }}
.top {{ position:absolute; left:60px; right:60px; top:170px; text-align:center; }}
.kick {{ display:inline-block; font-weight:700; font-size:26px; letter-spacing:0.2em; color:var(--gold2); background:rgba(59,36,22,0.9); padding:9px 20px; border-radius:40px; }}
.big {{ font-family:"Playfair Display", serif; font-weight:700; font-size:78px; line-height:1.05; color:#fff; text-shadow:0 6px 30px rgba(20,10,5,0.6); margin-top:18px; }}
.big em {{ color:#ffe7b8; font-style:italic; }}
/* thanh thông tin cố định ở đáy – che luôn chữ gốc của video */
.bar {{ position:absolute; left:40px; right:40px; top:1480px; height:230px; border-radius:34px; background:linear-gradient(180deg,#fbf5ec,#f1e3cf); border:3px solid var(--gold); box-shadow:0 20px 50px rgba(0,0,0,0.45); }}
.bar-in {{ position:absolute; left:70px; right:70px; top:1505px; height:180px; display:flex; flex-direction:column; justify-content:center; }}
.lab {{ font-weight:700; font-size:22px; letter-spacing:0.28em; color:var(--bronze2); text-align:center; margin-bottom:12px; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.pill {{ display:flex; align-items:center; justify-content:center; gap:10px; font-weight:700; font-size:26px; letter-spacing:0.03em; color:var(--choc); background:#fff; padding:12px 14px; border-radius:40px; border:2px solid var(--gold); white-space:nowrap; }}
.pill .dot {{ width:14px; height:14px; border-radius:50%; background:var(--brick); flex:none; }}
.pill.ok {{ background:linear-gradient(90deg,var(--bronze1),var(--bronze2)); color:#fff; border-color:var(--gold2); }}
.timer {{ position:absolute; right:60px; top:1755px; font-weight:700; font-size:30px; letter-spacing:0.2em; color:var(--gold2); }}
.cream {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #fbf5ec 0%, #f6eee4 50%, #efe3d3 100%); }}
.ring {{ position:absolute; left:290px; top:300px; width:500px; height:500px; }}
.ring-n {{ position:absolute; left:290px; top:300px; width:500px; height:500px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.ring-n b {{ font-family:"Playfair Display", serif; font-size:200px; line-height:0.9; color:var(--choc); }}
.ring-n span {{ font-weight:700; font-size:36px; letter-spacing:0.3em; color:var(--bronze2); }}
.mh {{ position:absolute; left:0; right:0; top:880px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:84px; line-height:1.05; color:var(--choc); }}
.mh em {{ color:var(--bronze2); }}
.steps {{ position:absolute; left:110px; right:110px; top:1140px; }}
.stp {{ display:flex; align-items:center; gap:24px; font-weight:700; font-size:40px; color:var(--choc); margin-bottom:24px; }}
.stp b {{ display:inline-flex; width:70px; height:70px; border-radius:50%; background:linear-gradient(135deg,var(--gold),var(--gold2)); color:#fff; align-items:center; justify-content:center; font-family:"Playfair Display", serif; font-size:38px; }}
.pol {{ position:absolute; top:420px; width:470px; height:720px; background:#fff; padding:18px 18px 90px; box-shadow:0 30px 70px rgba(40,20,10,0.4); }}
.pol .ph {{ width:100%; height:100%; overflow:hidden; }}
.pol img {{ width:100%; height:100%; object-fit:cover; object-position:50% 38%; }}
.pol .cap {{ position:absolute; left:0; right:0; bottom:22px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:44px; color:var(--choc); }}
.ribbon {{ position:absolute; left:340px; top:1180px; width:400px; text-align:center; font-weight:700; font-size:32px; letter-spacing:0.18em; color:#fff; background:var(--brick); padding:14px 0; border-radius:40px; box-shadow:0 12px 30px rgba(120,40,30,0.4); }}
.fan {{ position:absolute; top:640px; width:460px; height:620px; border-radius:26px; overflow:hidden; border:10px solid #fff; box-shadow:0 26px 60px rgba(74,46,34,0.3); }}
.fan img {{ width:100%; height:100%; object-fit:cover; }}
.bronze {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #8a5a32 0%, #5a3820 45%, #3b2416 100%); }}
.o-k {{ position:absolute; left:0; right:0; top:300px; text-align:center; }}
.o-k span {{ display:inline-block; font-weight:700; font-size:32px; letter-spacing:0.28em; color:var(--bronze1); background:linear-gradient(90deg,var(--gold),var(--gold2)); padding:12px 32px; border-radius:40px; }}
.o-svc {{ position:absolute; left:0; right:0; top:400px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:120px; color:#fff; }}
.o-rib {{ position:absolute; left:-20px; right:-20px; top:600px; height:330px; background:linear-gradient(90deg,#fbf5ec,#f1e3cf); transform:rotate(-4deg); box-shadow:0 30px 70px rgba(0,0,0,0.45); display:flex; align-items:center; justify-content:center; gap:30px; }}
.o-rib .f {{ font-weight:700; font-size:36px; letter-spacing:0.2em; color:var(--bronze2); writing-mode:horizontal-tb; text-align:right; line-height:1.3; }}
.o-rib .p {{ font-family:"Playfair Display", serif; font-weight:700; font-size:200px; line-height:1; background:linear-gradient(180deg,#8a5a32,#c9a46a 55%,#8a5a32); -webkit-background-clip:text; background-clip:text; color:transparent; }}
.o-off {{ position:absolute; left:0; right:0; top:1000px; text-align:center; }} .o-off span {{ display:inline-block; font-weight:700; font-size:40px; color:#fff; border:3px solid var(--gold2); padding:12px 30px; border-radius:40px; }}
.gift {{ position:absolute; left:110px; top:1130px; width:860px; height:300px; border-radius:30px; background:rgba(246,238,228,0.97); display:flex; align-items:center; gap:30px; padding:24px; box-shadow:0 20px 50px rgba(0,0,0,0.35); }}
.gift img {{ width:300px; height:252px; object-fit:cover; border-radius:20px; }}
.g1 {{ font-weight:700; font-size:34px; letter-spacing:0.08em; color:var(--bronze2); }} .g2 {{ font-family:"Playfair Display", serif; font-weight:700; font-size:64px; line-height:1.05; color:var(--choc); margin-top:6px; }} .g3 {{ font-weight:700; font-size:28px; color:var(--brick); margin-top:10px; }}
.cta-logo {{ position:absolute; left:290px; top:380px; width:500px; }}
.cta-h {{ position:absolute; left:0; right:0; top:720px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:100px; line-height:1.05; color:var(--choc); }}
.cta-h em {{ color:var(--bronze2); }}
.btn {{ position:absolute; left:160px; top:1060px; width:760px; height:150px; border-radius:80px; background:linear-gradient(90deg,var(--bronze1),var(--bronze2)); display:flex; align-items:center; justify-content:center; gap:22px; font-weight:700; font-size:52px; letter-spacing:0.08em; color:#fff; box-shadow:0 20px 50px rgba(74,46,34,0.4); }}
.addr {{ position:absolute; left:0; right:0; top:1260px; text-align:center; font-size:36px; letter-spacing:0.12em; color:var(--bronze2); font-weight:700; }}
.sweep {{ position:absolute; left:-500px; top:-200px; width:340px; height:2400px; background:linear-gradient(90deg, rgba(255,240,210,0) 0%, rgba(255,240,210,0.45) 50%, rgba(255,240,210,0) 100%); }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{r2(T)}" data-width="1080" data-height="1920">

<!-- NỀN: video chuyển động thật -->
<div class="wrap"><video class="clip full" src="assets/v_bef1.mp4" muted playsinline data-start="0" data-duration="2.15" data-track-index="1"></video></div>
<div class="wrap"><video class="clip full" src="assets/v_bef2.mp4" muted playsinline data-start="2.15" data-duration="{r2(min(1.4, s2 - 2.15))}" data-track-index="1"></video></div>
<div id="w-st" class="wrap"><img class="clip full" src="assets/s1.9.png" alt="" data-start="{r2(min(3.55, s2))}" data-duration="{r2(s3 - min(3.55, s2))}" data-track-index="1"></div>
<svg class="clip" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="2" style="position:absolute; left:0; top:0; width:1080px; height:1920px" viewBox="0 0 1080 1920">{"".join(circ(c, x, y, r) for c, x, y, r, _ in defects)}</svg>
<div id="w-a1" class="wrap"><video class="clip full" src="assets/v_aft1.mp4" muted playsinline data-start="{r2(s4)}" data-duration="2.1" data-track-index="1"></video></div>
<div class="wrap"><video class="clip full" src="assets/v_aft2.mp4" muted playsinline data-start="{r2(s4 + 2.1)}" data-duration="1.3" data-track-index="1"></video></div>
<div id="w-a3" class="wrap" style="transform-origin:540px 900px"><img class="clip full" src="assets/s13.0.png" alt="" data-start="{r2(s4 + 3.4)}" data-duration="{r2(L4 - 3.4)}" data-track-index="1"></div>
<div id="sweep" class="sweep clip" data-start="{r2(s4)}" data-duration="1.4" data-track-index="3"></div>

<div class="clip" data-start="0" data-duration="{r2(s3)}" data-track-index="4"><div class="shade-top"></div>
  <div id="h1" class="top clip" data-start="0" data-duration="{r2(L1)}" data-track-index="5"><div class="kick">MAXFILL · HA COLLAGEN</div><div class="big">Looking older<br>than <em>you feel?</em></div></div>
  <div id="h2" class="top clip" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="5"><div class="kick">BEFORE · WHAT WE SEE</div></div>
</div>
<div class="clip" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="4"><div class="shade-top"></div>
  <div id="h4" class="top"><div class="kick">30 MINUTES LATER</div><div class="big">Fresher. <em>Fuller.</em></div></div></div>

<!-- CƠ CHẾ: vòng đồng hồ 0→30 phút -->
<div class="clip cream" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="6">
  <svg id="deco" style="position:absolute; left:240px; top:250px; width:600px; height:600px" viewBox="0 0 600 600"><circle cx="300" cy="300" r="285" fill="none" stroke="#c9a46a" stroke-width="5" stroke-dasharray="4 22" stroke-linecap="round" opacity="0.8"/></svg>
  <svg class="ring" viewBox="0 0 500 500"><circle cx="250" cy="250" r="210" fill="none" stroke="#efe3d3" stroke-width="22"/>
    <circle id="rg" cx="250" cy="250" r="210" fill="none" stroke="#c9a46a" stroke-width="22" stroke-linecap="round" stroke-dasharray="{RING:.0f}" stroke-dashoffset="{RING:.0f}" transform="rotate(-90 250 250)"/></svg>
  <div class="ring-n"><b id="rn">0</b><span>MINUTES</span></div>
  <div id="mh" class="mh">Maxfill <em>HA collagen</em></div>
  <div class="steps"><div id="st1" class="stp"><b>1</b>Restores lost volume</div><div id="st2" class="stp"><b>2</b>Softens folds &amp; hollows</div><div id="st3" class="stp"><b>3</b>Natural, refreshed look</div></div>
</div>

<!-- SO SÁNH: 2 thẻ polaroid -->
<div class="clip cream" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="6">
  <div class="top" style="top:200px"><div class="kick" style="background:var(--choc)">SEE THE CHANGE</div></div>
  <div id="pa" class="pol" style="left:50px; transform:rotate(-5deg)"><div class="ph"><img src="assets/s1.9.png" alt=""></div><div class="cap">Before</div></div>
  <div id="pb" class="pol" style="left:560px; transform:rotate(4deg)"><div class="ph"><img src="assets/s13.0.png" alt=""></div><div class="cap">After</div></div>
  <div id="rb" class="ribbon">30 MINUTES</div>
</div>

<!-- KHÁCH THẬT: xoè 3 thẻ -->
<div class="clip cream" data-start="{r2(s6)}" data-duration="{r2(L6)}" data-track-index="6">
  <div class="top" style="top:300px"><div class="kick" style="background:var(--choc)">REAL MERAH CLIENTS</div><div class="big" style="color:var(--choc); text-shadow:none; font-size:76px">They love <em style="color:var(--bronze2)">their results</em></div></div>
  <div id="f1" class="fan" style="left:40px; transform:rotate(-9deg)"><img src="assets/5_ba.png" alt=""></div>
  <div id="f3" class="fan" style="left:580px; transform:rotate(9deg)"><img src="assets/7_ba.png" alt=""></div>
  <div id="f2" class="fan" style="left:310px; top:600px"><img src="assets/6_ba.png" alt=""></div>
</div>

<!-- ƯU ĐÃI: dải ruy băng giá -->
<div class="clip" data-start="{r2(s7)}" data-duration="{r2(L7)}" data-track-index="6"><div class="bronze"></div>
  <div id="ok" class="o-k"><span>CHRISTMAS DEAL</span></div>
  <div id="osv" class="o-svc">MAXFILL</div>
  <div id="orb" class="o-rib"><div class="f">STARTING<br>FROM</div><div class="p">₱2,999</div></div>
  <div id="oof" class="o-off"><span>40% OFF · until Nov 30</span></div>
  <div id="ogf" class="gift"><img src="assets/qua_10k.jpg" alt=""><div><div class="g1">+ CHRISTMAS GIFTS</div><div class="g2">Up to ₱10,000</div><div class="g3">Real ₱10,000 cash winner!</div></div></div>
</div>
<!-- CTA -->
<div class="clip cream" data-start="{r2(s8)}" data-duration="{r2(L8)}" data-track-index="6">
  <img id="cl" class="cta-logo" src="assets/logo.png" alt="MERAH Beauty"><div id="ch" class="cta-h">Gifts are<br><em>limited!</em></div>
  <div id="cb" class="btn"><span>💬</span>MESSAGE US NOW</div><div id="ca" class="addr">MERAH BEAUTY · MAKATI</div>
</div>

<!-- THANH ĐÁY cố định (cảnh có ảnh/video khách) -->
<div class="clip" data-start="0" data-duration="{r2(s3)}" data-track-index="7"><div class="bar"></div>
  <div id="hk" class="clip" data-start="0" data-duration="{r2(L1)}" data-track-index="9" style="position:absolute; left:70px; right:70px; top:1530px; text-align:center; font-family:'Playfair Display', serif; font-weight:700; font-size:64px; color:#4a2e22">Real client · <em style="color:#8a5a32">before</em></div>
  <div class="bar-in"><div id="lb1" class="lab">BEFORE MAXFILL</div><div class="grid2">{"".join(f'<div id="q{i+1}" class="pill"><span class="dot"></span>{lab}</div>' for i, (*_r, lab) in enumerate(defects))}</div></div></div>
<div class="clip" data-start="{r2(s4)}" data-duration="{r2(L4 + L5)}" data-track-index="7"><div class="bar"></div>
  <div class="bar-in"><div class="lab">AFTER MAXFILL</div><div class="grid2">{"".join(f'<div id="k{i+1}" class="pill ok">{t}</div>' for i, t in enumerate(fixes))}</div></div></div>

<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{r2(s3)}" data-track-index="8" style="position:absolute; left:40px; top:56px; width:210px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.7))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="8" style="position:absolute; left:40px; top:56px; width:210px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="8" style="position:absolute; left:40px; top:56px; width:210px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.7))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s5)}" data-duration="{r2(L5 + L6)}" data-track-index="8" style="position:absolute; left:40px; top:56px; width:210px; z-index:9">
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="{r2(s7)}" data-duration="{r2(L7)}" data-track-index="8" style="position:absolute; left:40px; top:56px; width:210px; z-index:9">

{"".join(f'<audio class="clip" src="assets/vo{i+1}.mp3" data-start="{r2(t + 0.1)}" data-duration="{r2(d[i])}" data-volume="1" data-track-index="10"></audio>' for i, t in enumerate(voice_at))}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s2 + 0.25 + i * step)}" data-duration="0.5" data-volume="0.55" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s3)}" data-duration="1.0" data-volume="0.45" data-track-index="12"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/click.mp3" data-start="{r2(s3 + 0.6 + i * 0.5)}" data-duration="0.4" data-volume="0.3" data-track-index="{13 + i % 2}"></audio>' for i in range(8))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(s4 - 0.4)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s4 + 0.2)}" data-duration="1.2" data-volume="0.55" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s4 + 1.2 + i * 0.9)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s5 - 0.1)}" data-duration="0.57" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/chime.mp3" data-start="{r2(s5 + 1.3)}" data-duration="1.2" data-volume="0.45" data-track-index="15"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s6 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/riser.mp3" data-start="{r2(s7 - 1.3)}" data-duration="1.4" data-volume="0.4" data-track-index="14"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s7)}" data-duration="1.0" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/chime.mp3" data-start="{r2(s7 + 1.4)}" data-duration="1.2" data-volume="0.5" data-track-index="13"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s8 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/click.mp3" data-start="{r2(s8 + 1.2)}" data-duration="0.4" data-volume="0.6" data-track-index="13"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused:true }}); const X = "expo.out";
tl.fromTo("#h1 .kick", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.1);
tl.fromTo("#h1 .big", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, 0.25);
tl.fromTo("#lb1", {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, {r2(s2)});
{"".join(f'tl.to("#{c}", {{ attr:{{ "stroke-dashoffset":0 }}, duration:0.5, ease:"power2.out" }}, {r2(s2 + 0.25 + i * step)}); tl.fromTo("#q{i+1}", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s2 + 0.3 + i * step)});' for i, (c, *_r) in enumerate(defects))}
tl.fromTo("#h2 .kick", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s2)});
// đồng hồ
tl.fromTo("#deco", {{ rotation:0, transformOrigin:"50% 50%" }}, {{ rotation:90, duration:{r2(L3)}, ease:"none" }}, {r2(s3)});  // vòng chấm xoay đều – cảnh không đứng
const rn = {{ v:0 }};
tl.to("#rg", {{ attr:{{ "stroke-dashoffset":0 }}, duration:4.0, ease:"power1.inOut" }}, {r2(s3 + 0.4)});
tl.to(rn, {{ v:30, duration:4.0, ease:"power1.inOut", onUpdate:() => {{ document.getElementById("rn").textContent = Math.round(rn.v); }} }}, {r2(s3 + 0.4)});
tl.fromTo("#mh", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s3 + 0.6)});
{"".join(f'tl.fromTo("#st{i+1}", {{ opacity:0, x:-60 }}, {{ opacity:1, x:0, duration:0.45, ease:X }}, {r2(s3 + 1.6 + i * 1.3)});' for i in range(3))}
// sau
tl.fromTo("#w-a1", {{ filter:"blur(14px)", scale:1.1 }}, {{ filter:"blur(0px)", scale:1.0, duration:0.5, ease:"power2.out" }}, {r2(s4)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:2000, duration:1.2, ease:"power2.inOut" }}, {r2(s4 + 0.2)});
tl.fromTo("#h4 .kick", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s4 + 0.1)});
tl.fromTo("#h4 .big", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s4 + 0.3)});
{"".join(f'tl.fromTo("#k{i+1}", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s4 + 0.5 + i * 0.9)});' for i in range(4))}
tl.fromTo("#w-a3", {{ scale:1.0 }}, {{ scale:1.06, duration:{r2(L4 - 3.4)}, ease:"none" }}, {r2(s4 + 3.4)});
// polaroid
tl.fromTo("#pa", {{ opacity:0, y:200, rotation:-15 }}, {{ opacity:1, y:0, rotation:-5, duration:0.6, ease:"back.out(1.5)" }}, {r2(s5 + 0.1)});
tl.fromTo("#pb", {{ opacity:0, y:200, rotation:15 }}, {{ opacity:1, y:0, rotation:4, duration:0.6, ease:"back.out(1.5)" }}, {r2(s5 + 0.5)});
tl.fromTo("#rb", {{ opacity:0, scale:0.6 }}, {{ opacity:1, scale:1, duration:0.45, ease:"back.out(2)" }}, {r2(s5 + 1.2)});
// khách thật
tl.fromTo("#f1", {{ opacity:0, x:-200 }}, {{ opacity:1, x:0, duration:0.5, ease:X }}, {r2(s6 + 0.1)});
tl.fromTo("#f3", {{ opacity:0, x:200 }}, {{ opacity:1, x:0, duration:0.5, ease:X }}, {r2(s6 + 0.3)});
tl.fromTo("#f2", {{ opacity:0, y:200 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s6 + 0.5)});
// ưu đãi
tl.fromTo("#ok", {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s7 + 0.1)});
tl.fromTo("#osv", {{ opacity:0, scale:1.25 }}, {{ opacity:1, scale:1, duration:0.5, ease:"power4.out" }}, {r2(s7 + 0.3)});
tl.fromTo("#orb", {{ opacity:0, x:-1100 }}, {{ opacity:1, x:0, duration:0.7, ease:X }}, {r2(s7 + 0.9)});
tl.fromTo("#oof", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s7 + 1.8)});
tl.fromTo("#ogf", {{ opacity:0, y:120 }}, {{ opacity:1, y:0, duration:0.55, ease:"back.out(1.4)" }}, {r2(s7 + 3.6)});
// CTA
tl.fromTo("#cl", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s8 + 0.05)});
tl.fromTo("#ch", {{ opacity:0, scale:0.85 }}, {{ opacity:1, scale:1, duration:0.5, ease:"back.out(1.8)" }}, {r2(s8 + 0.2)});
tl.fromTo("#cb", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s8 + 0.9)});
tl.fromTo("#ca", {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, {r2(s8 + 1.3)});
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>
'''
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(html)
print("T=%.2f" % T, [r2(x) for x in (s1, s2, s3, s4, s5, s6, s7, s8)])
