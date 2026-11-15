"""TẢI TƯ LIỆU PHONG CÁCH cho máy mới (để video/ảnh dựng ra giống máy MERAH) – không tốn token.
  python tai-nguyen/scripts/tai_tu_lieu_phong_cach.py              # kiểm tra + tải phần thiếu
  python tai-nguyen/scripts/tai_tu_lieu_phong_cach.py --logo D:/logo.png   # đặt logo thương hiệu (tạo đủ 3 bản nâu/kem/vàng)
Làm gì:
  1. Nhạc nền: tải lại đúng các bài Mixkit (giấy phép Mixkit Free: dùng cho bài mạng xã hội + quảng cáo online) TỪ CHÍNH MIXKIT
     theo danh sách id bên dưới vào tai-nguyen/am-nhac/tham-my/ (không phát tán lại file nhạc).
  2. Kiểm tra SFX (skill media-use), font (Cinzel, Cormorant Garamond, Montserrat – giấy phép OFL), bìa phong cách.
  3. Logo: chép logo của bạn thành các tên mà script dựng ảnh/video dùng (tai-nguyen/thuong-hieu/logo/).
In bảng ĐỦ / THIẾU từng mục.
"""
import argparse, os, shutil, sys, urllib.request

KHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NHAC = os.path.join(KHO, "tai-nguyen", "am-nhac", "tham-my")
MIXKIT = {  # tên file : id Mixkit (https://mixkit.co/free-stock-music/)
    "mixkit_dance_karma_1183.mp3": 1183, "mixkit_dance_like-there-no-tomorrow_1095.mp3": 1095,
    "mixkit_dance_one-more-dance_288.mp3": 288, "mixkit_disco_disco-aint-old-school_935.mp3": 935,
    "mixkit_funk_funkee-monkeee_1140.mp3": 1140, "mixkit_funk_gimme-that-groove_872.mp3": 872,
    "mixkit_funk_midnight-funk_1147.mp3": 1147, "mixkit_hiphop_hip-hop-02_738.mp3": 738,
    "mixkit_hiphop_nba-type_403.mp3": 403, "mixkit_pop_island-beat_250.mp3": 250,
    "mixkit_trap_trap-hamza_267.mp3": 267, "mixkit_xmas_lets-all-dance-this-christmas_911.mp3": 911,
}
SFX = os.path.join(KHO, ".claude", "skills", "media-use", "audio", "assets", "sfx")
SFX_CAN = ["pop.mp3", "whoosh.mp3", "whoosh-short.mp3", "whoosh-cinematic.mp3", "sparkle.mp3", "riser.mp3", "impact-bass-1.mp3", "chime.mp3"]
FONT = os.path.join(KHO, "tai-nguyen", "thuong-hieu", "font")
FONT_CAN = ["Cinzel.ttf", "CormorantGaramond-Italic.ttf", "Montserrat.ttf"]
LOGO = os.path.join(KHO, "tai-nguyen", "thuong-hieu", "logo")
LOGO_CAN = ["LOGO_MR_nau_tach_nen.png", "LOGO_MR_nho_kem_trong_suot.png", "LOGO_MR_vang_nau_trong_suot.png"]


def tai(url, dich):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dich + ".tmp", "wb") as o:
        shutil.copyfileobj(r, o)
    os.replace(dich + ".tmp", dich)


def dat_logo(src):
    from PIL import Image
    os.makedirs(LOGO, exist_ok=True)
    im = Image.open(src).convert("RGBA")
    for ten in LOGO_CAN:
        im.save(os.path.join(LOGO, ten))
    print("đã đặt logo:", ", ".join(LOGO_CAN), "(muốn bản sáng/tối khác nhau thì thay từng tệp)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo")
    a = ap.parse_args()
    if a.logo:
        dat_logo(a.logo)
    os.makedirs(NHAC, exist_ok=True)
    bang = []
    for ten, mid in MIXKIT.items():
        p = os.path.join(NHAC, ten)
        if not os.path.exists(p) or os.path.getsize(p) < 100_000:
            try:
                tai(f"https://assets.mixkit.co/music/{mid}/{mid}.mp3", p)
                bang.append(("nhạc", ten, "VỪA TẢI"))
            except Exception as e:
                bang.append(("nhạc", ten, f"THIẾU – {str(e)[:60]}"))
        else:
            bang.append(("nhạc", ten, "ĐỦ"))
    for nhom, d, ds in (("sfx", SFX, SFX_CAN), ("font", FONT, FONT_CAN), ("logo", LOGO, LOGO_CAN)):
        for ten in ds:
            bang.append((nhom, ten, "ĐỦ" if os.path.exists(os.path.join(d, ten)) else "THIẾU"))
    for nhom, ten, tt in bang:
        print(f"{nhom:5} {tt:12} {ten}")
    thieu = [b for b in bang if b[2].startswith("THIẾU")]
    print(f"\nKẾT QUẢ: {len(bang) - len(thieu)}/{len(bang)} đủ." + (" Còn thiếu: " + ", ".join(t[1] for t in thieu) if thieu else " Đủ hết."))
    if any(t[0] == "logo" for t in thieu):
        print("→ Logo: chạy lại với --logo <đường dẫn logo PNG nền trong suốt của bạn>.")
    sys.exit(1 if thieu else 0)


if __name__ == "__main__":
    main()
