"""Tạo giọng đọc bằng ElevenLabs cho video MERAH. KHÔNG in khoá API.
Khoá: biến môi trường ELEVENLABS_API_KEY (đám mây) hoặc file C:\\MERAH\\.bao-mat\\elevenlabs.txt (máy, người dùng tự dán).

python giong_doc.py voices                          # liệt kê giọng (tên, id, giới tính, giọng vùng)
python giong_doc.py doc <loi_doc.txt> <ra.mp3> [--voice ID] [--speed 1.0] [--kieu tuoi|vua|sang] [--model eleven_v3]
   --kieu tuoi = nhấn nhá, trẻ trung (stability thấp, style cao) cho quảng cáo; eleven_v3 hỗ trợ thẻ cảm xúc như [excited] [laughs] trong lời đọc
   - Mỗi dòng trống trong loi_doc.txt = 1 đoạn; tạo thêm <ra>_doan.json ghi thời lượng từng đoạn để canh chữ/cảnh.
python giong_doc.py nghe <video_hoac_audio> <ra.txt>        # chép lời thoại gốc (ElevenLabs Speech-to-Text, scribe_v1) để hiểu ý video SPY
MIỄN PHÍ (không cần khoá): thêm --nguon edge  -> dùng giọng Microsoft Edge (gói `pip install edge-tts`; dự phòng khi Edge lỗi: `pip install gTTS`).
   Không có khoá ElevenLabs thì script TỰ chuyển sang edge. Đặt GIONG_NGUON=edge để luôn dùng bản miễn phí.
   python giong_doc.py voices --nguon edge [vi|en|fil|...]     # liệt kê giọng miễn phí theo ngôn ngữ
   Giọng edge: --voice vi-VN-HoaiMyNeural (hoặc biến GIONG_EDGE); bỏ trống thì tự chọn theo ngôn ngữ lời đọc.
   `nghe` không có khoá: dùng faster-whisper / whisper nếu máy đã cài (`pip install faster-whisper`).
Giọng mặc định MERAH: đặt trong tai-nguyen/giong-doc.md (VOICE_ID) sau khi người dùng chọn.
"""
import json, os, re, subprocess, sys
import requests

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"


def _key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k:
        p = r"C:\MERAH\.bao-mat\elevenlabs.txt"
        if os.path.exists(p):
            k = open(p, encoding="utf-8").read().strip()
    return k


def nguon(a=None):
    """elevenlabs (có khoá) hoặc edge (miễn phí). Ưu tiên: --nguon > GIONG_NGUON > có khoá thì elevenlabs > edge."""
    if a and "--nguon" in a:
        return a[a.index("--nguon") + 1].lower()
    g = os.environ.get("GIONG_NGUON", "").strip().lower()
    if g or _key():
        return g or "elevenlabs"
    p = os.path.join(os.path.dirname(__file__), "..", "giong-doc.md")  # thương hiệu đã chốt giọng riêng -> không tự đổi giọng
    if os.path.exists(p) and re.search(r"VOICE_ID:\s*[A-Za-z0-9]{10,}", open(p, encoding="utf-8").read()):
        return "elevenlabs"
    return "edge"


EDGE_MAC_DINH = {"vi": "vi-VN-HoaiMyNeural", "fil": "fil-PH-BlessicaNeural", "en": "en-US-AvaNeural"}


def edge_voice(text, voice=""):
    v = voice if "Neural" in (voice or "") else os.environ.get("GIONG_EDGE", "").strip()
    if v:
        return v
    if re.search(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", text.lower()):
        return EDGE_MAC_DINH["vi"]
    if re.search(r"(ang|ng|mga|po|ito|ako|ikaw|natin|namin|kayo|hindi|para sa|sa mga)", text.lower()) and len(re.findall(r"(ang|ng|mga|po|sa)", text.lower())) >= 3:
        return EDGE_MAC_DINH["fil"]
    return EDGE_MAC_DINH["en"]


def edge_tts_mod():
    try:
        import edge_tts
        return edge_tts
    except ImportError:
        sys.exit("LỖI: chưa cài giọng miễn phí. Chạy: pip install edge-tts")


def tts_edge(text, out, voice, speed):
    import asyncio
    et = edge_tts_mod()
    text = re.sub(r"\[[a-zA-Z ]{2,20}\]", "", text).strip()  # bỏ thẻ cảm xúc kiểu [excited] của ElevenLabs
    pc = round((speed - 1) * 100)
    import time
    v, loi = edge_voice(text, voice), None
    for lan in range(4):  # dịch vụ miễn phí đôi lúc không trả âm thanh -> thử lại
        try:
            asyncio.run(et.Communicate(text, v, rate=f"{'+' if pc >= 0 else ''}{pc}%").save(out))
            if os.path.exists(out) and os.path.getsize(out) > 800:
                return
        except Exception as e:
            loi = e
        time.sleep(1.5 * (lan + 1))
    try:  # dự phòng miễn phí thứ hai: Google (pip install gTTS) – giọng đều hơn, ít tự nhiên hơn
        from gtts import gTTS
        lang = {"fil": "tl"}.get(v.split("-")[0], v.split("-")[0])
        gTTS(text, lang=lang).save(out)
        print(f"  (Edge không trả âm thanh – đoạn này dùng giọng Google dự phòng)")
        return
    except ImportError:
        pass
    except Exception as e:
        loi = e
    sys.exit(f"LỖI giọng miễn phí Edge ({v}): {type(loi).__name__ if loi else 'không có âm thanh'} – thử lại sau ít phút hoặc đổi giọng bằng --voice")


def voices_edge(loc=""):
    import asyncio
    et = edge_tts_mod()
    for v in sorted(asyncio.run(et.list_voices()), key=lambda x: x["ShortName"]):
        if not loc or v["Locale"].lower().startswith(loc.lower()):
            print(f"{v['ShortName']:<38} {v['Gender']:<7} {v['Locale']}")


def key():
    k = _key()
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
    if NGUON == "edge":
        return tts_edge(text, out, voice, speed)
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
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst] + (["-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100"] if NGUON == "edge" else ["-c", "copy"]) + [out], check=True)
    json.dump(info, open(os.path.splitext(out)[0] + "_doan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in tmp + [lst]:
        os.remove(f)
    print(f"Xong {out}: {len(parts)} đoạn, tổng {sum(x['giay'] for x in info):.1f}s" + (" (giọng miễn phí Edge)" if NGUON == "edge" else ""))


def nghe(src, out):
    """Chép lời (speech-to-text). Chỉ để hiểu nội dung – kịch bản MERAH phải viết lại bằng lời mới."""
    if not _key():
        return nghe_free(src, out)
    tmp = out + ".tmp.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", tmp], check=True)
    with open(tmp, "rb") as f:
        r = requests.post(f"{API}/speech-to-text", headers={"xi-api-key": key()}, data={"model_id": "scribe_v1"}, files={"file": ("a.mp3", f, "audio/mpeg")}, timeout=300)
    os.remove(tmp)
    if not r.ok:
        sys.exit(f"LỖI ElevenLabs STT {r.status_code}: {r.text[:300]}")
    j = r.json(); open(out, "w", encoding="utf-8").write(j.get("text", "")); print(f"Xong {out}: ngôn ngữ {j.get('language_code','?')}, {len(j.get('text',''))} ký tự")


def nghe_free(src, out):
    """Chép lời miễn phí bằng faster-whisper hoặc whisper (chạy trên máy)."""
    try:
        from faster_whisper import WhisperModel
        seg, inf = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8").transcribe(src)
        txt, lang = " ".join(x.text.strip() for x in seg), inf.language
    except ImportError:
        try:
            import whisper
            r = whisper.load_model(os.environ.get("WHISPER_MODEL", "small")).transcribe(src); txt, lang = r["text"].strip(), r.get("language", "?")
        except ImportError:
            sys.exit("LỖI: không có khoá ElevenLabs và chưa cài công cụ chép lời miễn phí. Chạy: pip install faster-whisper")
    open(out, "w", encoding="utf-8").write(txt); print(f"Xong {out}: ngôn ngữ {lang}, {len(txt)} ký tự (whisper miễn phí)")


NGUON = "elevenlabs"

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    a = sys.argv[1:]
    NGUON = nguon(a)
    if "--nguon" in a:
        i = a.index("--nguon"); del a[i:i + 2]
    if not a or a[0] == "voices":
        voices_edge(a[1] if len(a) > 1 else "") if NGUON == "edge" else voices()
    elif a[0] == "doc":
        v = a[a.index("--voice") + 1] if "--voice" in a else ("" if NGUON == "edge" else default_voice())
        sp = float(a[a.index("--speed") + 1]) if "--speed" in a else 1.0
        kieu = a[a.index("--kieu") + 1] if "--kieu" in a else "vua"
        mdl = a[a.index("--model") + 1] if "--model" in a else MODEL
        doc(a[1], a[2], v, sp, kieu, mdl)
    elif a[0] == "nghe":
        nghe(a[1], a[2])
