"""Tạo giọng đọc bằng ElevenLabs cho video MERAH. KHÔNG in khoá API.
Khoá: biến môi trường ELEVENLABS_API_KEY (đám mây) hoặc file C:\\MERAH\\.bao-mat\\elevenlabs.txt (máy, người dùng tự dán).

python giong_doc.py voices                          # liệt kê giọng (tên, id, giới tính, giọng vùng)
python giong_doc.py doc <loi_doc.txt> <ra.mp3> [--voice ID] [--speed 1.0] [--kieu tuoi|vua|sang] [--model eleven_v3]
   --kieu tuoi = nhấn nhá, trẻ trung (stability thấp, style cao) cho quảng cáo; eleven_v3 hỗ trợ thẻ cảm xúc như [excited] [laughs] trong lời đọc
   - Mỗi dòng trống trong loi_doc.txt = 1 đoạn; tạo thêm <ra>_doan.json ghi thời lượng từng đoạn để canh chữ/cảnh.
python giong_doc.py nghe <video_hoac_audio> <ra.txt>        # chép lời thoại gốc (ElevenLabs Speech-to-Text, scribe_v1) để hiểu ý video SPY
Giọng mặc định MERAH: đặt trong tai-nguyen/giong-doc.md (VOICE_ID) sau khi người dùng chọn.
"""
import json, os, re, subprocess, sys
import requests

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"


def key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k:
        p = r"C:\MERAH\.bao-mat\elevenlabs.txt"
        if os.path.exists(p):
            k = open(p, encoding="utf-8").read().strip()
    if not k:
        sys.exit("LỖI: chưa có khoá ElevenLabs (ELEVENLABS_API_KEY hoặc C:\\MERAH\\.bao-mat\\elevenlabs.txt)")
    return k


def default_voice():
    p = os.path.join(os.path.dirname(__file__), "..", "giong-doc.md")
    if os.path.exists(p):
        m = re.search(r"VOICE_ID:\s*([A-Za-z0-9]+)", open(p, encoding="utf-8").read())
        if m:
            return m.group(1)
    return "21m00Tcm4TlvDq8ikWAM"  # Rachel – giọng nữ ấm, dự phòng


def voices():
    r = requests.get(f"{API}/voices", headers={"xi-api-key": key()}, timeout=30)
    r.raise_for_status()
    for v in r.json().get("voices", []):
        lab = v.get("labels", {})
        print(f"{v['name']:<28} {v['voice_id']}  {lab.get('gender','')} {lab.get('accent','')} {lab.get('description','')}")


KIEU={"tuoi":(0.3,0.75,0.7),"vua":(0.45,0.8,0.35),"sang":(0.6,0.8,0.15)}


def tts(text, out, voice, speed, kieu="vua", model=MODEL):
    stb, sim, sty = KIEU.get(kieu, KIEU["vua"])
    r = requests.post(f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128",
                      headers={"xi-api-key": key(), "Content-Type": "application/json"},
                      json={"text": text, "model_id": model,
                            "voice_settings": {"stability": stb, "similarity_boost": sim, "style": sty, "speed": speed}},
                      timeout=120)
    if not r.ok:
        sys.exit(f"LỖI ElevenLabs {r.status_code}: {r.text[:300]}")
    open(out, "wb").write(r.content)


def dur(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    try:
        return float(o.stdout.strip())
    except ValueError:
        return 0.0


def doc(src, out, voice, speed, kieu="vua", model=MODEL):
    parts = [p.strip() for p in re.split(r"\n\s*\n", open(src, encoding="utf-8").read()) if p.strip()]
    tmp, info = [], []
    for i, t in enumerate(parts):
        f = f"{out}.doan{i+1}.mp3"
        tts(t, f, voice, speed, kieu, model); tmp.append(f); info.append({"doan": i + 1, "loi": t, "giay": round(dur(f), 2)})
    lst = out + ".list.txt"
    open(lst, "w", encoding="utf-8").write("".join(f"file '{os.path.abspath(f)}'\n" for f in tmp))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    json.dump(info, open(os.path.splitext(out)[0] + "_doan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in tmp + [lst]:
        os.remove(f)
    print(f"Xong {out}: {len(parts)} đoạn, tổng {sum(x['giay'] for x in info):.1f}s")


def nghe(src, out):
    """Chép lời (speech-to-text). Chỉ để hiểu nội dung – kịch bản MERAH phải viết lại bằng lời mới."""
    tmp = out + ".tmp.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", tmp], check=True)
    with open(tmp, "rb") as f:
        r = requests.post(f"{API}/speech-to-text", headers={"xi-api-key": key()}, data={"model_id": "scribe_v1"}, files={"file": ("a.mp3", f, "audio/mpeg")}, timeout=300)
    os.remove(tmp)
    if not r.ok:
        sys.exit(f"LỖI ElevenLabs STT {r.status_code}: {r.text[:300]}")
    j = r.json(); open(out, "w", encoding="utf-8").write(j.get("text", "")); print(f"Xong {out}: ngôn ngữ {j.get('language_code','?')}, {len(j.get('text',''))} ký tự")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "voices":
        voices()
    elif a[0] == "doc":
        v = a[a.index("--voice") + 1] if "--voice" in a else default_voice()
        sp = float(a[a.index("--speed") + 1]) if "--speed" in a else 1.0
        kieu = a[a.index("--kieu") + 1] if "--kieu" in a else "vua"
        mdl = a[a.index("--model") + 1] if "--model" in a else MODEL
        doc(a[1], a[2], v, sp, kieu, mdl)
    elif a[0] == "nghe":
        nghe(a[1], a[2])
