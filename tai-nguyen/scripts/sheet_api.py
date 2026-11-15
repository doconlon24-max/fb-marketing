"""Ghi/đọc Sheet MERAH qua Apps Script (tai-nguyen/apps-script/merah_sheet_api.gs) – KHÔNG tốn token Claude.
Cấu hình (KHÔNG đưa lên GitHub, không in ra): C:\\MERAH\\.bao-mat\\sheet_api.json {"url": "...", "key": "..."}
hoặc biến môi trường MERAH_SHEET_API_URL + MERAH_SHEET_API_KEY (đám mây).

Dùng trong Python:
    from sheet_api import get, set_, set_key, claim, append, co_cau_hinh
    rows = get("SPY-ADS!A1:J")
    if claim("QUANG-CAO", "A", "QC-20261115-VD1", "K", r"^$|^Lỗi", "Đang đăng (máy PC TRỰC 15/11 01:30)"): ...
Dòng lệnh:  python sheet_api.py thu      (kiểm tra kết nối, chỉ đọc 1 ô)
"""
import json, os, sys
import requests

_LOCAL = r"C:\MERAH\.bao-mat\sheet_api.json"


def _cfg():
    url, key = os.environ.get("MERAH_SHEET_API_URL", ""), os.environ.get("MERAH_SHEET_API_KEY", "")
    if (not url or not key) and os.path.exists(_LOCAL):
        c = json.load(open(_LOCAL, encoding="utf-8"))
        url, key = url or c.get("url", ""), key or c.get("key", "")
    return url, key


def co_cau_hinh():
    u, k = _cfg()
    return bool(u and k)


def goi(ops, timeout=60):
    url, key = _cfg()
    if not (url and key):
        raise RuntimeError("chưa có cấu hình Sheet API (.bao-mat/sheet_api.json)")
    r = requests.post(url, data=json.dumps({"key": key, "ops": ops}), headers={"Content-Type": "application/json"}, timeout=timeout)
    try:
        d = r.json()
    except Exception:
        raise RuntimeError("Sheet API trả về không phải JSON (HTTP %s) – kiểm tra Deploy 'Bất kỳ ai'" % r.status_code)
    if not d.get("ok"):
        raise RuntimeError("Sheet API lỗi: %s" % d.get("err"))
    return d["kq"]


def get(rng):
    return goi([{"op": "get", "range": rng}])[0]["values"]


def set_(rng, values):
    return goi([{"op": "set", "range": rng, "values": values}])[0]


def append(tab, values):
    return goi([{"op": "append", "tab": tab, "values": values}])[0]


def set_key(tab, key_col, key, cols):
    return goi([{"op": "setKey", "tab": tab, "keyCol": key_col, "key": key, "set": cols}])[0]


def claim(tab, key_col, key, col, match, value):
    """Giành việc nguyên tử: chỉ ghi `value` khi ô hiện tại khớp regex `match`. True = mình giành được."""
    return bool(goi([{"op": "claim", "tab": tab, "keyCol": key_col, "key": key, "col": col, "match": match, "value": value}])[0].get("claimed"))


if __name__ == "__main__":
    if sys.argv[1:2] == ["thu"]:
        if not co_cau_hinh():
            print("CHƯA CÓ cấu hình", _LOCAL); sys.exit(1)
        v = get("SPY-ADS!J1:J1")
        print("Sheet API OK – đọc được:", v)
    else:
        print(__doc__)
