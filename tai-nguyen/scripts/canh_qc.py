"""CANH QUẢNG CÁO TỰ ĐỘNG – KHÔNG TỐN TOKEN CLAUDE (sếp chốt 17/11/2026).
Luật: quang-cao/quy-chuan-1-1-3.md mục 0, 4, 4b, 4c, 5. Chỉ đụng chiến dịch tên bắt đầu "CLAUDE" / "[CQC]".

  python canh_qc.py tat        # mỗi 10 phút: CHỈ tắt video chạm luật tắt
  python canh_qc.py dem        # 0h30 VN: tắt → bật lại → tính lại nhóm → giảm → tăng (+ đề xuất, + việc sếp đã duyệt)
  python canh_qc.py thu-token  # kiểm tra token đọc/ghi quảng cáo (không đổi gì)

CHẠY THẬT hay CHẠY THỬ: file C:\\MERAH\\trang-thai-may\\canh_qc_cai_dat.json {"chay_that": true}. Mặc định chạy thử:
tính đủ mọi việc, ghi lên app với trạng thái "Chạy thử – chưa làm", KHÔNG gửi lệnh nào tới Meta.
Token: dùng CHUNG token app MERAH C:\\MERAH\\.bao-mat\\facebook.txt (sếp chốt 17/11: 1 token, có thêm ads_read + ads_management;
sếp tự dán bằng C:\\MERAH\\luu_token_facebook.ps1 – xem quang-cao/HUONG-DAN-TOKEN-QC.md). Không in token. Kết quả ghi tab QC-TU-DONG (app QUẢN TRỊ MERAH hiện + nút Duyệt/Bỏ) và log máy.
"""
import datetime, json, os, sys, time, traceback

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TK = "act_{{ID_FACEBOOK}}"  # MR 1 - HOÀNG
G = "https://graph.facebook.com/v22.0"
VN = datetime.timezone(datetime.timedelta(hours=7))
SEC = r"C:\MERAH\.bao-mat"
MAY = r"C:\MERAH\trang-thai-may"
os.makedirs(MAY, exist_ok=True)
STATE = os.path.join(MAY, "canh_qc.json")
CAI_DAT = os.path.join(MAY, "canh_qc_cai_dat.json")
LOG = os.path.join(MAY, "canh_qc.log")
LOCK = os.path.join(MAY, "canh_qc.lock")
TAB = "QC-TU-DONG"

# ---- LUẬT (quy chuẩn 17/11) ----
MUC_LM, MUC_TN = 500_000, 750_000          # tiền để tắt: (số đơn + 1) × mức
KPI_TIN = 10_000                            # giá tin
TIN_0_TAT = 50_000                          # TN: tiêu ≥50k mà 0 tin
DEPTH_MIN_TIN, DEPTH_TL = 50, 0.10          # TN: ≥50 tin mà <10% tới tin thứ 3
GIO_TEST = 72                               # 72h đầu không đụng lô; sau 72h giá tin >10k + 0 đơn → tắt
NGAY_TANG = 7                               # đủ 7 ngày chạy (cộng dồn, bỏ ngày tắt) mới tăng
BUOC = 0.20                                 # mỗi lần ±20%
GIU_NGAY = 2                                # sau mỗi lần ±20% giữ 2 ngày
TIEU_80 = 0.80                              # nhóm tiêu ≥80% ngân sách TB 3 ngày mới tăng
TAN_SUAT_TANG = 2.5
TRAN_CLAUDE = 3_000_000                     # tổng ngân sách các nhóm CLAUDE
LM_DON_TANG = 2                             # camp lượt mua ≥2 đơn mới tự tăng
MOI_TAN_SUAT = 3.0

DON_KEYS = ("onsite_conversion.purchase", "purchase", "offsite_conversion.fb_pixel_purchase", "omni_purchase")
TIN_KEY = "onsite_conversion.messaging_conversation_started_7d"
DEPTH3_KEY = "onsite_conversion.messaging_user_depth_3_message_send"


def now():
    return datetime.datetime.now(VN)


def log(msg):
    line = f"{now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def chay_that():
    try:
        return bool(json.load(open(CAI_DAT, encoding="utf-8")).get("chay_that"))
    except Exception:
        return False


def token():
    p = os.path.join(SEC, "meta_ads.txt")
    if os.path.exists(p) and open(p, encoding="utf-8").read().strip():
        return open(p, encoding="utf-8").read().strip()
    import fb_api as F  # dự phòng: token người dùng (thường thiếu ads_read)
    return F.user_token()


TOK = None


def api(method, path, **params):
    params["access_token"] = TOK
    url = path if path.startswith("http") else f"{G}/{path}"
    for lan in range(3):
        r = requests.request(method, url, params=params if method == "GET" else None,
                             data=params if method != "GET" else None, timeout=90)
        if r.ok:
            return r.json()
        try:
            e = r.json().get("error", {})
        except Exception:
            e = {"message": r.text[:200]}
        if e.get("code") in (4, 17, 32, 613) and lan < 2:  # giới hạn gọi → chờ rồi thử lại
            time.sleep(30 * (lan + 1)); continue
        raise RuntimeError(f"Meta lỗi {e.get('code')}/{e.get('error_subcode')}: {e.get('message')}")


def lay_het(path, **params):
    out, d = [], api("GET", path, **params)
    while True:
        out += d.get("data", [])
        nxt = d.get("paging", {}).get("next")
        if not nxt:
            return out
        d = requests.get(nxt, timeout=90).json()


LOC_CLAUDE = json.dumps([{"field": "campaign.name", "operator": "CONTAIN", "value": "CLAUDE"}])


def act(row, *keys):
    vals = {a["action_type"]: float(a["value"]) for a in row.get("actions", [])}
    for k in keys:  # lấy khoá đầu tiên có số, tránh cộng trùng purchase/onsite purchase
        if vals.get(k):
            return vals[k]
    return 0.0


def don(row):
    return act(row, *DON_KEYS)


# ---------------- ĐỌC DỮ LIỆU ----------------
def doc():
    camps = {c["id"]: c for c in lay_het(f"{TK}/campaigns", fields="id,name,status,effective_status,objective,daily_budget", limit=200)
             if c["name"].upper().startswith(("CLAUDE", "[CQC]"))}
    adsets = {s["id"]: s for s in lay_het(f"{TK}/adsets", fields="id,name,status,effective_status,daily_budget,campaign_id,created_time",
                                          filtering=LOC_CLAUDE, limit=500) if s["campaign_id"] in camps}
    ads = {a["id"]: a for a in lay_het(f"{TK}/ads", fields="id,name,status,effective_status,adset_id,campaign_id,created_time",
                                       filtering=LOC_CLAUDE, limit=500) if a["campaign_id"] in camps}
    tron = {r["ad_id"]: r for r in lay_het(f"{TK}/insights", level="ad", date_preset="maximum", filtering=LOC_CLAUDE, limit=500,
                                          fields="ad_id,spend,actions,impressions")}
    f7 = {r["ad_id"]: float(r.get("frequency", 0)) for r in lay_het(f"{TK}/insights", level="ad", date_preset="last_7d",
                                                                      filtering=LOC_CLAUDE, limit=500, fields="ad_id,frequency")}
    ngay = {}
    for r in lay_het(f"{TK}/insights", level="ad", date_preset="last_90d", time_increment=1, filtering=LOC_CLAUDE, limit=500,
                     fields="ad_id,date_start,spend,actions,impressions,inline_link_clicks"):
        ngay.setdefault(r["ad_id"], []).append(r)
    for v in ngay.values():
        v.sort(key=lambda r: r["date_start"])
    return camps, adsets, ads, tron, f7, ngay


def la_lm(camp):
    return camp.get("objective") == "OUTCOME_SALES" or " LM" in camp["name"].upper() or "LƯỢT MUA" in camp["name"].upper()


def so_lieu_ad(a, camps, tron, f7, ngay):
    t = tron.get(a["id"], {})
    lm = la_lm(camps[a["campaign_id"]])
    chi, d, tin = float(t.get("spend", 0)), don(t), act(t, TIN_KEY)
    rows = ngay.get(a["id"], [])
    # chi kể từ đơn gần nhất
    chi_sau_don, co_don_trong_90 = 0.0, False
    for r in reversed(rows):
        if don(r) > 0:
            co_don_trong_90 = True; break
        chi_sau_don += float(r.get("spend", 0))
    if d == 0:
        chi_sau_don = chi
    # mỏi: so 3 ngày đầu vs 3 ngày gần nhất (trong các ngày có chi)
    co_chi = [r for r in rows if float(r.get("spend", 0)) > 0]
    moi_xau = False
    if len(co_chi) >= 6:
        def gia_tin(rs):
            c, n = sum(float(r["spend"]) for r in rs), sum(act(r, TIN_KEY) for r in rs)
            return c / n if n else None
        def ctr(rs):
            im, cl = sum(float(r.get("impressions", 0)) for r in rs), sum(float(r.get("inline_link_clicks", 0)) for r in rs)
            return cl / im if im else None
        g0, g1, c0, c1 = gia_tin(co_chi[:3]), gia_tin(co_chi[-3:]), ctr(co_chi[:3]), ctr(co_chi[-3:])
        moi_xau = bool((g0 and g1 and g1 >= 2 * g0) or (c0 and c1 is not None and c1 <= 0.7 * c0))
    return {"lm": lm, "chi": chi, "don": d, "tin": tin, "depth3": act(t, DEPTH3_KEY),
            "muc": (d + 1) * (MUC_LM if lm else MUC_TN), "base": MUC_LM if lm else MUC_TN,
            "chi_sau_don": chi_sau_don, "f7": f7.get(a["id"], 0.0), "moi_xau": moi_xau,
            "so_ngay_chay": len(co_chi), "gio_tuoi": (now() - datetime.datetime.strptime(a["created_time"][:19], "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=datetime.timezone.utc)).total_seconds() / 3600}


def luat_tat(s):
    """Trả lý do tắt hoặc None. Thứ tự ưu tiên theo quy chuẩn mục 0/4."""
    if s["chi"] >= s["muc"]:
        return f"Chạm mức tiền: chi {s['chi']:,.0f}đ ≥ ({s['don']:.0f} đơn + 1) × {s['base']:,.0f}đ = {s['muc']:,.0f}đ, chưa có đơn tiếp theo"
    moi = s["f7"] > MOI_TAN_SUAT and s["moi_xau"]
    if moi and s["chi_sau_don"] >= s["base"]:
        return f"Video mỏi: tần suất 7 ngày {s['f7']:.1f} + giá tin/CTR xấu đi + chi {s['chi_sau_don']:,.0f}đ kể từ đơn gần nhất chưa ra đơn mới"
    if not s["lm"]:
        if s["chi"] >= TIN_0_TAT and s["tin"] == 0:
            return f"Tiêu {s['chi']:,.0f}đ mà 0 tin"
        if s["tin"] >= DEPTH_MIN_TIN and s["depth3"] / s["tin"] < DEPTH_TL:
            return f"{s['tin']:.0f} tin nhưng chỉ {s['depth3'] / s['tin']:.0%} nhắn tới tin thứ 3 (<10%)"
        if s["gio_tuoi"] >= GIO_TEST and s["don"] == 0 and s["tin"] and s["chi"] / s["tin"] > KPI_TIN:
            return f"Đủ 72h, giá tin {s['chi'] / s['tin']:,.0f}đ >10k và chưa có đơn"
    return None


# ---------------- GHI ----------------
KQ = []  # các dòng ghi lên app


def ghi(loai, cap, oid, ten, thay_doi, ly_do, trang_thai):
    ma = f"QCT-{now():%Y%m%d%H%M}-{oid[-6:]}-{len(KQ)}"
    KQ.append([f"{now():%d/%m %H:%M}", loai, cap, oid, ten, thay_doi, ly_do, trang_thai, ma])
    log(f"{loai} | {cap} {oid} {ten} | {thay_doi} | {ly_do} | {trang_thai}")


def lam(oid, **params):
    """Gửi lệnh tới Meta (chỉ khi chạy thật). Trả trạng thái để ghi."""
    if not chay_that():
        return "Chạy thử – chưa làm"
    api("POST", oid, **params)
    return "Đã làm"


def day_len_app():
    if not KQ:
        return
    try:
        import sheet_api as S
        S.append(TAB, KQ)
    except Exception as e:
        log(f"LỖI ghi app (Sheet tab {TAB}): {e}")


def state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"ad": {}, "adset": {}}


def luu(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ---------------- CÁC BƯỚC ----------------
def buoc_tat(camps, adsets, ads, tron, f7, ngay, st):
    doi = set()
    for a in ads.values():
        if a["effective_status"] != "ACTIVE":
            continue
        s = so_lieu_ad(a, camps, tron, f7, ngay)
        ly_do = luat_tat(s)
        if not ly_do:
            continue
        tt = lam(a["id"], status="PAUSED")
        ghi("Đã tự tắt", "Quảng cáo", a["id"], a["name"], "Đang chạy → Tắt", ly_do, tt)
        st["ad"][a["id"]] = {"don_luc_tat": s["don"], "chi_luc_tat": s["chi"], "tat_luc": now().isoformat(), "ly_do": ly_do}
        a["effective_status"] = "PAUSED"
        doi.add(a["adset_id"])
    # nhóm có mọi video đã tắt → tắt nhóm
    for sid in doi:
        s = adsets.get(sid)
        if s and s["status"] == "ACTIVE" and not any(x["adset_id"] == sid and x["effective_status"] == "ACTIVE" for x in ads.values()):
            tt = lam(sid, status="PAUSED")
            ghi("Đã tự tắt", "Nhóm", sid, s["name"], "Đang chạy → Tắt", "Mọi video trong nhóm đã tắt", tt)
            s["status"] = "PAUSED"
    return doi


def buoc_bat_lai(camps, adsets, ads, tron, f7, ngay, st):
    doi = set()
    for a in ads.values():
        if a["status"] != "PAUSED":
            continue
        s = so_lieu_ad(a, camps, tron, f7, ngay)
        goc = st["ad"].get(a["id"])
        if goc is None:  # lần đầu thấy: ghi mốc, đơn về SAU mốc này mới tính là đơn mới
            st["ad"][a["id"]] = {"don_luc_tat": s["don"], "chi_luc_tat": s["chi"], "tat_luc": "moc-" + now().isoformat()}
            continue
        if s["don"] > goc["don_luc_tat"] and s["chi"] < s["muc"]:
            c = camps[a["campaign_id"]]
            if c["status"] != "ACTIVE":
                ghi("Cảnh báo", "Quảng cáo", a["id"], a["name"], "Không bật", "Có đơn mới dưới mức nhưng chiến dịch đang tắt – sếp xem", "Chờ sếp")
                continue
            tt = ""
            s_set = adsets.get(a["adset_id"])
            if s_set and s_set["status"] != "ACTIVE":
                tt = lam(s_set["id"], status="ACTIVE")
                ghi("Đã tự bật lại", "Nhóm", s_set["id"], s_set["name"], "Tắt → Đang chạy", "Bật để chạy lại video có đơn về trễ", tt)
                s_set["status"] = "ACTIVE"
            tt = lam(a["id"], status="ACTIVE")
            ghi("Đã tự bật lại", "Quảng cáo", a["id"], a["name"], "Tắt → Đang chạy",
                f"Đơn về trễ: {goc['don_luc_tat']:.0f} → {s['don']:.0f} đơn, chi {s['chi']:,.0f}đ < mức {s['muc']:,.0f}đ. Ngân sách giữ nguyên", tt)
            st["ad"].pop(a["id"], None)
            a["effective_status"] = "ACTIVE"
            doi.add(a["adset_id"])
    return doi


def seg_insights(sid, since):
    hom_qua = (now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if since > hom_qua:
        return None
    d = api("GET", f"{sid}/insights", time_range=json.dumps({"since": since, "until": hom_qua}), fields="spend,actions,frequency")
    return (d.get("data") or [{}])[0]


def ngay_nhom(sid):
    rows = lay_het(f"{sid}/insights", date_preset="maximum", time_increment=1, fields="date_start,spend,actions,frequency", limit=500)
    hom_nay = now().strftime("%Y-%m-%d")
    return sorted([r for r in rows if r["date_start"] < hom_nay], key=lambda r: r["date_start"])


def buoc_tang_giam(camps, adsets, ads, tron, f7, ngay, st, bo_qua):
    hom_qua = (now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    song = [s for s in adsets.values() if s["status"] == "ACTIVE" and camps[s["campaign_id"]]["status"] == "ACTIVE"]
    tong_ns = sum(float(s.get("daily_budget") or 0) for s in song)
    for s in song:
        sid = s["id"]
        if not s.get("daily_budget"):
            continue  # ngân sách ở chiến dịch (CBO) – không tự đổi
        ns = float(s["daily_budget"])
        ss = st["adset"].setdefault(sid, {"lan_doi": None, "ns_truoc": None, "tran": None, "kieu": None})
        if sid in bo_qua:
            continue
        if ss["lan_doi"] and (now() - datetime.datetime.fromisoformat(ss["lan_doi"])).days < GIU_NGAY:
            continue
        lm = la_lm(camps[s["campaign_id"]])
        base = MUC_LM if lm else MUC_TN
        rows = ngay_nhom(sid)
        if not rows:
            continue
        since = ss["lan_doi"][:10] if ss["lan_doi"] else rows[0]["date_start"]
        seg = seg_insights(sid, since) or {}
        c, d, tin = float(seg.get("spend", 0)), don(seg), act(seg, TIN_KEY)
        gia_tin = c / tin if tin else None
        cpo = c / d if d else None
        ad_song = [a for a in ads.values() if a["adset_id"] == sid and a["effective_status"] == "ACTIVE"]
        sl = [so_lieu_ad(a, camps, tron, f7, ngay) for a in ad_song]
        moi_ra_don = any(x["f7"] > MOI_TAN_SUAT and x["moi_xau"] and x["chi_sau_don"] < x["base"] for x in sl)

        # ---- GIẢM ----
        ly_do = None
        if d and cpo > base:
            ly_do = f"Đoạn từ {since}: {cpo:,.0f}đ/đơn > {base:,.0f}đ"
        elif not d and c >= base:
            ly_do = f"Đoạn từ {since}: chi {c:,.0f}đ mà 0 đơn"
        elif not lm and gia_tin and gia_tin > KPI_TIN and not d:
            ly_do = f"Giá tin {gia_tin:,.0f}đ > 10k (lô chưa có đơn trong đoạn)"
        elif moi_ra_don:
            ly_do = "Video mỏi nhưng vẫn ra đơn → giảm 20%"
        if ly_do:
            moi = ss["ns_truoc"] if (ss["kieu"] == "tang" and ss["ns_truoc"]) else ns * (1 - BUOC)
            moi = max(round(moi / 1000) * 1000, 50_000)
            if moi < ns:
                tt = lam(sid, daily_budget=int(moi))
                ghi("Đã tự giảm", "Nhóm", sid, s["name"], f"{ns:,.0f}đ → {moi:,.0f}đ/ngày ({moi / ns - 1:+.0%})", ly_do, tt)
                if "đơn" in ly_do and "mỏi" not in ly_do:
                    ss["tran"] = ns  # mức vừa lùi xuống = trần
                ss.update(lan_doi=now().isoformat(), ns_truoc=ns, kieu="giam")
                tong_ns += moi - ns
            continue

        # ---- TĂNG ----
        so_ngay = len([r for r in rows if float(r.get("spend", 0)) > 0])
        if so_ngay < NGAY_TANG:
            continue
        don_tron = sum(don(r) for r in rows)
        dat_kpi = d > 0 and cpo <= base
        if not dat_kpi:
            continue  # chưa đủ dữ liệu → giữ nguyên, xét lại mai
        moi = round(ns * (1 + BUOC) / 1000) * 1000
        ba = rows[-3:]
        chi3 = sum(float(r["spend"]) for r in ba) / len(ba)
        tin3 = sum(act(r, TIN_KEY) for r in ba)
        f_nhom = float(ba[-1].get("frequency", 0)) if ba else 0
        f_7 = max([x["f7"] for x in sl] or [0])
        thieu = []
        if not lm and (not tin3 or chi3 * len(ba) / tin3 > KPI_TIN):
            thieu.append("giá tin 3 ngày >10k")
        if chi3 < TIEU_80 * ns:
            thieu.append(f"chỉ tiêu {chi3 / ns:.0%} ngân sách (cần ≥80%)")
        if f_7 >= TAN_SUAT_TANG:
            thieu.append(f"tần suất {f_7:.1f} (cần <2,5)")
        if tong_ns + (moi - ns) >= TRAN_CLAUDE:
            thieu.append(f"tổng CLAUDE sau tăng {tong_ns + moi - ns:,.0f}đ chạm trần 3tr")
        if lm and don_tron < LM_DON_TANG:
            thieu.append(f"camp lượt mua mới {don_tron:.0f} đơn (cần ≥2)")
        if ss["tran"] and moi > ss["tran"]:
            thieu.append(f"vượt trần cũ {ss['tran']:,.0f}đ – nên mở rộng ngang")
        mo_ta = f"{ns:,.0f}đ → {moi:,.0f}đ/ngày (+20%)"
        kpi_txt = f"Đoạn từ {since}: {d:.0f} đơn, {cpo:,.0f}đ/đơn ≤ {base:,.0f}đ; chạy {so_ngay} ngày"
        if not thieu:
            tt = lam(sid, daily_budget=int(moi))
            ghi("Đã tự tăng", "Nhóm", sid, s["name"], mo_ta, kpi_txt + "; đủ mọi điều kiện", tt)
            ss.update(lan_doi=now().isoformat(), ns_truoc=ns, kieu="tang")
            tong_ns += moi - ns
        elif not any("trần cũ" in t for t in thieu):
            ghi("Đề xuất tăng", "Nhóm", sid, s["name"], mo_ta, kpi_txt + ". THIẾU: " + "; ".join(thieu), "Chờ sếp duyệt")


def buoc_lam_viec_da_duyet(adsets, st):
    """Đề xuất sếp bấm Duyệt trên app (cột H = 'Đã duyệt') → tăng lúc 0h30."""
    try:
        import sheet_api as S
        rows = S.get(f"{TAB}!A2:I")
    except Exception as e:
        log(f"Không đọc được đề xuất đã duyệt: {e}"); return
    for i, r in enumerate(rows, start=2):
        r += [""] * (9 - len(r))
        if r[1] != "Đề xuất tăng" or r[7].strip() != "Đã duyệt":
            continue
        sid = r[3]
        s = adsets.get(sid)
        if not s or s["status"] != "ACTIVE" or not s.get("daily_budget"):
            S.set_(f"{TAB}!H{i}", [["Không làm được – nhóm đã tắt/đổi"]]); continue
        ns = float(s["daily_budget"]); moi = round(ns * (1 + BUOC) / 1000) * 1000
        tt = lam(sid, daily_budget=int(moi))
        S.set_(f"{TAB}!H{i}", [[f"Đã làm theo duyệt {now():%d/%m %H:%M}" if tt == "Đã làm" else "Đã duyệt – chạy thử, chưa làm"]])
        ghi("Đã tăng theo duyệt", "Nhóm", sid, s["name"], f"{ns:,.0f}đ → {moi:,.0f}đ/ngày (+20%)", f"Sếp duyệt trên app (mã {r[8]})", tt)
        st["adset"].setdefault(sid, {"lan_doi": None, "ns_truoc": None, "tran": None, "kieu": None})
        st["adset"][sid].update(lan_doi=now().isoformat(), ns_truoc=ns, kieu="tang")


def main():
    global TOK
    cmd = (sys.argv[1:2] or ["?"])[0]
    if cmd not in ("tat", "dem", "thu-token"):
        print(__doc__); return
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 1500:
        log("Bỏ qua: lượt trước còn chạy"); return
    open(LOCK, "w").write(str(os.getpid()))
    try:
        TOK = token()
        if cmd == "thu-token":
            d = api("GET", TK, fields="name,account_status")
            print(f"ĐỌC OK: {d.get('name')} (trạng thái {d.get('account_status')})")
            dbg = requests.get(f"{G}/me/permissions", params={"access_token": TOK}, timeout=30).json()
            quyen = {p["permission"] for p in dbg.get("data", []) if p.get("status") == "granted"}
            print("ads_management:", "CÓ" if "ads_management" in quyen or not quyen else "THIẾU",
                  "| chế độ:", "CHẠY THẬT" if chay_that() else "CHẠY THỬ")
            return
        st = state()
        data = doc()
        camps, adsets, ads, tron, f7, ngay = data
        log(f"== {cmd} ({'THẬT' if chay_that() else 'THỬ'}) – {len(camps)} camp, {len(adsets)} nhóm, {len(ads)} QC CLAUDE")
        doi = buoc_tat(*data, st)
        if cmd == "dem":
            doi |= buoc_bat_lai(*data, st)
            buoc_lam_viec_da_duyet(adsets, st)
            buoc_tang_giam(*data, st, doi)
        luu(st)
        day_len_app()
    except Exception as e:
        log("LỖI: " + str(e) + "\n" + traceback.format_exc()[-800:])
        if cmd == "dem" or now().minute < 10:  # lượt 10 phút: chỉ báo lỗi lên app 1 lần/giờ, tránh spam
            KQ.append([f"{now():%d/%m %H:%M}", "Cảnh báo", "Hệ thống", "-", "canh_qc.py", "Lỗi", str(e)[:300], "Chờ sếp", f"QCT-LOI-{now():%Y%m%d%H%M}"])
        day_len_app()
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


if __name__ == "__main__":
    main()
