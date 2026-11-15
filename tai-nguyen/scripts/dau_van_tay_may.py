"""DẤU VÂN TAY MÁY – để 2 máy (PC trực, laptop) chạy giống nhau 100% (sếp chốt 15/11/2026).
  python dau_van_tay_may.py --may truc|laptop          # ghi trang-thai/may/<may>.json (KHÔNG chứa khoá/mật khẩu: chỉ tên, phiên bản, mã băm, có/không)
  python dau_van_tay_may.py --so-sanh                   # so trang-thai/may/truc.json với laptop.json, in phần lệch
Sau khi ghi: git add trang-thai/may && commit && push. Máy kia pull rồi --so-sanh.
"""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
KHO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(KHO, "trang-thai", "may")
HOME = os.path.expanduser("~")
try:
    sys.path.insert(0, HERE)
    from duong_dan_may import dat_rclone
    dat_rclone()
except Exception:
    pass


def sh(cmd, t=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t, shell=isinstance(cmd, str),
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return (r.stdout or r.stderr).strip()
    except Exception as e:
        return f"LỖI {e}"[:120]


def bam(p):
    try:
        return hashlib.sha1(open(p, "rb").read().replace(b"\r\n", b"\n")).hexdigest()[:12]
    except Exception:
        return "?"


def thu_muc_bam(d, duoi=None):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "**", "*"), recursive=True)):
        if os.path.isfile(p) and (not duoi or p.endswith(duoi)) and "__pycache__" not in p:
            out[os.path.relpath(p, d).replace("\\", "/")] = bam(p)
    return out


def phien_ban(exe, arg="--version"):
    p = shutil.which(exe)
    if not p:
        g = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages", f"*{exe}*", "**", exe + ".exe"), recursive=True)
        p = g[0] if g else None
    if not p:
        return "THIẾU"
    return sh([p, arg]).splitlines()[0][:80] if sh([p, arg]) else "?"


def ghi(may):
    git = shutil.which("git") or r"C:\Program Files\Git\cmd\git.exe"
    d = {"may": may, "luc": time.strftime("%Y-%m-%d %H:%M"), "may_tinh": os.environ.get("COMPUTERNAME", "")}
    d["kho"] = {"commit": sh([git, "-C", KHO, "rev-parse", "--short", "HEAD"]),
                "chua_commit": [l for l in sh([git, "-C", KHO, "status", "--short"]).splitlines() if l.strip()][:40]}
    d["skill_kho"] = sorted(os.listdir(os.path.join(KHO, ".claude", "skills"))) if os.path.isdir(os.path.join(KHO, ".claude", "skills")) else []
    d["agent_kho"] = sorted(os.listdir(os.path.join(KHO, ".claude", "agents"))) if os.path.isdir(os.path.join(KHO, ".claude", "agents")) else []
    us = os.path.join(HOME, ".claude", "skills")
    d["skill_nguoi_dung"] = {n: bam(os.path.join(us, n, "SKILL.md")) for n in sorted(os.listdir(us))} if os.path.isdir(us) else {}
    mem = [m for pat in ("*MERAH-he-thong*", "*SUB-AGENT*") for m in glob.glob(os.path.join(HOME, ".claude", "projects", pat, "memory"))]  # PC trực | laptop
    d["bo_nho"] = thu_muc_bam(mem[0], ".md") if mem else {}
    d["cong_cu"] = {"python": sys.version.split()[0], "node": phien_ban("node"), "npm": phien_ban("npm"), "git": phien_ban("git"),
                    "ffmpeg": phien_ban("ffmpeg", "-version"), "rclone": phien_ban("rclone", "version"),
                    "claude": sh([shutil.which("claude") or os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd"), "--version"], 90)[:60]}
    pk = sh([sys.executable, "-m", "pip", "list", "--format", "json"], 120)
    try:
        d["pip"] = {x["name"].lower(): x["version"] for x in json.loads(pk)}
    except Exception:
        d["pip"] = {"LỖI": pk[:100]}
    d["npm_toan_cuc"] = sorted(re.findall(r"[+`-]-- (\S+)@", sh("npm ls -g --depth=0", 120)))
    lich = sh(["powershell", "-NoProfile", "-Command",
               "Get-ScheduledTask | ?{$_.TaskName -like 'MERAH*'} | %{ $_.TaskName + ' | ' + $_.State + ' | ' + (($_.Actions | %{ [IO.Path]::GetFileName($_.Execute) + ' ' + ($_.Arguments -replace '.*\\\\','') }) -join ';') }"], 60)
    d["lich_windows"] = sorted(l for l in lich.splitlines() if l.strip())
    bm = r"C:\MERAH\.bao-mat"
    d["bi_mat_co"] = {os.path.basename(p): os.path.getsize(p) > 0 for p in sorted(glob.glob(os.path.join(bm, "*")))} if os.path.isdir(bm) else {"THIẾU thư mục": False}
    env = sh(["powershell", "-NoProfile", "-Command", "(Get-ItemProperty HKCU:\\Environment).PSObject.Properties.Name -join ','"])
    d["bien_moi_truong"] = sorted(n for n in env.split(",") if re.search(r"CLAUDE|MERAH|ELEVEN|HIGGS|FB_|OPENAI|RCLONE|GITHUB", n, re.I))
    rc = sh(["rclone", "listremotes"])
    d["rclone_remote"] = sorted(rc.split()) if "LỖI" not in rc else rc
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, may + ".json")
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("đã ghi", p)


def so_sanh():
    a, b = [json.load(open(os.path.join(OUT, m + ".json"), encoding="utf-8")) for m in ("truc", "laptop")]
    print(f"PC trực: {a['luc']} commit {a['kho']['commit']} | laptop: {b['luc']} commit {b['kho']['commit']}")
    for k in sorted(set(a) | set(b)):
        if k in ("luc", "may", "may_tinh"):
            continue
        x, y = a.get(k), b.get(k)
        if x == y:
            continue
        if isinstance(x, dict) and isinstance(y, dict):
            for kk in sorted(set(x) | set(y)):
                if x.get(kk) != y.get(kk):
                    print(f"[{k}] {kk}: trực={x.get(kk, '—')} | laptop={y.get(kk, '—')}")
        elif isinstance(x, list) and isinstance(y, list):
            chi_a, chi_b = sorted(set(map(str, x)) - set(map(str, y))), sorted(set(map(str, y)) - set(map(str, x)))
            if chi_a: print(f"[{k}] chỉ PC trực: {chi_a}")
            if chi_b: print(f"[{k}] chỉ laptop: {chi_b}")
        else:
            print(f"[{k}] trực={x} | laptop={y}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--may", choices=["truc", "laptop"])
    ap.add_argument("--so-sanh", action="store_true")
    a = ap.parse_args()
    so_sanh() if a.so_sanh else ghi(a.may)
