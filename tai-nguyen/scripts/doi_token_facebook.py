"""Đổi token Facebook (app MERAH) – 1 token dùng chung cho đăng bài + quảng cáo (sếp chốt 17/11/2026).
Đọc token mới ở C:\\MERAH\\.bao-mat\\facebook.moi.txt (luu_token_facebook.ps1 ghi), kiểm tra đủ quyền rồi mới thay facebook.txt.
Token cũ giữ ở facebook.cu.txt. Không bao giờ in token.
"""
import os, shutil, sys, requests

SEC = r"C:\MERAH\.bao-mat"
G = "https://graph.facebook.com/v22.0"
MOI, CU, DANG = (os.path.join(SEC, f) for f in ("facebook.moi.txt", "facebook.cu.txt", "facebook.txt"))
CAN = {"ads_read", "ads_management", "business_management", "pages_show_list", "pages_read_engagement",
       "pages_manage_posts", "pages_manage_engagement", "pages_manage_metadata", "pages_read_user_content", "read_insights"}


def main():
    tok = open(MOI, encoding="utf-8").read().strip()
    try:
        p = requests.get(f"{G}/me/permissions", params={"access_token": tok}, timeout=30).json()
        if "error" in p:
            return print("TOKEN LỖI:", p["error"].get("message")), 1
        co = {x["permission"] for x in p.get("data", []) if x.get("status") == "granted"}
        thieu = sorted(CAN - co)
        if thieu:
            return print("CHƯA ĐỦ QUYỀN, chưa thay token. Thiếu:", ", ".join(thieu)), 1
        d = requests.get(f"{G}/debug_token", params={"input_token": tok, "access_token": tok}, timeout=30).json().get("data", {})
        r = requests.get(f"{G}/act_{{ID_FACEBOOK}}", params={"access_token": tok, "fields": "name"}, timeout=30).json()
        if "error" in r:
            return print("Đủ quyền nhưng CHƯA ĐỌC ĐƯỢC TK MR 1:", r["error"].get("message"),
                         "→ trong BM MERAH ADS - TKQC cấp cho tài khoản Facebook này quyền vào TK quảng cáo MR 1. Chưa thay token."), 1
        het = d.get("expires_at", 0)
        if os.path.exists(DANG):
            shutil.copyfile(DANG, CU)
        shutil.move(MOI, DANG)
        print(f"ĐÃ THAY TOKEN. Đọc được TK: {r.get('name')}. Hạn: {'không hết hạn' if not het else 'ngắn hạn – nên gia hạn'}")
        return 0
    finally:
        if os.path.exists(MOI):
            os.remove(MOI)


if __name__ == "__main__":
    sys.exit(main())
