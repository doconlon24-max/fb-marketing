"""Dựng nhiều bài MERAH từ 3 template: A (tối giản sang trọng), B (công nghệ), R (review).
python make_posts.py  -> xuất out/POST_xx.png
"""
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PHONE = "{{SO_DIEN_THOAI}}"

A = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1350px;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:url(../{bg}) center/cover no-repeat}
.c::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(248,241,232,.97) 0%,rgba(248,241,232,.9) 22%,rgba(248,241,232,.55) 34%,rgba(248,241,232,0) 46%)}
.c::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(40,24,16,.55) 0%,rgba(40,24,16,0) 16%)}
.top{position:absolute;top:70px;left:0;right:0;text-align:center;z-index:2}
.k{font:400 22px "Gill Sans MT";letter-spacing:.62em;padding-left:.62em;color:#6b4a36}
h1{margin:26px 0 0;font:400 {size}px/1.02 "Bodoni MT",serif;background:linear-gradient(180deg,#4a2e22,#6e4630 55%,#9a6a3e);-webkit-background-clip:text;color:transparent}
.s{margin-top:16px;font:italic 400 38px Garamond,serif;color:#a07443}
.d{margin:22px auto 0;display:flex;align-items:center;justify-content:center;gap:18px}
.d i{width:190px;height:1px;background:linear-gradient(90deg,transparent,#b8905c)}.d i:last-child{transform:scaleX(-1)}
.d b{width:9px;height:9px;background:#b8905c;transform:rotate(45deg)}
.f{position:absolute;bottom:40px;left:0;right:0;text-align:center;z-index:2;font:400 21px "Gill Sans MT";letter-spacing:.32em;color:#f6eee4}
.f span{opacity:.6;margin:0 14px}
</style></head><body><div class="c"><div class="top"><div class="k">{kicker}</div><h1>{title}</h1>
<div class="s">{sub}</div><div class="d"><i></i><b></b><i></i></div></div>
<div class="f">MAKATI CITY<span>·</span>{phone}</div></div></body></html>"""

B = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1350px;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;font-family:"Segoe UI";background:url(../{bg}) center/cover no-repeat}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,14,9,.78),rgba(22,14,9,.25) 20%,rgba(22,14,9,0) 34%),linear-gradient(0deg,rgba(22,14,9,.92),rgba(22,14,9,.55) 26%,rgba(22,14,9,0) 46%)}
.g{position:absolute;inset:0;opacity:.07;background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);background-size:90px 90px}
.h{position:absolute;top:52px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center}
.h img{height:74px}
.p{font:600 17px "Segoe UI";letter-spacing:.24em;color:#f3e2c4;padding:12px 22px;border-radius:40px;border:1px solid rgba(232,207,160,.45);background:rgba(255,255,255,.08);backdrop-filter:blur(10px)}
.p b{display:inline-block;width:8px;height:8px;border-radius:50%;background:#e8cfa0;margin-right:12px;box-shadow:0 0 12px #e8cfa0;vertical-align:2px}
.hud{position:absolute;left:{hx}px;top:{hy}px;width:{hw}px;height:{hh}px}
.hud i{position:absolute;width:44px;height:44px;border:2px solid rgba(232,207,160,.9)}
.hud i:nth-child(1){left:0;top:0;border-right:0;border-bottom:0}.hud i:nth-child(2){right:0;top:0;border-left:0;border-bottom:0}
.hud i:nth-child(3){left:0;bottom:0;border-right:0;border-top:0}.hud i:nth-child(4){right:0;bottom:0;border-left:0;border-top:0}
.hud span{position:absolute;top:-46px;left:0;font:500 15px Consolas;letter-spacing:.18em;color:#f3e2c4;padding:7px 12px;border-radius:6px;background:rgba(22,14,9,.55);backdrop-filter:blur(6px);white-space:nowrap}
.cd{position:absolute;left:60px;right:60px;bottom:56px;padding:30px 40px;border-radius:26px;background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(18px);box-shadow:0 20px 60px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25)}
.l{font:500 16px Consolas;letter-spacing:.22em;color:#d9bf92}
h1{margin:12px 0 0;font:300 56px/1.08 "Segoe UI Light";color:#fff}
h1 em{font-style:normal;font-weight:600;background:linear-gradient(90deg,#f3dcae,#c9a46a);-webkit-background-clip:text;color:transparent}
.r{margin-top:22px;display:flex;border-top:1px solid rgba(255,255,255,.18);padding-top:24px}
.r div{flex:1;padding-right:18px}.r div+div{padding-left:24px;border-left:1px solid rgba(255,255,255,.14)}
.r small{display:block;font:500 13px Consolas;letter-spacing:.2em;color:#bfa883}
.r strong{display:block;margin-top:8px;font:600 26px "Segoe UI";color:#fff}
.bar{margin-top:26px;height:4px;border-radius:4px;background:rgba(255,255,255,.12)}
.bar b{display:block;width:72%;height:100%;background:linear-gradient(90deg,#c9a46a,#f3dcae);box-shadow:0 0 14px #e8cfa0}
</style></head><body><div class="c"><div class="sh"></div><div class="g"></div>
<div class="h"><img src="../logo_light.png"><div class="p"><b></b>{pill}</div></div>
<div class="hud"><i></i><i></i><i></i><i></i><span>{hud}</span></div>
<div class="cd"><div class="l">{label}</div><h1>{h1}</h1><div class="r">{rows}</div><div class="bar"><b></b></div></div>
</div></body></html>"""

R = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1350px;overflow:hidden}
.c{position:relative;width:1080px;height:1350px;background:url(../{bg}) center/cover no-repeat}
.c::before{content:"";position:absolute;inset:0;background:rgba(246,238,228,.55)}
.top{position:absolute;top:66px;left:0;right:0;text-align:center}
.top img{height:96px}
.k{margin-top:22px;font:400 20px "Gill Sans MT";letter-spacing:.6em;padding-left:.6em;color:#6b4a36}
h1{margin:18px 0 0;font:400 76px/1.05 "Bodoni MT",serif;background:linear-gradient(180deg,#4a2e22,#9a6a3e);-webkit-background-clip:text;color:transparent}
.cd{position:absolute;left:84px;right:84px;top:440px;padding:64px 70px 54px;border-radius:30px;background:rgba(255,252,247,.86);
  border:1px solid rgba(184,144,92,.35);box-shadow:0 30px 80px rgba(74,46,34,.18);backdrop-filter:blur(8px)}
.q{position:absolute;top:-58px;left:56px;font:400 190px/1 "Bodoni MT",serif;color:#c9a46a}
.st{font-size:34px;letter-spacing:.18em;color:#c9a46a}
.tx{margin-top:24px;font:400 39px/1.5 Garamond,serif;color:#4a2e22}
.au{margin-top:30px;display:flex;align-items:center;gap:18px;font:400 22px "Gill Sans MT";letter-spacing:.14em;color:#8a6a4e}
.au i{width:60px;height:1px;background:#b8905c}
.f{position:absolute;bottom:46px;left:0;right:0;text-align:center;font:400 21px "Gill Sans MT";letter-spacing:.32em;color:#6b4a36}
.f span{opacity:.6;margin:0 14px}
</style></head><body><div class="c"><div class="top"><img src="../logo_dark.png"><div class="k">{kicker}</div><h1>{title}</h1></div>
<div class="cd"><div class="q">“</div><div class="st">★★★★★</div><div class="tx">{quote}</div><div class="au"><i></i>{author}</div></div>
<div class="f">MAKATI CITY<span>·</span>{phone}</div></div></body></html>"""


def rows(items):
    return "".join(f"<div><small>{k}</small><strong>{v}</strong></div>" for k, v in items)


POSTS = [
    ("POST_01", A, dict(bg="bg_lucky_warm.jpg", kicker="MERAH BEAUTY", title="Lucky Draw,<br>Lucky You", size=92,
                        sub="Christmas Lucky Draw at Merah Makati")),
    ("POST_02", B, dict(bg="bg_p14.jpg", pill="CHRISTMAS LUCKY DRAW", hud="LUCKY DRAW · WINNER 02",
                        hx=300, hy=395, hw=480, hh=335, label="MERAH LOUNGE / LUCKY DRAW",
                        h1="Another lucky winner,<br><em>another happy smile.</em>",
                        rows=rows([("PRIZE", "Wallet + Lipstick"), ("LOCATION", "Makati City"), ("BOOK", PHONE)]))),
    ("POST_03", A, dict(bg="bg_p11.jpg", kicker="MERAH BEAUTY", title="Thank You for<br>Choosing Merah", size=84,
                        sub="Every visit, a little moment of care")),
    ("POST_04", B, dict(bg="bg_p0.jpg", pill="INSIDE MERAH LOUNGE", hud="MERAH LOUNGE · MAKATI",
                        hx=120, hy=470, hw=850, hh=380, label="MERAH DIARY / A DAY AT MERAH",
                        h1="A calm space,<br><em>before every glow.</em>",
                        rows=rows([("VISIT", "45 EDSA Bangkal"), ("CITY", "Makati"), ("BOOK", PHONE)]))),
    ("POST_05", R, dict(bg="bg_review.jpg", kicker="REAL WORDS · REAL CLIENTS", title="From Our Clients",
                        quote="It was my first time having someone touch my face for a beauty treatment, and I'm so glad "
                              "I found Merah Beauty in Makati! The staff were very friendly, accommodating, and attentive "
                              "throughout the entire process. They made me feel comfortable and well taken care of. "
                              "Highly recommended!",
                        author="JOAN P. · GOOGLE REVIEW")),
]


def main():
    for name, tpl, p in POSTS:
        html = tpl
        for k, v in {**p, "phone": PHONE}.items():
            html = html.replace("{" + k + "}", str(v))
        f = OUT / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1080,1350", "--virtual-time-budget=3000", f"--screenshot={OUT / (name + '.png')}",
                        f.as_uri()], capture_output=True)
        print("rendered", name)


if __name__ == "__main__":
    main()
