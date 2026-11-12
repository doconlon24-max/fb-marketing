"""PC09 'Tạp chí' (magazine): khung video 2/3 trên + bảng chữ kem 1/3 dưới – chữ không bao giờ đè mặt.
python build_vd1.py <hf_dir> [doan.json]"""
import io, json, math, sys
W = sys.argv[1]
dur = [3.6, 4.2, 6.5, 2.2, 8.5, 3.5]
if len(sys.argv) > 2:
    dur = [x["giay"] for x in json.load(open(sys.argv[2], encoding="utf-8"))]
d1, d2, d3, d4, d5, d6 = dur
s1 = 0.0; L1 = d1 + 0.4
s2 = L1; L2 = max(d2 + 0.9, 5.0)
s3 = s2 + L2; L3 = max(d3 + 0.8, 7.95)
s4 = s3 + L3; L4 = max(d4 + 2.6, 5.0)
s5 = s4 + L4; L5 = d5 + 0.8
s6 = s5 + L5; L6 = d6 + 1.0
T = s6 + L6
FY = 350  # nguồn hiện từ y=300 (bỏ chữ gốc phía trên)
r2 = lambda x: f"{x:.2f}"

def circ(cid, cx, cy, r):
    d = int(2 * math.pi * r) + 1
    return f'<circle id="{cid}" cx="{cx}" cy="{cy - FY}" r="{r}" fill="none" stroke="#e8cfa0" stroke-width="7" stroke-dasharray="{d}" stroke-dashoffset="{d}" stroke-linecap="round"/>'

# 4 khuyết điểm (toạ độ ảnh nguồn s11.3)
defects = [("c1", 720, 930, 80, "FLAT CHEEKBONES"), ("c2", 550, 1100, 85, "THIN LIPS"), ("c3", 300, 1180, 75, "SOFT JAWLINE"), ("c4", 550, 1262, 62, "SHORT CHIN")]
fixes = ["✓ SCULPTED CHEEKS", "✓ FULLER LIPS", "✓ DEFINED JAWLINE", "✓ PROJECTED CHIN"]
step = d2 / 4
a3 = [(s3, 2.75, "v_aft1"), (s3 + 2.75, 2.8, "v_aft2"), (s3 + 5.55, L3 - 5.55, "v_aft3")]

html = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
:root {{ --cream:#f6eee4; --cream2:#efe3d3; --choc:#4a2e22; --gold:#c9a46a; --gold2:#e8cfa0; --bronze1:#3b2416; --bronze2:#8a5a32; --brick:#9c4a3a; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--cream); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:Montserrat, sans-serif; color:var(--choc); }}
.frame {{ position:absolute; left:0; top:0; width:1080px; height:1300px; overflow:hidden; background:#2a1a10; }}
.frame .m {{ position:absolute; left:0; top:-{FY}px; width:1080px; height:1920px; object-fit:cover; }}
.panel {{ position:absolute; left:0; top:1270px; width:1080px; height:650px; background:linear-gradient(180deg,#fbf5ec 0%, #f3e6d4 100%); border-top:4px solid var(--gold); border-radius:44px 44px 0 0; box-shadow:0 -20px 50px rgba(40,20,10,0.35); }}
.issue {{ position:absolute; left:70px; top:1310px; font-weight:700; font-size:24px; letter-spacing:0.28em; color:var(--bronze2); }}
.issue b {{ color:var(--brick); }}
.ph {{ position:absolute; left:70px; right:70px; top:1365px; }}
.kick {{ display:inline-block; font-weight:700; font-size:26px; letter-spacing:0.2em; color:var(--gold2); background:var(--choc); padding:9px 20px; border-radius:40px; }}
.hl {{ font-family:"Playfair Display", serif; font-weight:700; font-size:86px; line-height:1.05; color:var(--choc); margin-top:22px; }}
.hl em {{ color:var(--bronze2); font-style:italic; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:30px; }}
.pill {{ display:flex; align-items:center; gap:12px; font-weight:700; font-size:32px; letter-spacing:0.04em; color:var(--choc); background:#fff; padding:16px 22px; border-radius:50px; border:3px solid var(--gold); box-shadow:0 8px 20px rgba(74,46,34,0.15); white-space:nowrap; }}
.pill .dot {{ width:18px; height:18px; border-radius:50%; background:var(--brick); flex:none; }}
.pill.ok {{ background:linear-gradient(90deg,var(--bronze1),var(--bronze2)); color:#fff; border-color:var(--gold2); }}
.half {{ position:absolute; top:0; width:538px; height:1300px; overflow:hidden; }}
.half img {{ position:absolute; top:-{FY + 40}px; width:1080px; height:1920px; object-fit:cover; }}
.tag {{ position:absolute; top:40px; font-weight:700; font-size:30px; letter-spacing:0.2em; padding:10px 22px; border-radius:40px; z-index:3; }}
.vline {{ position:absolute; left:536px; top:0; width:8px; height:1300px; background:linear-gradient(180deg,var(--gold2),var(--gold)); box-shadow:0 0 20px rgba(232,207,160,0.9); }}
.offer {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 25%, #fbf5ec 0%, #f6eee4 45%, #efe3d3 100%); }}
.o-h {{ position:absolute; left:0; right:0; top:300px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:96px; line-height:1.02; color:var(--choc); }}
.o-h em {{ color:var(--bronze2); }}
.seal {{ position:absolute; left:290px; top:560px; width:500px; height:500px; border-radius:50%; background:radial-gradient(circle at 35% 30%, #a06a3c 0%, #6b4226 55%, #3b2416 100%); border:8px solid var(--gold2); box-shadow:0 30px 70px rgba(40,20,10,0.45); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.seal .a {{ font-weight:700; font-size:30px; letter-spacing:0.26em; color:var(--gold2); }}
.seal .b {{ font-family:"Playfair Display", serif; font-weight:700; font-size:132px; line-height:1; background:linear-gradient(180deg,#fff3d6 0%,#e8cfa0 50%,#c9a46a 100%); -webkit-background-clip:text; background-clip:text; color:transparent; margin:10px 0; }}
.seal .c {{ font-weight:700; font-size:30px; color:#fff; }}
.strip {{ position:absolute; left:70px; right:70px; top:1130px; height:300px; border-radius:30px; background:#fff; border:3px solid var(--gold); display:flex; align-items:center; gap:26px; padding:20px; box-shadow:0 18px 40px rgba(74,46,34,0.2); }}
.strip img {{ width:280px; height:256px; object-fit:cover; border-radius:20px; }}
.s1t {{ font-weight:700; font-size:30px; letter-spacing:0.1em; color:var(--bronze2); }}
.s2t {{ font-family:"Playfair Display", serif; font-weight:700; font-size:62px; line-height:1.05; color:var(--choc); }}
.s3t {{ font-weight:700; font-size:28px; color:var(--brick); margin-top:8px; }}
.clients {{ position:absolute; left:70px; right:70px; top:1480px; display:flex; gap:20px; }}
.clients div {{ flex:1; height:300px; border-radius:22px; overflow:hidden; border:6px solid #fff; box-shadow:0 14px 30px rgba(74,46,34,0.25); }}
.clients img {{ width:100%; height:100%; object-fit:cover; }}
.cl-t {{ position:absolute; left:0; right:0; top:1800px; text-align:center; font-weight:700; font-size:28px; letter-spacing:0.2em; color:var(--bronze2); }}
.cta-logo {{ position:absolute; left:290px; top:380px; width:500px; }}
.cta-h {{ position:absolute; left:0; right:0; top:720px; text-align:center; font-family:"Playfair Display", serif; font-weight:700; font-size:100px; line-height:1.05; color:var(--choc); }}
.cta-h em {{ color:var(--bronze2); }}
.btn {{ position:absolute; left:160px; top:1060px; width:760px; height:150px; border-radius:80px; background:linear-gradient(90deg,var(--bronze1),var(--bronze2)); display:flex; align-items:center; justify-content:center; gap:22px; font-weight:700; font-size:52px; letter-spacing:0.08em; color:#fff; box-shadow:0 20px 50px rgba(74,46,34,0.4); }}
.addr {{ position:absolute; left:0; right:0; top:1260px; text-align:center; font-size:36px; letter-spacing:0.12em; color:var(--bronze2); font-weight:700; }}
.sweep {{ position:absolute; left:-500px; top:-200px; width:320px; height:1600px; background:linear-gradient(90deg, rgba(255,240,210,0) 0%, rgba(255,240,210,0.45) 50%, rgba(255,240,210,0) 100%); }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{r2(T)}" data-width="1080" data-height="1920">

<!-- KHUNG VIDEO (2/3 trên) -->
<div id="fr" class="frame">
  <div id="w-bef" class="full" style="position:absolute; inset:0"><video class="clip m" src="assets/v_bef.mp4" muted playsinline data-start="0" data-duration="2.75" data-track-index="1"></video></div>
  <div id="w-side" style="position:absolute; inset:0"><video class="clip m" src="assets/v_side.mp4" muted playsinline data-start="2.75" data-duration="2.85" data-track-index="1"></video></div>
  <div id="w-st" style="position:absolute; inset:0; transform-origin:540px 600px"><img class="clip m" src="assets/s11.3.png" alt="" data-start="5.6" data-duration="{r2(s3 - 5.6)}" data-track-index="1"></div>
  <svg id="circs" class="clip" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="2" style="position:absolute; left:0; top:0; width:1080px; height:1300px" viewBox="0 0 1080 1300">{"".join(circ(c, x, y, r) for c, x, y, r, _ in defects)}</svg>
  {"".join(f'<div id="w-{n}" style="position:absolute; inset:0"><video class="clip m" src="assets/{n}.mp4" muted playsinline data-start="{r2(st)}" data-duration="{r2(dd)}" data-track-index="1"></video></div>' for st, dd, n in a3)}
  <div style="position:absolute; left:0; top:0; width:1080px; height:260px; background:linear-gradient(180deg, rgba(30,15,5,0.55), rgba(30,15,5,0)); z-index:2"></div>
  <div id="sweep" class="sweep clip" data-start="{r2(s3)}" data-duration="1.4" data-track-index="3"></div>
  <div id="cmp" class="clip" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="2" style="position:absolute; inset:0; background:#2a1a10">
    <div id="hL" class="half" style="left:0"><img src="assets/s11.3.png" alt="" style="left:-270px"></div>
    <div id="hR" class="half" style="left:542px"><img src="assets/s22.6.png" alt="" style="left:-270px"></div>
    <div id="vl" class="vline"></div>
    <div class="tag" style="left:30px; top:170px; color:#fff; background:rgba(59,36,22,0.88)">BEFORE</div>
    <div class="tag" style="right:30px; top:170px; color:#3b2416; background:linear-gradient(90deg,#c9a46a,#e8cfa0)">AFTER</div>
  </div>
</div>

<!-- BẢNG CHỮ (1/3 dưới) -->
<div class="panel"></div>
<div class="issue clip" data-start="0" data-duration="{r2(s5)}" data-track-index="4">MERAH JOURNAL · <b>CASE 01</b> · MAXFILL FULL FACE</div>
<div id="p1" class="ph clip" data-start="0" data-duration="{r2(L1)}" data-track-index="5"><div class="kick">NO FILTER · NO MAKEUP</div><div class="hl">Her natural face,<br><em>before Maxfill</em></div></div>
<div id="p2" class="ph clip" data-start="{r2(s2)}" data-duration="{r2(L2)}" data-track-index="5"><div class="kick">WHAT MAXFILL WILL FIX</div>
  <div class="grid2">{"".join(f'<div id="q{i+1}" class="pill"><span class="dot"></span>{lab}</div>' for i, (_, _, _, _, lab) in enumerate(defects))}</div></div>
<div id="p3" class="ph clip" data-start="{r2(s3)}" data-duration="{r2(L3)}" data-track-index="5"><div class="hl" style="margin-top:0">Same girl,<br><em>30 minutes later</em></div>
  <div class="grid2">{"".join(f'<div id="k{i+1}" class="pill ok">{t}</div>' for i, t in enumerate(fixes))}</div></div>
<div id="p4" class="ph clip" data-start="{r2(s4)}" data-duration="{r2(L4)}" data-track-index="5"><div class="kick">SIDE BY SIDE</div><div class="hl">See the <em>difference</em></div></div>

<!-- ƯU ĐÃI -->
<div id="s5" class="clip offer" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="6">
  <div id="o-h" class="o-h">Your Christmas<br><em>glow-up</em></div>
  <div id="seal" class="seal"><div class="a">MAXFILL · STARTING FROM</div><div class="b">₱2,999</div><div class="c">40% OFF · until Nov 30</div></div>
  <div id="strip" class="strip"><img src="assets/qua_10k.jpg" alt=""><div><div class="s1t">+ CHRISTMAS GIFTS</div><div class="s2t">Up to ₱10,000</div><div class="s3t">Real ₱10,000 cash winner!</div></div></div>
  <div id="cls" class="clients"><div><img src="assets/5_ba.png" alt=""></div><div><img src="assets/6_ba.png" alt=""></div><div><img src="assets/7_ba.png" alt=""></div></div>
  <div class="cl-t">REAL MERAH CLIENTS</div>
</div>
<!-- CTA -->
<div id="s6" class="clip offer" data-start="{r2(s6)}" data-duration="{r2(L6)}" data-track-index="6">
  <img id="cta-logo" class="cta-logo" src="assets/logo.png" alt="MERAH Beauty">
  <div id="cta-h" class="cta-h">Book your<br><em>glow-up</em></div>
  <div id="cta-btn" class="btn"><span>💬</span>MESSAGE US NOW</div>
  <div id="cta-addr" class="addr">MERAH BEAUTY · MAKATI</div>
</div>
<img class="clip" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{r2(s5)}" data-track-index="7" style="position:absolute; left:40px; top:56px; width:210px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.7))">
<img class="clip" src="assets/logo_nau.png" alt="MERAH Beauty" data-start="{r2(s5)}" data-duration="{r2(L5)}" data-track-index="7" style="position:absolute; left:40px; top:56px; width:210px; z-index:9">

{"".join(f'<audio class="clip" src="assets/vo{i+1}.mp3" data-start="{r2(st + 0.1)}" data-duration="{r2(dur[i])}" data-volume="1" data-track-index="10"></audio>' for i, st in enumerate((s1, s2, s3, s4, s5, s6)))}
<audio class="clip" src="assets/music.mp3" data-start="0" data-duration="{r2(T)}" data-volume="0.2" data-fade-in="0.3" data-fade-out="1.5" data-track-index="11"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s2 + 0.3 + i * step)}" data-duration="0.5" data-volume="0.55" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="{r2(s3 - 0.4)}" data-duration="1.4" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s3 + 0.2)}" data-duration="1.2" data-volume="0.55" data-track-index="15"></audio>
{"".join(f'<audio class="clip" src="assets/sfx/pop.mp3" data-start="{r2(s3 + 1.6 + i * 1.1)}" data-duration="0.5" data-volume="0.5" data-track-index="{13 + i % 2}"></audio>' for i in range(4))}
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s4 - 0.1)}" data-duration="0.57" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/impact-bass-1.mp3" data-start="{r2(s5)}" data-duration="1.0" data-volume="0.5" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/chime.mp3" data-start="{r2(s5 + 1.0)}" data-duration="1.2" data-volume="0.5" data-track-index="13"></audio>
<audio class="clip" src="assets/sfx/sparkle.mp3" data-start="{r2(s5 + 3.0)}" data-duration="1.2" data-volume="0.45" data-track-index="15"></audio>
<audio class="clip" src="assets/sfx/whoosh.mp3" data-start="{r2(s6 - 0.1)}" data-duration="0.57" data-volume="0.45" data-track-index="12"></audio>
<audio class="clip" src="assets/sfx/click.mp3" data-start="{r2(s6 + 1.4)}" data-duration="0.4" data-volume="0.6" data-track-index="13"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }}); const X = "expo.out";
tl.fromTo("#p1 .kick", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.1);
tl.fromTo("#p1 .hl", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, 0.25);
// khuyết điểm: vòng + nhãn theo lời đọc
{"".join(f'tl.to("#{c}", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.5, ease: "power2.out" }}, {r2(s2 + 0.3 + i * step)}); tl.fromTo("#q{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s2 + 0.35 + i * step)});' for i, (c, *_r) in enumerate(defects))}
tl.fromTo("#p2 .kick", {{ opacity:0 }}, {{ opacity:1, duration:0.3 }}, {r2(s2)});
// lấy nét mờ XẤU -> ĐẸP
tl.to("#w-st", {{ filter:"blur(14px)", duration:0.3, ease:"power2.in" }}, {r2(s3 - 0.3)});
tl.fromTo("#w-v_aft1", {{ filter:"blur(14px)", scale:1.1 }}, {{ filter:"blur(0px)", scale:1.0, duration:0.5, ease:"power2.out" }}, {r2(s3)});
tl.fromTo("#sweep", {{ x:0 }}, {{ x:1900, duration:1.2, ease:"power2.inOut" }}, {r2(s3 + 0.2)});
tl.fromTo("#p3 .hl", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s3 + 0.2)});
{"".join(f'tl.fromTo("#k{i+1}", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.4, ease:X }}, {r2(s3 + 1.6 + i * 1.1)});' for i in range(4))}
// so sánh
tl.fromTo("#hL", {{ x:-540 }}, {{ x:0, duration:0.6, ease:X }}, {r2(s4)});
tl.fromTo("#hR", {{ x:540 }}, {{ x:0, duration:0.6, ease:X }}, {r2(s4)});
tl.fromTo("#vl", {{ scaleY:0, transformOrigin:"50% 50%" }}, {{ scaleY:1, duration:0.6, ease:X }}, {r2(s4 + 0.3)});
tl.fromTo("#hL img, #hR img", {{ scale:1.0 }}, {{ scale:1.08, duration:{r2(L4 - 0.6)}, ease:"none" }}, {r2(s4 + 0.6)});
tl.fromTo("#p4 .hl", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s4 + 0.3)});
// ưu đãi
tl.fromTo("#o-h", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, {r2(s5 + 0.1)});
tl.fromTo("#seal", {{ opacity:0, scale:0.6, rotation:-12 }}, {{ opacity:1, scale:1, rotation:0, duration:0.7, ease:"back.out(1.8)" }}, {r2(s5 + 0.6)});
tl.fromTo("#strip", {{ opacity:0, y:80 }}, {{ opacity:1, y:0, duration:0.55, ease:X }}, {r2(s5 + 2.6)});
tl.fromTo("#cls div", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.5, ease:X, stagger:0.15 }}, {r2(s5 + 4.0)});
// CTA
tl.fromTo("#cta-logo", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s6 + 0.05)});
tl.fromTo("#cta-h", {{ opacity:0, scale:0.85 }}, {{ opacity:1, scale:1, duration:0.5, ease:"back.out(1.8)" }}, {r2(s6 + 0.2)});
tl.fromTo("#cta-btn", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, {r2(s6 + 1.0)});
tl.fromTo("#cta-addr", {{ opacity:0 }}, {{ opacity:1, duration:0.4 }}, {r2(s6 + 1.4)});
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>
'''
io.open(W + "/index.html", "w", encoding="utf-8", newline="\n").write(html)
print("T=%.2f" % T, [r2(x) for x in (s1, s2, s3, s4, s5, s6)])
