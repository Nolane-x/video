
# Quality gates và regression tests

## P0 — chặn phát hành
File lỗi/không mở được; thiếu audio/video stream; sai tỷ lệ/thời lượng/FPS nghiêm trọng; dùng nhầm engine nhưng báo sai; file không tải được; checksum mismatch.

## P1 — lỗi hình/chuyển động lớn
Nhân vật/đạo cụ lơ lửng; tay không chạm vật; chân không chạm sàn/bậc; hành động chỉ có zoom camera; bao cát không phản ứng; crop đầu/chân ngoài ý muốn; bối cảnh lặp chung chung; caption che mặt/tay; hành động hoặc rig thay đổi không kiểm soát. Phải sửa hoặc ghi ngoại lệ rõ trước khi phát hành.

## P2 — lỗi nhỏ
Spacing, transition pop nhẹ, mức glow hoặc lệch màu nhỏ. Sửa khi ảnh hưởng cảm giác hoàn thiện hoặc đọc hiểu.

## Regression suite bắt buộc cho H2
1. Điện thoại: tay ôm/đặt đúng thiết bị; khi buông, điện thoại ở trên đúng mặt phẳng.
2. Viết: đầu bút chạm trang giấy, tay còn lại đặt hợp lý.
3. Uống: miệng/cốc/tay cùng chuyển động; không có cốc lơ lửng.
4. Buộc giày: thân cúi; tay đến dây giày chứ không phải vùng bóng/hiệu ứng.
5. Cầu thang: chân chạm bậc nhìn thấy được; thân đi lên dần; đầu không crop.
6. Đấm bao: nắm đấm tiếp xúc; bao lắc; tay hồi về tư thế thủ.
7. Tương tác hai người: hướng nhìn khác biệt rõ khi nói và lắng nghe.

## Checklist mỗi shot
- [ ] Mở đầu/giữa/đỉnh hành động/recovery/kết đều được kiểm tra.
- [ ] Không crop ngoài ý muốn; tỷ lệ nhân vật giữ nhất quán.
- [ ] Có hành động thấy được trong silhouette.
- [ ] Contact tay/chân/đạo cụ hợp lý, prop phản ứng đúng.
- [ ] Camera có mục đích; không lặp cùng framing quá nhiều shot.
- [ ] Ánh sáng có nguồn; glow tiết chế; set phân biệt rõ.
- [ ] Chữ đúng nguyên văn, đủ thời gian đọc và nằm trong safe area.
- [ ] SFX/nhạc ăn khớp sự kiện; khoảng lặng giữ đúng.
- [ ] Contact sheet bao phủ đủ shot; clip chuyển động đã được xem.
- [ ] ffprobe và phép đo loudness/true peak đã ghi vào QA.

## Mức tuyên bố
- Source changed không đồng nghĩa rendered.
- Typecheck passed không đồng nghĩa video đúng.
- Render completed không đồng nghĩa visual QA passed.
- Contact sheet generated không đồng nghĩa motion verified.
- Artifact staged locally không đồng nghĩa archived on GitHub.
- Chỉ đánh dấu visual QA passed khi đã xem sheet + moving proofs và xử lý mọi P0/P1.
