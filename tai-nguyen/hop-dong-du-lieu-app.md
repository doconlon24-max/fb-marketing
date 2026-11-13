# App MERAH Studio – 3 phòng (sếp duyệt 10/11/2026)

App (artifact `{{ID_KET_NOI}}`) đọc/ghi Google Sheet `MERAH – DUYỆT BÀI` (id `{{ID_DRIVE}}`), Google Drive và Meta Ads (chỉ đọc). Nhân viên/tác vụ đám mây phải ghi đúng chỗ dưới đây để app hiện ra.

## 1. QUẢN TRỊ PAGE
| Mục | Nguồn dữ liệu app đọc |
|---|---|
| File nguồn tư liệu | Drive `MERAH/TƯ LIỆU ĐĂNG BÀI/<d-m-yyyy>/` |
| Content ý tưởng | db ideas + câu hỏi tab `HOI-SEP` |
| Media | công cụ chỉnh ảnh + video trong app |
| Thành phẩm | Drive `THÀNH PHẨM (ảnh, video chờ duyệt)/<mã bài YYYYMMDD-HHMM>/` – chỉ ảnh/video, KHÔNG cần lưu content |
| Đăng bài | lịch + tab đầu Sheet (cột I trạng thái) |

**Quy tắc phòng (10/11/2026):**
- Ngày CÓ tư liệu → **HỌP Ý TƯỞNG TRƯỚC (sếp chốt 11/11/2026)**: Content + Media + Video cùng xem HẾT tư liệu (đọc NOTE.txt, ghép ảnh nhỏ xem tổng, trích khung video), rồi chọn **ý tưởng cho từng bài** (ưu tiên 3 bài: 2 ảnh + 1 video): chủ đề, câu hook, dùng ảnh/đoạn nào, dạng (ảnh đơn/carousel/Reels), hướng chữ trên hình, hướng caption. Ghi vào `trang-thai/<yyyy-mm-dd>-y-tuong-page.md`. Sau đó **từ ý tưởng đã chọn** Media làm ảnh, Video làm video (chỉ có ảnh → video chuyển cảnh chuyên nghiệp: nhạc, chuyển cảnh mượt, ít chữ, logo), Content viết caption khớp đúng hình. Không làm hình trước rồi mới nghĩ nội dung; không viết caption tách rời hình.
- Ngày KHÔNG có tư liệu → ghi 1 dòng tab `HOI-SEP`: `A mã HS-<yyyymmdd>-PAGE | B ngày | C "Quản trị page" | D "Hôm nay không có tư liệu. Có cần đăng bài không?" | E (sếp trả lời) | F ghi chú`. Sếp trả lời "Có, cần đăng" → lên ý tưởng (1 bài) để duyệt trong app (trạng thái Chờ duyệt, chỉ chủ đề + hướng hình) → duyệt xong mới làm ảnh HOẶC video, dùng tư liệu cũ (da-dang, thư viện) hoặc AI nếu không có tư liệu hợp chủ đề → viết caption. "Không cần đăng" → nghỉ.

## 2. QUẢN TRỊ QUẢNG CÁO
| Mục | Nguồn |
|---|---|
| File nguồn | Drive `MERAH/TƯ LIỆU QUẢNG CÁO/<d-m-yyyy>/SPA|SPY` + câu hỏi tab `HOI-SEP` (C = "Quản trị QC") |
| Content ý tưởng | db ads (concept) |
| Media quảng cáo | công cụ trong app |
| Thành phẩm | Drive `MERAH/THÀNH PHẨM QUẢNG CÁO` (id `{{ID_DRIVE}}`) / `<d-m-yyyy>/` ; **tên file có mã**: `VD1.mp4`, `VD2.mp4`, `ANH1.jpg`… (đánh số trong ngày) |
| Đăng bài lên page | tab `QUANG-CAO`: A Mã `QC-<yyyymmdd>-VD1` · B Ngày thành phẩm (dd/mm/yyyy) · C SPA/SPY · D Tên (VD1…) · E Ảnh/Video · F Link Drive · G Phong cách · **H PAGE (sếp chọn)** · I TRẠNG THÁI (`Chờ chọn page` → sếp: `Đã duyệt` → hệ thống: `Đã đăng page`) · J ghi chú · K nhật ký · **L ID POST** · **M CAPTION** (Content QC viết; app ghép F + M thành bản xem trước bài Facebook để Sếp duyệt). Chỉ đăng dòng I = Đã duyệt, đúng page ở H. |

Câu hỏi QC trong `HOI-SEP`: D ghi đủ phong cách đề xuất, số quảng cáo, hỏi page; sếp trả lời bằng chữ ở cột E (vd "PC1, 2 quảng cáo, page Merah Beauty Makati").

## 3. QUẢNG CÁO (chỉ đọc Meta Ads khi sếp bấm Đồng bộ)
- **Đặt tên quảng cáo mới có mã thành phẩm**: `CLAUDE - dd/mm - DỊCH VỤ - VD1` (camp lượt mua: `CLAUDE - LM - dd/mm - DỊCH VỤ - VD1`), dd/mm = **ngày thành phẩm**. App tự khớp số liệu vào dòng VD1 của ngày đó. Quảng cáo cũ không đổi tên (app hiện theo tên chiến dịch).
- Đánh giá: Vòng 1 camp tin nhắn Win khi giá mess ≤ 10.000đ; Vòng 2 camp lượt mua Win khi CPO ≤ 500.000đ (tiêu > 1tr chưa mua = Không win). KHÔNG gộp trung bình 2 loại camp; giá mess của camp lượt mua chỉ tham khảo; CPO tổng = tổng tiền 2 loại ÷ tổng lượt mua (tham khảo).
- Nhãn chiến dịch Tốt/Khá/Tệ: app tự tính theo KPI (Tốt ≤ KPI, Khá ≤ 1,5×KPI, Tệ hơn). **Chạy QC ghi đè + ghi chú** vào tab `QC-DANH-GIA`: A ID chiến dịch (hoặc tên thành phẩm như `VD1`) · B Tên · C Cấp (Chiến dịch/Thành phẩm) · D Nhãn (Tốt/Khá/Tệ hoặc Win/Không win) · E Ghi chú ngắn · F cập nhật lúc. Mỗi báo cáo quảng cáo hằng ngày cập nhật tab này (ghi đè dòng cùng ID).

## Văn phòng ảo (artifact 5ee0b1fb…, doc `office/status`)
Mã nhân viên để ghi trạng thái: coordinator, content, media, video, publisher (Phòng 1 · Quản trị page) · truong_phong, ads_content, ads_media, ads_video (Phòng 2 · Quản trị QC) · ads_runner (Phòng 3 · Quảng cáo) · manager, secretary (Phòng Sếp). Trạng thái: ranh / lam / cho / xong.

## ID POST (sếp chốt 10/11/2026)
**1 thành phẩm (video/ảnh QC + content) = 1 bài trên page = 1 ID post.** Đăng xong → ghi ngay ID trả về (dạng `pageid_postid`) vào cột **L** tab `QUANG-CAO` cùng dòng, I = `Đã đăng page`. Chạy QC lên camp bằng **đúng bài đó** ("Dùng bài viết hiện có" + nhập ID post ở cột L), tên quảng cáo có mã VDx của thành phẩm. App hiện cột ID post ở "Đăng bài lên page" và "Thành phẩm đã test".

## Thư mục tư liệu QC (10/11/2026)
`TƯ LIỆU QUẢNG CÁO/SPA/<dd-mm-yyyy>/` và `TƯ LIỆU QUẢNG CÁO/SPY/<dd-mm-yyyy>/` (SPA id `{{ID_DRIVE}}`, SPY id `{{ID_DRIVE}}`). App hiện 2 khối SPA và SPY trong mục File nguồn tư liệu – Quảng cáo.

## Hỏi Sếp bằng Ô TÍCH (sếp chốt 10/11/2026)
Mọi câu hỏi chọn page / phương án phải để Sếp TÍCH, không bắt Sếp gõ chữ:
- Trong app: ghi dòng tab `HOI-SEP` với cột **G = JSON** `{"phuong_an":["Đồng ý…","Chia lại (ghi rõ)"],"chon_page":[{"ten":"VD1","mo_ta":"bd47 · PC01 · MAXFILL"},…]}` → app hiện bảng tích (mỗi VD × 10 page) + nút Gửi lựa chọn. Câu trả lời về cột E dạng `Phương án: … | VD1: Page A, Page B | VD2: … | Ghi chú: …`.
- Trong chat: hiện biểu mẫu tích (widget) với danh sách 10 page cho từng VD.
- 1 VD tích nhiều page = đăng thành NHIỀU bài riêng (mỗi page 1 dòng tab `QUANG-CAO`, mỗi dòng 1 ID post).

**Ghi tab HOI-SEP / QUANG-CAO:** luôn đọc cột A trước rồi ghi vào DÒNG TRỐNG ĐẦU TIÊN (không ghi đè dòng có sẵn). Công cụ `update_values` của Google Sheets KHÔNG nhận tham số `valueInputOption` – đừng gửi.

## NGÀY KHÔNG CÓ TƯ LIỆU – quy trình 2 lần duyệt (sếp chốt 10/11/2026)
1. **Sếp trả lời "Có, cần đăng"** (tab `HOI-SEP`, phòng Quản trị page) → Content (`merah-content`) lên **1 ý tưởng**: chủ đề + hướng hình (ảnh hay video, cảnh gì) + caption nháp tiếng Anh, khung giờ trống gần nhất hôm nay (ưu tiên 19:00 PH).
   Ghi 1 dòng tab đầu Sheet: A mã `YYYYMMDD-HHMM`, E Dạng = `Ý tưởng`, F chủ đề, H caption nháp, I = `Chờ duyệt`, K = "Ý tưởng chờ Sếp duyệt – duyệt xong mới làm ảnh". Ghi `Đã xử lý` vào cột F của dòng HOI-SEP. Thông báo điện thoại + email: "Có ý tưởng bài page chờ duyệt".
2. **Sếp duyệt ý tưởng** trong app (Quản trị page → Đăng bài lên fanpage, mở bài → Duyệt / Yêu cầu sửa).
3. Dòng có E = `Ý tưởng` và I = `Đã duyệt` → **Media làm hình** (KHÔNG đăng): ưu tiên tư liệu cũ hợp chủ đề (Drive/thư viện); không có → **ảnh AI bằng `tai-nguyen/scripts/higgsfield.py`** (Ideogram 4.0 khi cần chữ, SOUL V2 cho ảnh chân thực; ghép logo/mẫu MERAH; không kim tiêm, không mặt khách giả làm khách thật). Lưu Drive `THÀNH PHẨM/<mã>/`.
4. Content hoàn thiện caption theo hình → cập nhật dòng: E = `Ảnh đơn`/`Reels`, G = link Drive, H = caption, **I = `Chờ duyệt`**, K = "Đã có hình – chờ Sếp duyệt đăng". Thông báo Sếp.
5. **Sếp duyệt lần 2** → đăng / hẹn giờ như bình thường (PHẦN 2 quy trình quét). Chỉ 1 bài cho ngày không có tư liệu.

## Yêu cầu sửa – tiến độ, lịch sử, tên file (sếp chốt 10/11/2026)
Sếp KHÔNG sửa tay – chỉ bấm **Duyệt** hoặc **Yêu cầu sửa** trong app. Khi có yêu cầu sửa (QUANG-CAO I = `Cần sửa` / bài page I = `Cần sửa`):
1. **Tiếp nhận ngay:** thêm 1 dòng vào lịch sử (QC: cột N; page: cột L) `dd/mm HH:MM – <phòng> đã tiếp nhận sửa`, rồi đặt I = `Đang sửa` + thêm dòng `… – Đang sửa: <sẽ làm gì>`.
2. **Sửa xong:** up bản mới với hậu tố phiên bản (`…_v2.mp4`, `_v3`…), cập nhật link (F / G) xong thì **XOÁ HẾT bản cũ** cùng mã trên Drive (`rclone deletefile`, vào Thùng rác) và file nháp/ảnh nền tạm – thư mục thành phẩm chỉ giữ bản cuối cùng (sếp chốt 12/11/2026); cập nhật link (F / G) sang bản mới; thêm dòng `… – Sửa xong (v2): <đã sửa gì>`; đặt I = `Chờ duyệt đăng` (QC) / `Chờ duyệt` (page). Thông báo điện thoại + email.
3. App tự hiện thanh tiến độ: Đã gửi yêu cầu → Đã tiếp nhận → Đang sửa → Sửa xong – chờ duyệt (dựa vào các chữ "tiếp nhận", "Đang sửa", "Sửa xong" trong lịch sử).
**Tên file thành phẩm (khớp bài):**
- Page: `YYYY-MM-DD_HHhMM_ANH1.jpg` / `YYYY-MM-DD_HHhMM_VIDEO1.mp4` (ngày + giờ đăng PH + ảnh/video số mấy trong ngày), thư mục Drive `THÀNH PHẨM/<mã bài YYYYMMDD-HHMM>/`.
- Quảng cáo: `YYYY-MM-DD_VD1.mp4`, `YYYY-MM-DD_ANH1.jpg` (ngày thành phẩm + video/ảnh số mấy), thư mục `THÀNH PHẨM QUẢNG CÁO/<dd-mm-yyyy>/`; cột D tab QUANG-CAO ghi đúng `VD1`/`ANH1`.

## Ảnh đính kèm khi sếp "Yêu cầu sửa" (từ 10/11/2026)
Ghi chú sửa (cột J tab QUANG-CAO, cột L lịch sử tab đầu, hoặc fixNote) có thể kèm `| Ảnh: <link Drive>` – app tự tải ảnh sếp dán lên Drive `MERAH/ẢNH YÊU CẦU SỬA` (id `{{ID_DRIVE}}`, tên `sua_<qc|page>_<mã>_<yyyymmddhhmm>_<n>.jpg`). Nhân viên PHẢI tải về xem trước khi sửa: `rclone copy "merah:ẢNH YÊU CẦU SỬA" /tmp/anh-sua --include "sua_*<mã>*"` rồi đọc ảnh (Read). Làm đúng theo chỗ sếp khoanh/chỉ trong ảnh.

## DỜI LỊCH BÀI PAGE – phải cập nhật đúng ngày mới (sếp chốt 11/11/2026)
Bài nào đăng/hẹn giờ KHÁC ngày giờ đã ghi (đăng muộn vì quá giờ, hết hạn mức, duyệt muộn, sếp bảo dời, trùng giờ…): ngay sau khi đăng/hẹn giờ phải sửa dòng của bài ở tab đầu Google Sheet: **B Ngày** (yyyy-mm-dd), **C Giờ PH** (HH:MM), **D Giờ VN** (= PH − 1 giờ) đúng thời điểm thực tế; ghi K "Dời lịch dd/mm HH:MM → dd/mm HH:MM (lý do)" và thêm 1 dòng vào L. Giữ nguyên Mã bài (cột A). App tự chuyển bài sang ngày mới và ghi lịch sử. TUYỆT ĐỐI không để bài nằm ở ngày cũ.

## TIẾN ĐỘ TƯ LIỆU NGUỒN – BẮT BUỘC (sếp chốt 11/11/2026)
Mỗi thư mục ngày tư liệu (PAGE = TƯ LIỆU ĐĂNG BÀI/<dd-mm-yyyy>, SPA/SPY = TƯ LIỆU QUẢNG CÁO/SPA|SPY/<dd-mm-yyyy>) phải có 1 dòng ở tab **TIEN-DO-TU-LIEU** của Google Sheet: A Khoá `PAGE/11-11-2026` (hoặc `SPA/…`, `SPY/…`), B Loại, C Thư mục ngày, D TRẠNG THÁI, E Ghi chú, F Cập nhật lúc (giờ VN `dd/mm HH:MM`), G Lịch sử (thêm 1 dòng mỗi lần: `dd/mm HH:MM – ai – việc`). Chưa có dòng thì thêm vào dòng trống đầu tiên; có rồi thì sửa đúng dòng đó.
- Vừa thấy thư mục mới → D = `Đã tiếp nhận` NGAY (trước cả khi tải file).
- Bắt đầu tải/che mặt/dựng → D = `Đang xử lý`, E ghi đang làm gì.
- Làm xong, thành phẩm đã lên Sheet chờ duyệt → D = `Xử lý xong`, E ghi ra những gì (mã bài/VD, số ảnh/video).
- Hỏng/thiếu/bị chặn → D = `Lỗi: <lý do>` và email sếp.
App hiện thanh tiến độ này dưới từng thư mục ở mục File nguồn; thư mục quá 20 phút chưa có dòng sẽ hiện đỏ "Chưa có ai tiếp nhận". Dừng giữa chừng (hết lượt/hạn mức) thì để `Đang xử lý` + ghi E còn thiếu gì để lượt sau làm tiếp.

## Số ảnh mỗi bài page (sếp chốt 11/11/2026)
Bài ảnh đăng page CHỈ được **1 ảnh, 3 ảnh hoặc 4 ảnh** (không 2, không 5+). Tư liệu nhiều ảnh → chọn/ghép đúng 1, 3 hoặc 4 ảnh thiết kế cùng bộ. Làm xong TỰ ĐỘNG tải lên Drive `THÀNH PHẨM (ảnh, video chờ duyệt)/<mã bài>/` (tên `yyyy-mm-dd_HHhMM_ANH<n>.jpg`) và ghi dòng Sheet trạng thái Chờ duyệt – không chờ ai nhắc.
**Video page mùa Giáng sinh:** dùng công cụ mẫu `tai-nguyen/scripts/video/build_xmas_mau.py` (bản mới nhất: `bai-cho-duyet/20261111-1900/nguon/build_xmas.py`, che mặt bằng sticker ông già Noel `santa.png`): dây thông + tuyết + kim tuyến, thẻ chữ đỏ/nâu viền vàng, hook → ảnh thẻ → ưu đãi 40% / quà đến ₱10,000 → bài cũ → outro kem, luôn có nhạc Giáng sinh.

## GHI MỐC ĐĂNG BÀI PAGE – để app hiện tiến độ (sếp chốt 11/11/2026)
App (Quản trị page → Đăng bài lên fanpage) đọc cột I + cột K tab đầu, hiện 4 bước: Đã duyệt › Đã lên lịch (hoặc Đăng ngay) › Đã đăng lên page › Đã đăng Tin 24h. Mỗi mốc ghi THÊM vào cột K đúng mẫu (giờ VN):
- Hẹn giờ xong: I = `Đã lên lịch`, K thêm `Đã hẹn giờ dd/mm HH:MM (n page)`.
- Lên page (đúng giờ hẹn hoặc đăng ngay/đăng bù): I = `Đã đăng`, K thêm `Đã đăng dd/mm HH:MM (n page[, đăng bù – lý do]). Post ID <tên page>: <pageid_postid>`.
- Tin: K thêm `TIN 24H: đã đăng dd/mm HH:MM (n page)`.
Bài hẹn giờ: tới giờ kiểm tra bài đã lên thật (GET post) rồi mới đổi I = `Đã đăng` và đăng Tin.

## BÀI QUẢNG CÁO ĐĂNG PAGE = ĐĂNG LUÔN TIN 24H (sếp chốt 11/11/2026)
Dòng tab `QUANG-CAO` I = `Đã duyệt` → đăng công khai lên đúng page cột H (`fb_api.py reel "<page>" …`), NGAY SAU ĐÓ đăng Tin 24h cùng video lên CHÍNH page đó (`fb_api.py story-video "<page>" <video>`; chỉ page cột H, không đăng 10 page). Ghi:
- L = ID post; I = `Đã đăng page`;
- K thêm `Đã đăng dd/mm HH:MM (<page>). Post ID: <pageid_postid>` rồi `TIN 24H: đã đăng dd/mm HH:MM (<page>)` (giờ VN).
Đăng Tin lỗi → ghi `TIN 24H: lỗi – <lý do>` vào K, email sếp, lượt sau thử lại. Mỗi lượt: dòng `Đã đăng page` mà K chưa có `TIN 24H: đã đăng` → đăng Tin ngay. App (Quản trị QC → Đăng bài lên page) hiện tiến độ Đã duyệt › Đã đăng page › Tin 24h từ cột I/K/L.

## SPY đối thủ + Manifold (12/11/2026) – ghi chú cho người dùng app
- Mục **Quản trị quảng cáo → SPY đối thủ**: chọn dịch vụ, quốc gia, nền tảng (bảng thả xuống có ô tích), bấm Quét. Tích **SPY** ở bài muốn làm lại → ghi tab `SPY-ADS` (I = `Dùng làm ý tưởng`, H bắt đầu `SPY-CLONE`) → nhân viên đám mây nhận trong 1–2 phút.
- **Manifold tính theo lượt:** gói miễn phí 250 lượt/tháng, tự cấp lại hằng tháng; mỗi từ khoá × mỗi nền tảng = 1 lượt; quét lại cùng từ khoá trong ngày thường không tốn. Hết lượt: Manifold ngừng trả kết quả, không tự trừ tiền; bỏ tích "Dùng Manifold" để quét bằng cách miễn phí (Meta Ad Library + tìm kiếm web: không có lượt xem TikTok, không tách video/ảnh). Gói trả phí (nếu cần): xem manifoldmcp.com/pricing – chủ tài khoản tự quyết và tự thanh toán.
- **Mỗi người dùng app phải tự kết nối Manifold** bằng tài khoản Claude của mình: claude.ai → Tuỳ chỉnh → Plugin → Manifold → Thêm → Trình kết nối → Kết nối. Lượt của ai người nấy dùng.
- Không tải được file video quảng cáo Facebook của đối thủ (chỉ có ảnh bìa + lời thoại) → EDIT video dựng lại theo cấu trúc.
- **Tiết kiệm lượt (mặc định):** Facebook/Instagram quét MIỄN PHÍ bằng kết nối Meta – vẫn hiện từng bài và tích SPY được; Manifold chỉ tốn lượt ở 3 chỗ: (1) ô "TikTok có lượt xem" khi có tích TikTok, (2) ô "Facebook quét bằng Manifold" (mặc định tắt), (3) nút "Xem chi tiết đối thủ này" – 1 lượt/đối thủ. Bài tích SPY: nhân viên đám mây dùng 1–2 lượt để lấy chi tiết + lời thoại.

## Bản chia sẻ SPA MARKETING (cập nhật 12/11/2026 – GĐ4)
- Artifact riêng, slug `{{ID_KET_NOI}}`, tạo bằng `python tai-nguyen/scripts/lam_app_chung.py merah-studio app-facebook-marketing <chk.js>` rồi thay `__APP_SLUG__` trong `index.html` bằng slug trên, `node --check`, đăng.
- Dữ liệu trong app lưu riêng từng người (`data/users/<uid>/app/`); Sheet/Drive/Meta/Manifold là của chính người mở app. Lượt Manifold tính theo tài khoản từng người (250 lượt/tháng bản miễn phí).
- Khác bản MERAH: Đo lường không ghi sẵn page (mặc định "Toàn tài khoản"); Sheet tự có thêm tab DO-LUONG, SPY-ADS, SPY-DOI-THU (Sheet cũ được bổ sung khi mở app); bấm SPY chỉ LƯU bài vào tab SPY-ADS (trạng thái `Dùng làm ý tưởng`), không tự tải video vì không có máy tải hộ.
- Sửa giao diện ở `merah-studio/src.html` xong phải chạy lại script trên để kiểm tra các chuỗi nó thay còn khớp.

## Hợp đồng TRẠNG THÁI app ↔ Google Sheet (chốt 13/11/2026 – mọi nhân viên phải theo)
Cột TRẠNG THÁI (tab bài fanpage cột I, QUANG-CAO cột I) CHỈ được ghi đúng một trong các chữ sau, không thêm chữ khác vào cột này (giải thích ghi ở cột Nhật ký):
| Ghi đúng chữ | Nghĩa | App hiện |
|---|---|---|
| `Chờ duyệt` | Nhân viên làm xong, chờ sếp xem | nút Duyệt / Yêu cầu sửa |
| `Cần sửa` | Sếp yêu cầu sửa (app ghi) | chờ nhân viên |
| `Đang sửa` | Nhân viên đã nhận việc sửa | tiến độ sửa |
| `Đã duyệt` | Sếp duyệt (app ghi) | chờ đăng |
| `Đã lên lịch` | Đã hẹn giờ trên page | đã hẹn giờ |
| `Đã đăng` (quảng cáo: `Đã đăng page`) | Đã lên page | xong, không còn nút |
| `Đã bỏ` | Sếp bỏ / bài trùng / đã gộp | ẩn khỏi app |
- Bài trùng hoặc đã gộp vào bài khác: ghi `Đã bỏ` (không ghi "Đã gộp", "TRÙNG"…). Mỗi mã bài chỉ nên có 1 dòng; nếu lỡ có 2 dòng cùng mã, app lấy dòng có trạng thái tiến xa nhất (Đã đăng > Đã lên lịch > Đã bỏ > Đã duyệt > Chờ duyệt > Đang sửa > Cần sửa).
- Đăng/hẹn giờ xong phải đổi ngay cột TRẠNG THÁI (`Đã lên lịch` / `Đã đăng`), không chỉ ghi vào Nhật ký. App tự chuyển bài `Đã lên lịch` sang `Đã đăng` khi đã qua giờ hẹn 2 tiếng.
- Chữ lạ không có trong bảng: app BỎ QUA dòng đó (không hiện), nên nhân viên ghi sai chữ = sếp không thấy bài.
- Ngày (cột B, yyyy-mm-dd) và giờ PH (cột C, HH:MM) là lịch đăng thật; sếp dời ngày trong app thì app sửa B–D, nhân viên đăng đúng theo đó.
