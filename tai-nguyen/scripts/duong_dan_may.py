"""Tìm đường dẫn tài nguyên chạy được trên CẢ laptop (C:\\Users\\Surface\\...) lẫn máy trực (C:\\MERAH\\...).

Dùng: from duong_dan_may import tim
      MD = tim("model/face_detection_yunet_2023mar.onnx")
Thứ tự tìm: biến môi trường MERAH_TAI_NGUYEN (nếu có) -> máy trực C:\\MERAH\\tai-nguyen-laptop -> laptop.
Máy trực tải bản sao từ Drive "MERAH/KHO TỪ MÁY TÍNH" về C:\\MERAH\\tai-nguyen-laptop (giữ nguyên tên thư mục con).
"""
import os

KHO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # thư mục gốc kho

# tên ngắn -> đường dẫn trên laptop
LAPTOP = {
    "model": r"C:\Users\Surface\Downloads\FINE\ADS 2.10.1\model",
    "font": r"C:\Users\Surface\AppData\Local\CapCut\Apps\6.8.1.2770\Resources\Font\SystemFont",
    "CLAUDE DỰNG VIDEO": r"C:\Users\Surface\Downloads\CLAUDE DỰNG VIDEO",
    "MERAH": r"C:\Users\Surface\Downloads\MERAH",
}


def _goc():
    ds = []
    if os.environ.get("MERAH_TAI_NGUYEN"):
        ds.append(os.environ["MERAH_TAI_NGUYEN"])
    ds += [r"C:\MERAH\tai-nguyen-laptop", r"C:\MERAH"]
    return ds


def tim(rel):
    """rel dạng 'model/xxx.onnx', 'font/CapCutSansText-Bold.otf', 'CLAUDE DỰNG VIDEO/ADS SPA 5.11', 'MERAH/...'."""
    rel = rel.replace("\\", "/").strip("/")
    dau, _, duoi = rel.partition("/")
    thu = [os.path.join(g, *rel.split("/")) for g in _goc()]
    if dau in LAPTOP:
        thu.append(os.path.join(LAPTOP[dau], *duoi.split("/")) if duoi else LAPTOP[dau])
    for p in thu:
        if os.path.exists(p):
            return p
    return thu[-1]  # không thấy: trả về đường dẫn laptop để báo lỗi rõ ràng
