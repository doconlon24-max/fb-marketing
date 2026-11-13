# Tác vụ ĐÁM MÂY: TRỰC NHANH (QUẢN TRỊ QUẢNG CÁO + QUẢN TRỊ PAGE) (phút 15, 30, 45 mỗi giờ – sếp chốt 10/11/2026)

Sếp yêu cầu: **có tư liệu (quảng cáo HOẶC đăng page) là làm ngay, làm xong để chờ duyệt** – không chờ giờ quét. Cùng lượt trực phút 00 → kiểm tra mỗi 15 phút.

## Bước 1 – Kiểm tra CỰC NHANH (không đọc file khác nếu không có việc)
0. **BÁO TƯ LIỆU MỚI (từ 11/11/2026):** máy theo dõi Drive (Google Apps Script `tai-nguyen/apps-script/theo-doi-tu-lieu.gs`) mở issue GitHub "Tư liệu mới: PAGE/dd-mm-yyyy …" → lượt này chạy NGAY. Đọc tab `TIEN-DO-TU-LIEU`: mọi dòng có D trống / `Đã tiếp nhận` / `Đang xử lý` (không phải `Xử lý xong`) = CÓ VIỆC → ghi D = `Đã tiếp nhận` ngay, rồi làm luôn (PAGE theo PHẦN 1 + 1A `quet-tu-lieu-dam-may.md`; SPA/SPY theo `quang-cao/quy-trinh-tu-lieu-qc.md`), làm HẾT trong lượt này, cập nhật tiến độ từng bước. Issue có tiêu đề "THỬ" → chỉ trả lời "đã nhận được báo thử" rồi dừng.
1. Google Drive `search_files`: file trong `TƯ LIỆU QUẢNG CÁO/SPA/<ngày>/` hoặc `TƯ LIỆU QUẢNG CÁO/SPY/<ngày>/` (SPA id `{{ID_DRIVE}}`, SPY id `{{ID_DRIVE}}` – liệt kê thư mục ngày rồi file bên trong) có `modifiedTime` sau mốc đã xử lý trong `trang-thai/quang-cao/` (chưa có file trạng thái cho thư mục ngày đó = mới).
2. Sheet `{{ID_DRIVE}}`: tab `HOI-SEP` dòng phòng "Quản trị QC" có cột E mà F chưa `Đã xử lý`; tab `QUANG-CAO` dòng I = `Đã duyệt` mà L trống, hoặc I = `Cần sửa`.
   **Tab đầu (bài page)**: dòng I = `Cần sửa` (yêu cầu sửa của Sếp) – BẮT BUỘC kiểm tra mỗi lượt. Tab `HOI-SEP` mọi phòng (cả Quản trị page) có E mà F chưa `Đã xử lý`.
2b. Drive `TƯ LIỆU ĐĂNG BÀI/<d-m-yyyy>/` (id `{{ID_DRIVE}}`): thư mục ngày có file mới mà chưa có `trang-thai/tu-lieu/<ngày>.json` (hoặc có file mới hơn mốc trong đó).
3. `trang-thai/quang-cao/<ngày>.json` (sau `git pull`): còn video dở dang và `ket_thuc` = true (hoặc cũ > 30 phút).
Không có gì → trả lời "QC nhanh: không có việc." và DỪNG ngay.

## Bước 2 – Có việc: làm NGAY theo `tac-vu/nhan-vien-truc.md` (phần QC) + `quang-cao/quy-trinh-tu-lieu-qc.md`
- Tư liệu mới: file mới nhất đã sửa cách đây ≥ 5 phút (đã up xong) là nhận việc luôn – KHÔNG chờ 30 phút. Trưởng phòng QC đọc NOTE, gửi câu hỏi ô tích (HOI-SEP cột G) + thông báo điện thoại/email, chờ trả lời trong lượt (mỗi 10 phút, tối đa 60 phút) rồi làm.
- Tuân thủ khoá chống trùng (`ket_thuc`), làm hết N video trong một lượt, tự báo Sếp ở từng mốc, KHÔNG đăng khi Sếp chưa duyệt.
- **Tư liệu page mới:** file mới nhất up xong ≥ 5 phút là làm ngay theo PHẦN 1 + 1A của `tac-vu/quet-tu-lieu-dam-may.md` (media trước: 2 ảnh + 1 video, rồi content, 3 bài 07:00/11:00/19:00 PH) → Sheet `Chờ duyệt` + thông báo điện thoại/email. Tải video nặng bằng rclone.

## Ảnh đính kèm khi sếp "Yêu cầu sửa" (từ 10/11/2026)
Ghi chú sửa (cột J tab QUANG-CAO, cột L lịch sử tab đầu, hoặc fixNote) có thể kèm `| Ảnh: <link Drive>` – app tự tải ảnh sếp dán lên Drive `MERAH/ẢNH YÊU CẦU SỬA` (id `{{ID_DRIVE}}`, tên `sua_<qc|page>_<mã>_<yyyymmddhhmm>_<n>.jpg`). Nhân viên PHẢI tải về xem trước khi sửa: `rclone copy "merah:ẢNH YÊU CẦU SỬA" /tmp/anh-sua --include "sua_*<mã>*"` rồi đọc ảnh (Read). Làm đúng theo chỗ sếp khoanh/chỉ trong ảnh.

## MỌI YÊU CẦU CỦA SẾP = LÀM NGAY (sếp chốt 10/11/2026 23:00)
Thấy bất kỳ yêu cầu sửa/duyệt/trả lời nào của Sếp (QUANG-CAO I=`Cần sửa`, tab đầu I=`Cần sửa`, HOI-SEP E mới) → trong CÙNG lượt này:
1. Ghi tiếp nhận ngay: tab đầu cột L / QUANG-CAO cột N thêm dòng `<MM-DD HH:MM> – <Phòng> – đã tiếp nhận`, đổi I = `Đang sửa` (app hiện bước 2–3).
2. Giao đúng nhân viên phụ trách (media/video/content page hoặc QC) và làm luôn, không để lượt sau.
3. Xong: I = `Chờ duyệt` (link mới cột G/F), thêm dòng `… – sửa xong (vN) – chờ Sếp duyệt` + thông báo điện thoại/email.
4. Không làm được (thiếu tư liệu, bài đã qua ngày…) → vẫn ghi tiếp nhận + lý do vào lịch sử và hỏi Sếp ở HOI-SEP bằng ô tích; KHÔNG được im lặng.

## LUẬT CỦA SẾP (chốt 10/11/2026) – áp dụng cho MỌI lượt chạy
1. **Yêu cầu của Sếp là làm ngay**: thấy yêu cầu (sửa, duyệt, trả lời, việc mới) → tiếp nhận + giao đúng nhân viên + làm luôn trong lượt này, ghi tiến độ cho Sếp thấy. Không để lượt sau, không im lặng.
2. **Sau khi hết hạn mức (usage limit) được reset**: lượt đầu tiên chạy được KHÔNG chỉ làm việc của giờ hiện tại mà phải **bù toàn bộ việc tồn**: quét lại từ lần chạy thành công cuối (xem `trang-thai/` + nhật ký) tới giờ.
3. **Bài đăng quá giờ vì hết hạn mức**: bài đã `Đã duyệt` mà giờ đăng đã qua và chưa lên page → **đăng ngay lập tức** (đăng thẳng, không hẹn giờ vào quá khứ), đúng page đã chọn; ghi nhật ký "đăng bù lúc HH:MM (trễ do hết hạn mức)" và báo Sếp. Bài CHƯA duyệt vẫn không được đăng – chỉ nhắc Sếp duyệt.
4. **Việc làm dở**: khoá `trang-thai/**.json` có `ket_thuc=false` (dù chưa quá 30 phút nếu lượt trước bị cắt do hạn mức), video/ảnh dở, yêu cầu sửa chưa xong, báo cáo QC 0h00 bị lỡ, tư liệu mới chưa xử lý → làm tiếp cho xong hết trong lượt này, rồi báo Sếp một tin tổng hợp những gì đã bù.

## DỜI LỊCH BÀI PAGE – phải cập nhật đúng ngày mới (sếp chốt 11/11/2026)
Bài nào đăng/hẹn giờ KHÁC ngày giờ đã ghi (đăng muộn vì quá giờ, hết hạn mức, duyệt muộn, sếp bảo dời, trùng giờ…): ngay sau khi đăng/hẹn giờ phải sửa dòng của bài ở tab đầu Google Sheet: **B Ngày** (yyyy-mm-dd), **C Giờ PH** (HH:MM), **D Giờ VN** (= PH − 1 giờ) đúng thời điểm thực tế; ghi K "Dời lịch dd/mm HH:MM → dd/mm HH:MM (lý do)" và thêm 1 dòng vào L. Giữ nguyên Mã bài (cột A). App tự chuyển bài sang ngày mới và ghi lịch sử. TUYỆT ĐỐI không để bài nằm ở ngày cũ.

## Tư liệu up lẻ ở thư mục gốc (sếp chốt 11/11/2026)
Sếp có thể up ảnh/video thẳng vào gốc `TƯ LIỆU ĐĂNG BÀI/` (không tạo thư mục ngày). Mỗi lượt: thấy file lẻ ở gốc (trừ `_NOTE-MAU.txt`) → `rclone moveto` từng file vào `TƯ LIỆU ĐĂNG BÀI/<dd-mm-yyyy theo giờ VN>/` rồi xử lý như tư liệu ngày đó. `_NOTE-MAU.txt` vừa được sửa (cùng lúc với file mới) → chép thành `NOTE.txt` trong thư mục ngày đó (KHÔNG xoá file mẫu). Không được bỏ qua tư liệu chỉ vì không nằm trong thư mục ngày. (Không chuyển thư mục vào chính nó: `rclone move` gốc → con báo lỗi, phải `moveto` từng file.)

## TIẾN ĐỘ TƯ LIỆU NGUỒN – BẮT BUỘC (sếp chốt 11/11/2026)
Mỗi thư mục ngày tư liệu (PAGE = TƯ LIỆU ĐĂNG BÀI/<dd-mm-yyyy>, SPA/SPY = TƯ LIỆU QUẢNG CÁO/SPA|SPY/<dd-mm-yyyy>) phải có 1 dòng ở tab **TIEN-DO-TU-LIEU** của Google Sheet: A Khoá `PAGE/11-11-2026` (hoặc `SPA/…`, `SPY/…`), B Loại, C Thư mục ngày, D TRẠNG THÁI, E Ghi chú, F Cập nhật lúc (giờ VN `dd/mm HH:MM`), G Lịch sử (thêm 1 dòng mỗi lần: `dd/mm HH:MM – ai – việc`). Chưa có dòng thì thêm vào dòng trống đầu tiên; có rồi thì sửa đúng dòng đó.
- Vừa thấy thư mục mới → D = `Đã tiếp nhận` NGAY (trước cả khi tải file).
- Bắt đầu tải/che mặt/dựng → D = `Đang xử lý`, E ghi đang làm gì.
- Làm xong, thành phẩm đã lên Sheet chờ duyệt → D = `Xử lý xong`, E ghi ra những gì (mã bài/VD, số ảnh/video).
- Hỏng/thiếu/bị chặn → D = `Lỗi: <lý do>` và email sếp.
App hiện thanh tiến độ này dưới từng thư mục ở mục File nguồn; thư mục quá 20 phút chưa có dòng sẽ hiện đỏ "Chưa có ai tiếp nhận". Dừng giữa chừng (hết lượt/hạn mức) thì để `Đang xử lý` + ghi E còn thiếu gì để lượt sau làm tiếp.

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

**Seeding (12/11/2026) – NHÂN VIÊN ĐĂNG BÀI làm:** bài QC vừa lên page (có ID post) → seeding NGAY trong cùng lượt, không chờ lượt sau, bằng chính page vừa đăng theo `tac-vu/seeding-quang-cao.md` (TỐI THIỂU 10 bình luận ảnh feedback ĐÚNG DỊCH VỤ của bài, lấy từ Drive `ẢNH SEEDING QUẢNG CÁO/<dịch vụ>`), ghi K `Seeding: đã bình luận dd/mm HH:MM (N ảnh <dịch vụ>)`. Mỗi lượt: dòng `Đã đăng page` mà K chưa có `Seeding: đã bình luận` → seeding bù. App hiện thêm tích Seeding.

## Yêu cầu sửa MỚI luôn thắng ghi chú cũ (sếp phạt 11/11/2026)
Ghi chú kiểu "KHÔNG LÀM LẠI / đã làm trên máy" ở cột K chỉ áp dụng cho phiên bản lúc ghi. Nếu SAU đó Sếp bấm Yêu cầu sửa (cột I = `Cần sửa`, dòng mới trong lịch sử có giờ muộn hơn) → **phải tiếp nhận ngay** (ghi "đã tiếp nhận" vào lịch sử + I = `Đang sửa`) và làm. Không bao giờ bỏ qua yêu cầu của Sếp vì ghi chú cũ. Ghi chú trên máy cũng phải ghi kèm giờ.

## SPY ADS – yêu cầu quét sâu của Sếp (12/11/2026)
Mỗi lượt chạy đều đọc tab `SPY-ADS` A1:K3000 của Sheet `{{ID_DRIVE}}`: dòng I = `Chờ quét` hoặc `Dùng làm ý tưởng` là CÓ VIỆC → làm ngay theo mục "SPY ADS ĐỐI THỦ" trong `tac-vu/nhan-vien-truc.md` (agent `fb-spy`). Nhận việc là đổi I thành `Đang quét` NGAY (app hiện tiến độ cho Sếp), xong đổi thành `Đã quét (n video)`. Nhiều dòng `Chờ quét` trùng dịch vụ + nền tảng thì làm 1 lần, các dòng còn lại ghi `Đã quét (gộp với dòng trên)`.

**Bỏ thành phẩm (13/11/2026):** Sếp bảo bỏ thành phẩm QC nào → đổi cột I tab QUANG-CAO thành `Đã bỏ` (không để `Đã duyệt`), ghi lý do ở K. App tự ẩn dòng `Đã bỏ`.
