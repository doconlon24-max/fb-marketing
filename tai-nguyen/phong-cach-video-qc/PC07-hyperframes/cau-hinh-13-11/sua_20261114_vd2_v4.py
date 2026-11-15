import io, re
W = "C:/tmp/QC-20261114-VD2"
css = re.search(r"<style>(.*?)</style>", io.open("C:/MERAH/he-thong/tai-nguyen/phong-cach-video-qc/PC07-hyperframes/index.html", encoding="utf-8").read(), re.S).group(1)
HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>%s
.top { position:absolute; left:70px; right:70px; top:170px; text-align:center; }
.bot { position:absolute; left:70px; right:70px; top:1560px; text-align:center; }
.band { position:absolute; left:0; top:1632px; width:1080px; height:288px; z-index:4; background:linear-gradient(180deg,#4a2d1b 0%%,#3b2416 100%%); border-top:3px solid #c9a46a }
.logo { position:absolute; left:36px; top:34px; width:220px; z-index:9; filter:drop-shadow(0 2px 8px rgba(30,15,5,0.6)) }
.tg { position:absolute; font-family:Montserrat; font-weight:700; font-size:34px; letter-spacing:0.2em; padding:12px 28px; border-radius:40px; z-index:6; box-shadow:0 8px 24px rgba(30,15,5,0.45) }
.tb { background:rgba(59,36,22,0.88); color:#fff3d6; border:2px solid #c9a46a }
.ta { background:linear-gradient(90deg,#c9a46a,#e8cfa0); color:#3b2416 }
</style></head><body>
''' % css
TAIL = '\nwindow.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;\n</script></body></html>\n'

# ---------- HOOK 0–2.8s ----------
T = 2.8
hook = HEAD + f'''<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<video class="clip" src="assets/v_nen.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="1" style="position:absolute; left:0; top:0; width:1080px; height:1632px; object-fit:cover; z-index:0"></video>
<div id="hk" style="position:absolute; left:0; top:400px; width:1080px; height:1232px; overflow:hidden; z-index:1; -webkit-mask-image:linear-gradient(180deg, transparent 0px, #000 260px); mask-image:linear-gradient(180deg, transparent 0px, #000 260px)">
  <div id="hk-z" style="position:absolute; left:0; top:100px; width:1080px; height:1126px; transform-origin:540px 520px">
    <video class="clip" src="assets/v_hook.mp4" muted playsinline data-start="0" data-duration="{T}" data-track-index="2" style="position:absolute; left:0; top:0; width:1080px; height:1126px"></video>
  </div>
  <div id="hk-line" style="position:absolute; left:537px; top:200px; width:6px; height:1032px; background:linear-gradient(180deg, rgba(232,207,160,0), #e8cfa0 15%, #c9a46a); box-shadow:0 0 18px rgba(232,207,160,0.8); transform-origin:50% 0%"></div>
</div>
<div id="tb" class="tg tb" style="left:60px; top:1530px">BEFORE</div>
<div id="ta" class="tg ta" style="right:60px; top:1530px">AFTER</div>
<div class="band"></div>
<div id="s1" class="clip full" data-start="0" data-duration="{T}" data-track-index="3" style="z-index:5">
  <div class="shade-top" style="height:700px; background:linear-gradient(180deg, rgba(40,22,12,0.7) 0%, rgba(40,22,12,0.3) 60%, rgba(40,22,12,0) 100%)"></div>
  <div class="top"><div id="s1-k" class="kick">MAXFILL · FULL FACE</div><div id="s1-a" class="big" style="margin-top:22px; font-size:82px">Tired, hollow<br><em>&amp; older-looking?</em></div></div>
  <div class="bot" style="top:1700px"><div class="serif" style="font-weight:700; font-size:54px; color:#fff3d6">Maxfill <em style="color:#e8cfa0">from ₱2,999</em></div><div style="font-family:Montserrat; font-weight:700; font-size:24px; letter-spacing:6px; color:#e8cfa0; margin-top:10px">MERAH BEAUTY · MAKATI</div></div>
</div>
<img class="clip logo" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{T}" data-track-index="4">
</div>
<script>
const tl = gsap.timeline({{ paused:true }}); const X = "expo.out";
tl.fromTo("#hk-z", {{ scale:1.08 }}, {{ scale:1.0, duration:0.7, ease:"power3.out" }}, 0);
tl.to("#hk-z", {{ scale:1.05, duration:2.1, ease:"none" }}, 0.7);
tl.fromTo("#hk-line", {{ scaleY:0 }}, {{ scaleY:1, duration:0.6, ease:"power2.out" }}, 0.15);
tl.fromTo("#tb", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, ease:X }}, 0.5);
tl.fromTo("#ta", {{ opacity:0, x:40 }}, {{ opacity:1, x:0, duration:0.4, ease:X }}, 0.7);
tl.fromTo("#s1-k", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.1);
tl.fromTo("#s1-a", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.5, ease:X }}, 0.25);
tl.to("#tb, #ta", {{ opacity:0, duration:0.2 }}, 2.6);''' + TAIL
io.open(W + "/hf_hook/index.html", "w", encoding="utf-8", newline="\n").write(hook)

# ---------- SO SÁNH 4.5s ----------
T = 4.5
ss = HEAD + f'''<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" style="background:#3b2416">
<div id="pb" style="position:absolute; left:0; top:0; width:1080px; height:816px; overflow:hidden; z-index:1">
  <img id="ib" class="clip" src="assets/bef.png" alt="" data-start="0" data-duration="{T}" data-track-index="1" style="position:absolute; left:0; top:0; width:1080px; height:816px; transform-origin:540px 420px">
</div>
<div id="pa" style="position:absolute; left:0; top:816px; width:1080px; height:816px; overflow:hidden; z-index:2">
  <img id="ia" class="clip" src="assets/aft.png" alt="" data-start="0" data-duration="{T}" data-track-index="2" style="position:absolute; left:0; top:0; width:1080px; height:816px; transform-origin:540px 420px">
</div>
<div id="ln" style="position:absolute; left:0; top:812px; width:1080px; height:8px; z-index:3; background:linear-gradient(90deg,#c9a46a,#fff3d6 50%,#c9a46a); box-shadow:0 0 22px rgba(232,207,160,0.9); transform-origin:50% 50%"></div>
<div id="tb" class="tg tb" style="right:50px; top:60px">BEFORE</div>
<div id="ta" class="tg ta" style="right:50px; top:876px">AFTER</div>
<div class="band"></div>
<div class="bot" style="top:1712px; z-index:5"><div id="ba-h" class="big" style="font-size:64px">See the <em>difference</em></div></div>
<img class="clip logo" src="assets/logo_kem.png" alt="MERAH Beauty" data-start="0" data-duration="{T}" data-track-index="4">
</div>
<script>
const tl = gsap.timeline({{ paused:true }}); const X = "expo.out";
tl.fromTo("#pa", {{ x:1080 }}, {{ x:0, duration:0.55, ease:"power3.out" }}, 0.25);
tl.fromTo("#ln", {{ scaleX:0 }}, {{ scaleX:1, duration:0.5, ease:"power2.out" }}, 0.6);
tl.fromTo("#tb", {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:0.35, ease:X }}, 0.4);
tl.fromTo("#ta", {{ opacity:0, y:-20 }}, {{ opacity:1, y:0, duration:0.35, ease:X }}, 0.8);
tl.fromTo("#ba-h", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:0.45, ease:X }}, 0.2);
tl.fromTo("#ib, #ia", {{ scale:1.0 }}, {{ scale:1.06, duration:{T}, ease:"none" }}, 0);''' + TAIL
io.open(W + "/hf_ss/index.html", "w", encoding="utf-8", newline="\n").write(ss)
print("ok")
