"""SỐ LIỆU CHO BÁO CÁO – KHÔNG TỐN TOKEN (sếp chốt 15/11/2026).
Code đếm sẵn, Claude chỉ đọc bảng ngắn này rồi viết nhận xét/đề xuất (không tự đọc cả Sheet, không gọi lại số liệu).

  python so_lieu_bao_cao.py thu-ky            # báo cáo cuối ngày 21h30: đếm trạng thái các tab hôm nay
  python so_lieu_bao_cao.py qc [--ngay yyyy-mm-dd]   # báo cáo QC 0h: số liệu Meta Ads hôm qua + chấm KPI cố định
In ra Markdown. Lỗi/thiếu quyền thì in dòng `THIẾU:` để Claude biết phải lấy bằng công cụ khác.
"""
import argparse, collections, datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
VN = datetime.timezone(datetime.timedelta(hours=7))
PH = datetime.timezone(datetime.timedelta(hours=8))
TK_QC = "act_{{ID_FACEBOOK}}"  # MR 1 - HOÀNG (quang-cao/cai-dat-chay-qc.md)
KPI_TIN, KPI_MUA, LUAT_1TR, TRAN_TK = 10_000, 500_000, 1_000_000, 3_000_000


def doc_sheet():
    import sheet_api as S
    tabs = ["Untitled!A1:L", "QUANG-CAO!A1:N", "SPY-ADS!A1:K", "HOI-SEP!A1:F"]
    if not S.co_cau_hinh():  # đám mây chưa có Sheet API → tải bản xlsx bằng rclone
        import canh_spy as C
        x = C.tai_sheet()
        out = {}
        for t in tabs:
            ten, cot = t.split("!")[0], t.split(":")[1]
            n = ord(cot) - 64
            out[ten] = [[r.get(chr(65 + j), "") for j in range(n)] for r in C.doc_tab(x, ten)]
            if ten == "Untitled":  # ô ngày trong xlsx là số ngày Excel → yyyy-mm-dd
                for r in out[ten][1:]:
                    r[1] = C.ngay_iso(r[1])
        return out
    kq = S.goi([{"op": "get", "range": t} for t in tabs], timeout=120)
    return {t.split("!")[0]: k["values"] for t, k in zip(tabs, kq)}


def thu_ky():
    d = doc_sheet()
    now = datetime.datetime.now(VN)
    hn_vn, hn_iso = now.strftime("%d/%m"), datetime.datetime.now(PH).strftime("%Y-%m-%d")
    out = [f"# Số liệu ngày {now.strftime('%d/%m/%Y')} (code đếm lúc {now.strftime('%H:%M')} VN)"]

    # Bài page
    rows = [(r + [""] * 12)[:12] for r in d["Untitled"][1:] if r and r[0]]
    hom_nay = [r for r in rows if r[1] == hn_iso]
    dang_hn = [r for r in rows if re.search(rf"Đã (đăng|hẹn giờ) {hn_vn}", r[10])]
    out.append("\n## Fanpage (tab đầu)")
    out.append(f"- Bài lịch hôm nay: {len(hom_nay)} · trạng thái: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r[8] for r in hom_nay).items()))
    out.append(f"- Đã đăng/hẹn giờ trong ngày: {len(dang_hn)} · Tin 24h hôm nay: {sum(1 for r in rows if f'TIN 24H: đã đăng {hn_vn}' in r[10])}")
    cho = collections.Counter(r[8] for r in rows if r[8] in ("Chờ duyệt", "Cần sửa", "Đang sửa", "Đã duyệt"))
    out.append(f"- Đang tồn: " + (", ".join(f"{k} {v}" for k, v in cho.items()) or "không"))
    loi = [r[0] for r in rows if re.search(rf"Lỗi (đăng|Tin) {hn_vn}", r[10])]
    if loi:
        out.append(f"- Lỗi đăng hôm nay: {', '.join(loi)}")

    # Quảng cáo
    q = [(r + [""] * 14)[:14] for r in d["QUANG-CAO"][1:] if r and r[0].startswith("QC-")]
    out.append("\n## Quảng cáo (QUANG-CAO)")
    out.append("- Trạng thái: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r[8] for r in q if r[8] != "Đã bỏ").items()))
    out.append(f"- Đăng page hôm nay: {sum(1 for r in q if re.search(rf'Đã đăng {hn_vn}', r[10]))} · Seeding hôm nay: "
               f"{sum(1 for r in q if re.search(r'Seeding: đã bình luận ' + hn_vn, r[10]))} · Sửa xong hôm nay: "
               f"{sum(len(re.findall(re.escape(hn_vn) + r'[^\n]*sửa xong', r[13], re.I)) for r in q)}")
    chua_ads = [r[0] for r in q if r[8] == "Đã đăng page" and "Lên ads:" not in r[10]]
    out.append(f"- Đã đăng page nhưng CHƯA lên ads ({len(chua_ads)}): {', '.join(chua_ads) or 'không'}")
    chua_seed = [r[0] for r in q if r[8] == "Đã đăng page" and "Seeding: đã bình luận" not in r[10]]
    if chua_seed:
        out.append(f"- Chưa seeding: {', '.join(chua_seed)}")

    # SPY
    s = [(r + [""] * 11)[:11] for r in d["SPY-ADS"][1:] if r and len(r) > 9 and r[9]]
    dem = collections.Counter(re.sub(r"\s*\(.*$|\s+\d{2}-\d{2}-\d{4}.*$", "", r[8]) for r in s)
    out.append("\n## SPY-ADS")
    out.append("- " + ", ".join(f"{k} {v}" for k, v in dem.most_common() if k and not k.startswith("Bỏ")))

    # Hỏi sếp
    h = [(r + [""] * 6)[:6] for r in d["HOI-SEP"][1:] if r and r[0]]
    out.append("\n## HOI-SEP")
    out.append(f"- Chờ sếp trả lời: {sum(1 for r in h if not r[4].strip())} · Sếp đã trả lời, chưa xử lý: {sum(1 for r in h if r[4].strip() and not r[5].strip())}")
    print("\n".join(out))


def qc(ngay):
    import requests
    import fb_api as F
    try:
        tok = F.user_token()
    except SystemExit:
        print("THIẾU: không có token Facebook – Claude lấy số liệu bằng công cụ Meta Ads"); return
    ngay = ngay or (datetime.datetime.now(VN) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    r = requests.get(f"{F.G}/{TK_QC}/insights", timeout=90, params={
        "level": "ad", "time_range": json.dumps({"since": ngay, "until": ngay}), "limit": 500, "access_token": tok,
        "fields": "campaign_name,adset_name,ad_name,ad_id,spend,impressions,frequency,actions"})
    if not r.ok:
        print(f"THIẾU: token chưa có quyền đọc quảng cáo (ads_read) – {F.err_text(r)[:150]}. Claude lấy số liệu bằng công cụ Meta Ads; "
              "sếp muốn bỏ hẳn bước này thì tạo lại token có quyền ads_read."); return
    rows = r.json().get("data", [])

    def act(a, *keys):
        return sum(float(x["value"]) for x in a.get("actions", []) if x["action_type"] in keys)
    tong = sum(float(a.get("spend", 0)) for a in rows)
    out = [f"# Số liệu Meta Ads ngày {ngay} – TK {TK_QC} (code kéo + chấm KPI)",
           f"- Tổng chi TK: {tong:,.0f}đ ({'VƯỢT' if tong > TRAN_TK else 'dưới'} trần 3tr)", "",
           "| Quảng cáo | Chi | Tin | Giá/tin | Mua | Tần suất | KPI |", "|---|---|---|---|---|---|---|"]
    for a in sorted(rows, key=lambda x: -float(x.get("spend", 0))):
        chi = float(a.get("spend", 0))
        tin = act(a, "onsite_conversion.messaging_conversation_started_7d")
        mua = act(a, "onsite_conversion.purchase", "purchase", "offsite_conversion.fb_pixel_purchase")
        gia = chi / tin if tin else 0
        cua_claude = a.get("campaign_name", "").startswith(("CLAUDE", "[CQC]"))
        kpi = []
        if tin and gia <= KPI_TIN: kpi.append("tin đạt")
        elif tin: kpi.append("tin đắt" + (" >2×" if gia > 2 * KPI_TIN else ""))
        elif chi > 0: kpi.append("0 tin")
        if mua and chi / mua <= KPI_MUA: kpi.append("mua đạt")
        if cua_claude and chi >= LUAT_1TR and not mua: kpi.append("**LUẬT 1 TRIỆU → tắt**")
        ten = ("★ " if cua_claude else "") + a.get("ad_name", "")[:60]
        out.append(f"| {ten} | {chi:,.0f} | {tin:.0f} | {gia:,.0f} | {mua:.0f} | {float(a.get('frequency', 0)):.2f} | {', '.join(kpi)} |")
    out.append("\n★ = quảng cáo của Claude (được tắt theo luật). Không ★ = của sếp: chỉ đọc. Chi trong ngày theo múi giờ TK (UTC+7).")
    print("\n".join(out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("loai", choices=["thu-ky", "qc"])
    ap.add_argument("--ngay", default="")
    a = ap.parse_args()
    thu_ky() if a.loai == "thu-ky" else qc(a.ngay)
