#!/usr/bin/env bash
# Sau MỖI lần dựng/sửa video QC: đẩy thư mục làm việc (voice, đoạn cắt, ảnh thẻ, cfg, index.html, KHÔNG render/node_modules)
# lên Drive để MÁY NÀO (PC/laptop/đám mây) cũng sửa tiếp được. (Sếp 15/11: mỗi lần sửa lại phải dựng lại từ đầu)
#   bash luu_thu_muc_lam_viec.sh <thư mục làm việc> <mã QC>   -> merah:MERAH/THƯ MỤC LÀM VIỆC QC/<mã>
#   Lấy về: rclone copy "merah:MERAH/THƯ MỤC LÀM VIỆC QC/<mã>" <thư mục>
export PATH="$HOME/bin:$PATH"
rclone copy "$1" "merah:MERAH/THƯ MỤC LÀM VIỆC QC/$2" --exclude "node_modules/**" --exclude "renders/**" --exclude "*.mov" -q && echo "đã lưu làm việc $2"
