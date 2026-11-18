# Kiểm duyệt bình luận bằng AI (sếp chốt 16/11/2026)

Không lọc theo từ khoá. Claude ĐỌC HIỂU từng bình luận (kèm nội dung bài/quảng cáo) rồi quyết định.

## Luật
1. **Viết tắt / tiếng lóng / Taglish / emoji** → đoán nghĩa SÁT NHẤT theo ngữ cảnh bài (vd "scm" = scam, "pngt" = panget, "sna ttoo 😂" = sana totoo – mỉa mai).
2. (16/11 bổ sung) **Dịch ra được nghĩa và nghĩa xấu** (kể cả xúc phạm nhẹ như "istorbo") → AI TỰ XOÁ; app mục "Bình luận xấu → AI đã xoá" có nút **Chặn người này** để sếp quyết chặn. Câu KHÔNG dịch được / hiểu 2 kiểu → "Bình luận xấu → Chưa chắc chắn" (Xoá / Xoá + chặn / Giữ).
   **Chắc chắn là ác ý** (chửi bới, tục tĩu, giễu cợt/mỉa mai, tố lừa đảo không căn cứ, spam, quảng cáo đối thủ) → **XOÁ** luôn (`DELETE /{comment-id}` bằng page token của page sở hữu bài).
3. **Không chắc** → KHÔNG đụng, gửi lên app cho sếp xem và quyết định (Xoá / Giữ / Cấm người này).
4. **Khiếu nại thật** (có trải nghiệm cụ thể: đặt lịch, giá, kết quả, phản ứng da…) → KHÔNG xoá, đẩy lên app để trả lời.
5. Bình thường / hỏi giá / khen / bình luận của chính page (seeding) → để nguyên.
6. Mọi bình luận đã xoá đều ghi lại (page, bài, nội dung gốc, nghĩa AI hiểu, lý do) để sếp kiểm tra; AI xoá nhầm thì rút kinh nghiệm vào luật.

## Quyền (kiểm tra 16/11)
Token người dùng có `pages_read_user_content`, `pages_read_engagement`, `pages_manage_engagement` = granted; cả 14 page có task MODERATE → đọc, ẩn, xoá được. Bình luận do chính page viết thì `can_hide=false` (bỏ qua).

## Phụ trách + phạm vi (sếp chốt 16/11)
- **Nhân viên Đăng bài (phòng Quản trị fanpage)** phụ trách. App: Fanpage → **Kiểm duyệt bình luận** (lọc theo ngày, theo từng page hoặc tất cả page; mục Chờ Sếp / Khiếu nại / Đã xoá / Bình thường).
- TOÀN BỘ bình luận trên TẤT CẢ page token đang quản lý (sếp 16/11: "quét toàn bộ các page đang có" – 14 page gồm cả Beauty Jobs; page mới thêm vào token tự được quét, pages.json làm mới 1 lần/ngày): bài page + bài chạy quảng cáo. KHÔNG tính tin nhắn.
- Quét toàn bộ lịch sử (mọi bài, mọi bình luận): `kiem_duyet_bl.py quet_het` (đã chạy 16/11). Lượt 10 phút chỉ quét bình luận mới trên 100 bài gần nhất/page.
- Bài quảng cáo đăng công khai trên page: quét được (100 bài gần nhất/page). Bài quảng cáo ẨN (dark post, chỉ có trong Ads Manager) cần token có thêm quyền `ads_read` – chưa có (16/11), script tự bỏ qua.

## Máy chạy
- `tai-nguyen/scripts/kiem_duyet_bl.py chay` – canh_spy (máy trực) gọi 10 phút/lần, chạy tách rời.
- Quét Graph API (không tốn token) → tab Sheet **BINH-LUAN** ('Chờ AI'; bình luận của chính page = 'Của page', bỏ qua).
- Có 'Chờ AI' → gọi `claude -p --model sonnet` phân loại theo luật trên (lô 40 câu) → 'xoa' thì xoá ngay ('Đã xoá (AI)'), còn lại 'Chờ Sếp' / 'Khiếu nại' / 'Bình thường'.
- Sếp bấm trong app → I = 'Sếp: Xoá' / 'Sếp: Cấm' / 'Sếp: Giữ' → lượt máy kế tiếp làm → 'Đã xoá (Sếp)' / 'Đã xoá + cấm (Sếp)' / 'Giữ (Sếp)'.
- Máy trực tắt thì chưa quét (bình luận vẫn còn, máy bật lại quét bù theo mốc).
