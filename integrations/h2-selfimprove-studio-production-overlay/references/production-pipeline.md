
# Quy trình sản xuất có cổng kiểm định

## Gate 0 — Khôi phục đúng trạng thái
Đọc skill H2, scene/QA references, project config/story JSON; sau đó đọc trạng thái repo Nolane nếu repo được kết nối. Kiểm tra HEAD, workflow và artifact thật. Tách rõ source đã sửa, build đã qua, video đã render và video đã được duyệt hình ảnh.

## Gate 1 — Brief
Ghi nền tảng, tỷ lệ, thời lượng, ngôn ngữ, thuyết minh hay không, khán giả, cảm xúc đích, quyền sử dụng asset và giới hạn nội dung. Không hỏi lại thông tin đã có.

## Gate 2 — Phân tích tham khảo
Phân tích các đoạn xuyên suốt video, không chỉ thumbnail. Ghi shot-size, góc máy, chuyển động camera, nhân vật/hành động, bối cảnh, ánh sáng, màu, đạo cụ/điểm tiếp xúc, chữ, chuyển cảnh và sound cue. Học ngữ pháp hình ảnh chứ không chép khung hình/lời thoại/nhạc.

## Gate 3 — Storyboard theo schema H2
Mỗi shot có thời gian vào/ra, template được engine hỗ trợ, setting/pose, hành động, cảm xúc, đạo cụ, contact target, framing/camera, caption, sound cue và transition. Dùng schema thật từ source. Tính tổng thời lượng và kiểm tra frame-boundaries trước render.

## Gate 4 — Art direction
Khóa character bible, tỷ lệ đầu/thân, nét viền, màu áo, bố trí mặt, bảng màu bối cảnh, logic ánh sáng và typography. Nhân vật đơn giản nhưng môi trường phải có chiều sâu, chi tiết có lý do và mặt đất nhất quán.

## Gate 5 — Blocking
Dựng layout thô trước khi trang trí. Khóa chân trời, điểm neo tay/chân, scale nhân vật, layer order, mặt phẳng đạo cụ và vùng an toàn camera. Render sheet thô để bắt lỗi trước khi animate.

## Gate 6 — Animation
Mỗi hành động có anticipation → action → contact/impact → follow-through → recovery. Chuyển động camera không thay thế chuyển động nhân vật. Đạo cụ phải di chuyển/phản ứng đúng khi có tương tác; chân phải chạm sàn/bậc.

## Gate 7 — Preview
Render một khung cho từng shot và một overview; tạo clip 5–10 giây có hành động khó. Trích khung trước/trúng/sau tiếp xúc. Xem ở kích thước xuất, không chỉ phóng to hình đẹp nhất.

## Gate 8 — Audio
Sinh nhạc/SFX bằng code có trong kit, kiểm tra file output đã tồn tại và thời lượng khớp video. Cue đúng thời điểm; giữ khoảng lặng có chủ đích. Mặc định không có TTS trừ khi brief yêu cầu.

## Gate 9 — Full render và mastering
Ghi command, engine, commit, workflow run; render file tạm; FFmpeg mastering; ffprobe xác nhận video/audio streams, thời lượng, ratio, FPS, codec, sample rate và channels.

## Gate 10 — Archive/handoff
Lưu MP4, preview, storyboard, provenance, contact sheets, audio report, metadata, checksum, QA report, source commit và vấn đề còn tồn đọng. Cập nhật project manifest/state/handoff trước khi kết thúc.
