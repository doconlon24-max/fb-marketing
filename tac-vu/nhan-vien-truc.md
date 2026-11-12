# Tác vụ ĐÁM MÂY: NHÂN VIÊN TRỰC – mỗi giờ (sếp chốt 10/11/2026)

Mục tiêu: Sếp duyệt / trả lời trong app QUẢN TRỊ MERAH xong thì các phòng làm NGAY (chậm nhất ~1 tiếng), máy tắt vẫn chạy.
Chạy mỗi giờ, TRỪ giờ có lượt quét chính (9h, 13h, 17h, 21h VN). Báo cáo tiếng Việt. Đọc `tai-nguyen/app-merah-studio.md` và `tac-vu/quet-tu-lieu-dam-may.md`.

## Bước 1 – Kiểm tra nhanh (phải xong trong ~1 phút, KHÔNG làm gì khác nếu không có việc)
Đọc Sheet `{{ID_DRIVE}}`:
1. Tab `HOI-SEP` A1:G300: dòng có cột E (sếp trả lời) mà cột F CHƯA có chữ `Đã xử lý`.
2. Tab `QUANG-CAO` A1:L500: dòng I = `Đã duyệt` mà L (ID post) còn trống.
3. Tab đầu (bài page): dòng I = `Đã duyệt` hoặc `Cần sửa`.
4. Drive: tư liệu mới trong 70 phút qua – `search_files` với `modifiedTime > '<now-70m>'` trong `TƯ LIỆU ĐĂNG BÀI`, `TƯ LIỆU QUẢNG CÁO/SPA`, `TƯ LIỆU QUẢNG CÁO/SPY` (thư mục ngày bên trong).
Không có gì → trả lời đúng 1 dòng "Trực: không có việc." rồi DỪNG (không commit, không email).

## Bước 1b – Tránh làm trùng
`git pull origin main` rồi đọc `trang-thai/quang-cao/<yyyy-mm-dd>.json`: chỉ coi là "lượt khác đang làm" khi file có `"ket_thuc": false` VÀ `cap_nhat_luc` cách đây < 30 phút. Nếu `ket_thuc` = true, hoặc không có, hoặc cũ hơn 30 phút → lượt trước đã dừng, CỨ LÀM TIẾP phần còn lại. Khi nhận việc: ghi ngay vào file đó `{"cap_nhat_luc": "<UTC>", "dang_lam": ["VD1",…]}`, commit + push; cập nhật `cap_nhat_luc` sau mỗi video (ghi `"ket_thuc": false` khi đang làm). **Trước khi kết thúc lượt (dù xong hay chưa) PHẢI ghi `"ket_thuc": true`**, commit + push.

**LÀM HẾT TRONG MỘT LƯỢT:** có N video thì dựng lần lượt đủ N video trong cùng lượt, KHÔNG dừng sau 1 video. Chỉ dừng khi xong hết hoặc gặp lỗi không tự sửa được.

## Bước 2 – Có việc thì làm luôn (đúng quy trình `tac-vu/quet-tu-lieu-dam-may.md`)
- Chạy `bash tai-nguyen/scripts/chuan_bi_dam_may.sh` trước mọi việc video (rclone Drive + opencv). Thiếu RCLONE_DRIVE_TOKEN hoặc lỗi → email lỗi cho sếp, ghi rõ "cần dán lại mã Google cho rclone".
- Câu trả lời QC (vd "Phương án: Đồng ý… | VD1: MERAH Beauty Makati | …") → Trưởng phòng QC giao việc: tải video gốc bằng `rclone copy`, CLONE SPY thành MERAH (`spy_merah.py`, giữ nguyên nội dung gốc), mọi video qua `kiem_tra_muot.py` = MƯỢT, viết lời mới, giọng Mely (`giong_doc.py`), dựng theo phong cách (vd `dung_qc_v2.py`), nhạc + SFX. Mỗi thành phẩm: up `rclone copy` lên `MERAH/THÀNH PHẨM QUẢNG CÁO/<dd-mm-yyyy>/VDx.mp4`, thêm dòng tab `QUANG-CAO` (mỗi page sếp tích = 1 dòng, H = page, F = link Drive).
  - **KHÔNG BAO GIỜ đăng khi Sếp chưa duyệt video (sếp chốt 10/11/2026).** Làm xong: Content QC viết caption vào **cột M** tab `QUANG-CAO` (app hiện bản xem trước bài Facebook = video cột F + caption cột M); link Drive cột F phải là link file video (`https://drive.google.com/file/d/<id>/view`, lấy bằng `rclone lsjson` hoặc Drive search), I = `Chờ duyệt đăng` (đã có page sếp tích ở H) hoặc `Chờ chọn page` (chưa có page). Email sếp link Drive để xem.
  - Sếp xem video trong app (Quản trị QC → Thành phẩm / Đăng bài lên page) và bấm **Duyệt đăng** → I = `Đã duyệt` → lượt trực/quét kế tiếp mới đăng.
- Dòng `QUANG-CAO` I = `Đã duyệt` → tải video từ Drive (rclone), viết caption (Content QC), đăng công khai đúng page cột H bằng `fb_api.py reel "<page>" …`, ghi ID post cột L, I = `Đã đăng page`.
- Câu trả lời page "Có, cần đăng" → làm theo mục NGÀY KHÔNG CÓ TƯ LIỆU bên dưới. "Không cần đăng" → bỏ.
- Bài page `Đã duyệt` có E = `Ý tưởng` HOẶC **cột G (link ảnh/video) trống** → KHÔNG đăng, coi là ý tưởng Sếp đã duyệt → Media làm hình (bước 3 mục dưới), xong để lại `Chờ duyệt`.
- Bài page `Đã duyệt` → đăng / hẹn giờ như PHẦN 2 của quy trình quét.
- Làm xong mỗi câu hỏi → ghi `Đã xử lý <giờ>` vào cột F của dòng HOI-SEP đó (ghi đúng ô, không ghi đè dòng khác).
- Video dài: dựng lần lượt, mỗi video xong thì up + ghi Sheet ngay; hết thời gian thì để lượt sau làm tiếp (ghi tiến độ vào `trang-thai/quang-cao/<ngày>.json`).
- Cập nhật văn phòng ảo (doc `office/status`, mã nhân viên trong `tai-nguyen/app-merah-studio.md`).

## Giới hạn
Không tạo/chạy quảng cáo, không tiêu tiền. Không đăng `all` cho bài quảng cáo. Không in token/khoá. Email chỉ {{EMAIL_BAO_CAO}}. Commit + push khi có thay đổi trong kho.

## TỰ BÁO CHO SẾP – KHÔNG ĐỂ SẾP PHẢI HỎI (sếp yêu cầu 10/11/2026)
Gửi **thông báo điện thoại (PushNotification)** + **email** ({{EMAIL_BAO_CAO}}) ở MỖI mốc:
1. **Nhận việc:** "Phòng QC đã nhận việc: N video, dự kiến xong lúc …".
2. **Mỗi thành phẩm xong:** "VDx đã xong – mở app QUẢN TRỊ MERAH → Quản trị quảng cáo → Thành phẩm để xem bản xem trước và bấm Duyệt đăng" + link Drive.
3. **Gặp lỗi:** lỗi gì, đã thử gì, Sếp cần làm gì (nếu có).
4. **Hết lượt mà còn việc:** "Đã xong a/N, phần còn lại lượt trực HH:00 làm tiếp".
5. **Đăng xong:** link bài + ID post.
Mốc 2 và 5 không gộp chờ cuối lượt – gửi ngay khi xong từng cái.

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
2. **Sửa xong:** up bản mới với hậu tố phiên bản (`…_v2.mp4`, `_v3`…), GIỮ bản cũ trên Drive; cập nhật link (F / G) sang bản mới; thêm dòng `… – Sửa xong (v2): <đã sửa gì>`; đặt I = `Chờ duyệt đăng` (QC) / `Chờ duyệt` (page). Thông báo điện thoại + email.
3. App tự hiện thanh tiến độ: Đã gửi yêu cầu → Đã tiếp nhận → Đang sửa → Sửa xong – chờ duyệt (dựa vào các chữ "tiếp nhận", "Đang sửa", "Sửa xong" trong lịch sử).
**Tên file thành phẩm (khớp bài):**
- Page: `YYYY-MM-DD_HHhMM_ANH1.jpg` / `YYYY-MM-DD_HHhMM_VIDEO1.mp4` (ngày + giờ đăng PH + ảnh/video số mấy trong ngày), thư mục Drive `THÀNH PHẨM/<mã bài YYYYMMDD-HHMM>/`.
- Quảng cáo: `YYYY-MM-DD_VD1.mp4`, `YYYY-MM-DD_ANH1.jpg` (ngày thành phẩm + video/ảnh số mấy), thư mục `THÀNH PHẨM QUẢNG CÁO/<dd-mm-yyyy>/`; cột D tab QUANG-CAO ghi đúng `VD1`/`ANH1`.

## Ảnh đính kèm khi sếp "Yêu cầu sửa" (từ 10/11/2026)
Ghi chú sửa (cột J tab QUANG-CAO, cột L lịch sử tab đầu, hoặc fixNote) có thể kèm `| Ảnh: <link Drive>` – app tự tải ảnh sếp dán lên Drive `MERAH/ẢNH YÊU CẦU SỬA` (id `{{ID_DRIVE}}`, tên `sua_<qc|page>_<mã>_<yyyymmddhhmm>_<n>.jpg`). Nhân viên PHẢI tải về xem trước khi sửa: `rclone copy "merah:ẢNH YÊU CẦU SỬA" /tmp/anh-sua --include "sua_*<mã>*"` rồi đọc ảnh (Read). Làm đúng theo chỗ sếp khoanh/chỉ trong ảnh.

## NHẮC VIỆC CHẠY QC – 11/11/2026 (sếp duyệt trong chat 10/11)
Từ 0h00 VN ngày 11/11/2026, 4 đối tượng sau PHẢI đang bật: camp 120250588173210083, nhóm 120250588178570083, camp 120250588151200083, nhóm 120250589864750083 (đều tên bắt đầu "CLAUDE", đối tượng Nữ 30-64, tắt Advantage+ – KHÔNG sửa lại). Lịch chính: routine {{ID_ROUTINE}} lúc 0h00. Lượt trực đầu tiên sau 0h10 VN 11/11: đọc status 4 ID qua Meta Ads; cái nào còn PAUSED (mà tên bắt đầu CLAUDE) thì bật bằng ads_activate_entity, ghi nhat-ky-chay-qc.md, email {{EMAIL_BAO_CAO}} "[MERAH QC] Bật dự phòng camp CLAUDE". Đã ACTIVE hết thì bỏ qua. Không đụng camp khác, không đổi ngân sách. Hết hiệu lực sau 12h00 VN 11/11.

## Video QC – nhắc nhanh (10/11/2026)
- Dùng `tai-nguyen/scripts/video/spy_merah.py` (bản mới nhất), mẫu `quang-cao/test-video/spy_ee79_mau.json`: BẮT BUỘC có `truoc_sau` (bản đồ BEFORE/AFTER, giữ BEFORE 3–5s khoanh vấn đề, rồi mới chuyển AFTER), `che` (che chữ cũ, không làm mờ), `loi` (voice Mely – mỗi câu ngắn, không đè câu sau).
- Nhạc AI tạo ra (`tai-nguyen/am-nhac/tham-my/ai_*.mp3`) phải **commit vào kho** để lần sau dùng lại, không tạo lại tốn credit.
- Google Sheet id chính xác: `{{ID_DRIVE}}` (chữ X hoa) – báo "not found" là gõ sai id.
- Sửa xong mỗi video: up Drive, ghi Sheet (I = `Chờ duyệt đăng`, F link mới, N lịch sử "Sửa xong (vN)…"), báo điện thoại + email ngay, rồi làm video kế tiếp – làm hết trong một lượt.


## LUẬT CỦA SẾP (chốt 10/11/2026) – áp dụng cho MỌI lượt chạy
1. **Yêu cầu của Sếp là làm ngay**: thấy yêu cầu (sửa, duyệt, trả lời, việc mới) → tiếp nhận + giao đúng nhân viên + làm luôn trong lượt này, ghi tiến độ cho Sếp thấy. Không để lượt sau, không im lặng.
2. **Sau khi hết hạn mức (usage limit) được reset**: lượt đầu tiên chạy được KHÔNG chỉ làm việc của giờ hiện tại mà phải **bù toàn bộ việc tồn**: quét lại từ lần chạy thành công cuối (xem `trang-thai/` + nhật ký) tới giờ.
3. **Bài đăng quá giờ vì hết hạn mức**: bài đã `Đã duyệt` mà giờ đăng đã qua và chưa lên page → **đăng ngay lập tức** (đăng thẳng, không hẹn giờ vào quá khứ), đúng page đã chọn; ghi nhật ký "đăng bù lúc HH:MM (trễ do hết hạn mức)" và báo Sếp. Bài CHƯA duyệt vẫn không được đăng – chỉ nhắc Sếp duyệt.
4. **Việc làm dở**: khoá `trang-thai/**.json` có `ket_thuc=false` (dù chưa quá 30 phút nếu lượt trước bị cắt do hạn mức), video/ảnh dở, yêu cầu sửa chưa xong, báo cáo QC 0h00 bị lỡ, tư liệu mới chưa xử lý → làm tiếp cho xong hết trong lượt này, rồi báo Sếp một tin tổng hợp những gì đã bù.

## DỜI LỊCH BÀI PAGE – phải cập nhật đúng ngày mới (sếp chốt 11/11/2026)
Bài nào đăng/hẹn giờ KHÁC ngày giờ đã ghi (đăng muộn vì quá giờ, hết hạn mức, duyệt muộn, sếp bảo dời, trùng giờ…): ngay sau khi đăng/hẹn giờ phải sửa dòng của bài ở tab đầu Google Sheet: **B Ngày** (yyyy-mm-dd), **C Giờ PH** (HH:MM), **D Giờ VN** (= PH − 1 giờ) đúng thời điểm thực tế; ghi K "Dời lịch dd/mm HH:MM → dd/mm HH:MM (lý do)" và thêm 1 dòng vào L. Giữ nguyên Mã bài (cột A). App tự chuyển bài sang ngày mới và ghi lịch sử. TUYỆT ĐỐI không để bài nằm ở ngày cũ.

## ĐĂNG BÀI ĐÃ DUYỆT (Sếp cho phép 11/11/2026 – đã ghi cả trong lời giao việc của routine)
- Chỉ đăng bài page / bài QC có trạng thái `Đã duyệt` (Sếp bấm Duyệt trong app). `Cần sửa` / `Chờ duyệt` / chưa duyệt: KHÔNG đăng.
- Ngày/giờ trong Sheet đã qua (quá hạn) → đăng NGAY (`fb_api.py … ` không `--at`).
- Ngày/giờ còn ở tương lai (kể cả Sếp vừa chuyển ngày/giờ) → hẹn giờ ĐÚNG ngày giờ đó (`--at "YYYY-MM-DD HH:MM"`, giờ PH).
- Bài đã hẹn giờ mà Sếp đổi ngày/giờ → huỷ bài hẹn giờ cũ (chưa hiển thị, bằng ID) rồi hẹn lại giờ mới.
- Xong: ghi `Đã đăng` / `Đã lên lịch` + ID post vào Sheet, báo Sếp (điện thoại + email). Không đăng 3 page cấm, không sửa/xoá bài đã hiển thị.

## TIN 24H (Story) – mỗi lượt trực đều kiểm tra (sếp nhắc 11/11/2026: hay bị quên)
- Mọi bài PAGE đã đăng (kể cả bài hẹn giờ vừa tới giờ) phải có Tin 24h trên cùng các page: `fb_api.py story-photo all <story.jpg | ảnh đầu>` hoặc `story-video all <video>` (API chỉ đăng Tin ngay, không hẹn giờ được).
- Mỗi lượt: bài page có giờ đăng đã qua + đã đăng/đã lên lịch mà cột K CHƯA có dòng `TIN 24H: đã đăng` → đăng Tin NGAY, rồi ghi `TIN 24H: đã đăng dd/mm HH:MM (n page)` vào cột K. Kiểm tra GET /{page}/stories nếu nghi trùng. Không đăng Tin 2 lần cho 1 bài.
- Bài QC (tab QUANG-CAO) không cần Tin 24h trừ khi Sếp ghi.

## BÙ VIỆC SAU KHI HẾT HẠN MỨC / LỖI (sếp yêu cầu 11/11/2026)
Khi đám mây bị dừng vì hết hạn mức sử dụng (giới hạn 5 giờ) hoặc lỗi, các lượt bị lỡ KHÔNG tự chạy lại. Vì vậy MỖI lượt trực, trước mọi việc khác, làm bước BÙ:
1. Bài page/QC `Đã duyệt` mà giờ đăng đã qua và chưa có ID post → đăng NGAY.
2. Bài page đã đăng mà thiếu Tin 24h → đăng Tin ngay.
3. Dòng `Cần sửa` chưa ai tiếp nhận, câu trả lời HOI-SEP chưa xử lý, tư liệu mới chưa làm → làm luôn trong lượt này.
4. Báo Sếp 1 tin tổng hợp: "Bù việc sau gián đoạn: đã đăng …, đã đăng Tin …, đang sửa …".


## Phối hợp Content + Media + Video (sếp chốt 11/11/2026)
Ngày có tư liệu page: cả 3 (merah-content, merah-media, merah-video) **họp ý tưởng trước**: xem hết tư liệu, chọn ý tưởng cho từng bài (chủ đề, hook, ảnh/đoạn dùng, dạng, chữ trên hình, hướng caption), ghi `trang-thai/<yyyy-mm-dd>-y-tuong-page.md`. Sau đó mỗi người làm phần mình **theo đúng ý tưởng đó**; caption viết khớp hình đã làm xong.

## Tư liệu up lẻ ở thư mục gốc (sếp chốt 11/11/2026)
Sếp có thể up ảnh/video thẳng vào gốc `TƯ LIỆU ĐĂNG BÀI/` (không tạo thư mục ngày). Mỗi lượt: thấy file lẻ ở gốc (trừ `_NOTE-MAU.txt`) → `rclone moveto` từng file vào `TƯ LIỆU ĐĂNG BÀI/<dd-mm-yyyy theo giờ VN>/` rồi xử lý như tư liệu ngày đó. `_NOTE-MAU.txt` vừa được sửa (cùng lúc với file mới) → chép thành `NOTE.txt` trong thư mục ngày đó (KHÔNG xoá file mẫu). Không được bỏ qua tư liệu chỉ vì không nằm trong thư mục ngày. (Không chuyển thư mục vào chính nó: `rclone move` gốc → con báo lỗi, phải `moveto` từng file.)

9. **Drive chỉ giữ bản cuối** (sếp 11/11): khi nộp bản sửa mới (v2, v3…) lên THÀNH PHẨM / THÀNH PHẨM QUẢNG CÁO, chuyển bản cũ của CÙNG thành phẩm vào thùng rác Drive (`rclone deletefile --drive-use-trash=true …`), cập nhật link mới vào Sheet. Không xoá vĩnh viễn, không đụng tư liệu gốc (TƯ LIỆU…).

## TIẾN ĐỘ TƯ LIỆU NGUỒN – BẮT BUỘC (sếp chốt 11/11/2026)
Mỗi thư mục ngày tư liệu (PAGE = TƯ LIỆU ĐĂNG BÀI/<dd-mm-yyyy>, SPA/SPY = TƯ LIỆU QUẢNG CÁO/SPA|SPY/<dd-mm-yyyy>) phải có 1 dòng ở tab **TIEN-DO-TU-LIEU** của Google Sheet: A Khoá `PAGE/11-11-2026` (hoặc `SPA/…`, `SPY/…`), B Loại, C Thư mục ngày, D TRẠNG THÁI, E Ghi chú, F Cập nhật lúc (giờ VN `dd/mm HH:MM`), G Lịch sử (thêm 1 dòng mỗi lần: `dd/mm HH:MM – ai – việc`). Chưa có dòng thì thêm vào dòng trống đầu tiên; có rồi thì sửa đúng dòng đó.
- Vừa thấy thư mục mới → D = `Đã tiếp nhận` NGAY (trước cả khi tải file).
- Bắt đầu tải/che mặt/dựng → D = `Đang xử lý`, E ghi đang làm gì.
- Làm xong, thành phẩm đã lên Sheet chờ duyệt → D = `Xử lý xong`, E ghi ra những gì (mã bài/VD, số ảnh/video).
- Hỏng/thiếu/bị chặn → D = `Lỗi: <lý do>` và email sếp.
App hiện thanh tiến độ này dưới từng thư mục ở mục File nguồn; thư mục quá 20 phút chưa có dòng sẽ hiện đỏ "Chưa có ai tiếp nhận". Dừng giữa chừng (hết lượt/hạn mức) thì để `Đang xử lý` + ghi E còn thiếu gì để lượt sau làm tiếp.

## ⚠ CHUẨN BẮT BUỘC ẢNH/VIDEO PAGE (sếp phạt lỗi 11/11/2026)
Đọc và làm đúng `tai-nguyen/mau-thiet-ke/da-dang/README.md` + xem 28 bài đã đăng `tai-nguyen/mau-thiet-ke/da-dang/mau_*.jpg` TRƯỚC khi làm.
- Ảnh page KHÔNG BAO GIỜ là ảnh thô: phải thiết kế như mẫu (logo MR, tiêu đề serif, khung/decor, pill ưu đãi). Làm bằng **Higgsfield** (ảnh thật làm đầu vào + mẫu cùng loại làm tham chiếu, `gpt_image_2_6` high 2k 3:4), chỉ lỗi mới dựng PIL.
- Che mặt khách = **sticker** (Giáng sinh: mặt ông già Noel; thường: tim hồng). CẤM ô vuông mờ/pixel/blur.
- Video **dựng bằng code** (PIL + ffmpeg / script trong `tai-nguyen/scripts/video/`): mở đầu tiêu đề + decor đúng mùa, sticker che mặt bám theo khung, chữ nhấn đẹp, nhạc + SFX, outro logo + ưu đãi/CTA. Higgsfield chỉ khi cần hình AI. CẤM video thô + 1 dòng chữ.
- Tự kiểm: đặt thành phẩm cạnh 2–3 mẫu cùng loại; kém hơn rõ rệt → làm lại trước khi up.

## Số ảnh mỗi bài page (sếp chốt 11/11/2026)
Bài ảnh đăng page CHỈ được **1 ảnh, 3 ảnh hoặc 4 ảnh** (không 2, không 5+). Tư liệu nhiều ảnh → chọn/ghép đúng 1, 3 hoặc 4 ảnh thiết kế cùng bộ. Làm xong TỰ ĐỘNG tải lên Drive `THÀNH PHẨM (ảnh, video chờ duyệt)/<mã bài>/` (tên `yyyy-mm-dd_HHhMM_ANH<n>.jpg`) và ghi dòng Sheet trạng thái Chờ duyệt – không chờ ai nhắc.
**Video page mùa Giáng sinh:** dùng công cụ mẫu `tai-nguyen/scripts/video/build_xmas_mau.py` (bản mới nhất: `bai-cho-duyet/20261111-1900/nguon/build_xmas.py`, che mặt bằng sticker ông già Noel `santa.png`): dây thông + tuyết + kim tuyến, thẻ chữ đỏ/nâu viền vàng, hook → ảnh thẻ → ưu đãi 40% / quà đến ₱10,000 → bài cũ → outro kem, luôn có nhạc Giáng sinh.

## Video QC dựng bằng HyperFrames (thiết kế chuẩn PC07 – sếp chốt 11/11/2026)
- Dựng theo `.claude/agents/merah-ads-video.md` mục "THIẾT KẾ CHUẨN". Cần Node (`node -v`) + `npx --yes hyperframes@0.9.30` (tự tải trình duyệt khi render). Không chạy được trên đám mây → dựng dự phòng bằng spy_merah.py, ghi rõ "chưa phải bản HyperFrames" vào cột K và báo Sếp.
- Up bản mới xong: chuyển bản cũ của cùng VD vào thùng rác Drive (`trash_file`).


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
