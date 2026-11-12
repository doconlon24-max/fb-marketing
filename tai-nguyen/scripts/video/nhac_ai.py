"""Nhạc nền thẩm mỹ tạo bằng AI (ElevenLabs Music – gói trả phí có quyền dùng thương mại) khi thư viện
tai-nguyen/am-nhac/tham-my chưa có bài sếp tải. Bài tạo ra được LƯU vào thư viện (ai_<kieu>.mp3) để dùng lại.
python nhac_ai.py <kieu> [giay]       kieu: sang | tuoi | nhe
Không in khoá. Lỗi -> thoát mã 1 (spy_merah.py sẽ dùng nhạc dự phòng)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
THU_VIEN = os.path.abspath(os.path.join(HERE, "..", "..", "am-nhac", "tham-my"))
PROMPT = {
    "sang": "Elegant luxury beauty clinic commercial music, warm deep house groove, soft piano chords, airy female vocal chops without lyrics, "
            "polished and glamorous, confident, 118 bpm, clean modern mix, instrumental, no lyrics",
    "tuoi": "Upbeat bright pop commercial for skincare and aesthetic clinic, feel-good, light claps, plucky synth, shimmering bells, "
            "fresh and youthful, 124 bpm, catchy hook, instrumental, no lyrics",
    "nhe": "Soft chic lo-fi chill beat for spa and beauty ad, gentle Rhodes piano, warm bass, subtle sparkle textures, calm and premium, "
           "92 bpm, instrumental, no lyrics",
}


def tao(kieu="sang", giay=40):
    import requests, giong_doc as G
    os.makedirs(THU_VIEN, exist_ok=True); out = os.path.join(THU_VIEN, f"ai_{kieu}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 50000:
        return out
    r = requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                      headers={"xi-api-key": G.key(), "Content-Type": "application/json"},
                      json={"prompt": PROMPT.get(kieu, PROMPT["sang"]), "music_length_ms": int(giay * 1000)}, timeout=300)
    if not r.ok or len(r.content) < 50000:
        sys.exit(f"LỖI ElevenLabs Music {r.status_code}: {r.text[:200] if not r.ok else 'file quá nhỏ'}")
    open(out, "wb").write(r.content)
    with open(os.path.join(THU_VIEN, "README.md"), "a", encoding="utf-8") as f:
        f.write(f"| ai_{kieu}.mp3 | ElevenLabs Music (AI, gói trả phí) – prompt: {PROMPT.get(kieu)[:60]}… | {kieu} | Quyền thương mại theo gói ElevenLabs |\n")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    print(tao(a[0] if a else "sang", float(a[1]) if len(a) > 1 else 40))
