
# State restoration cho phiên AI mới

## Nguồn chính
- Private plugin: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 (v1.0.2 làm nền cho bản overlay v1.1.0).
- Source mirror: integrations/h2-selfimprove-studio/.
- Cross-engine production skill: https://github.com/Nolane-x/video/blob/main/.agents/skills/video-production-master/SKILL.md
- Project state: https://github.com/Nolane-x/video/blob/main/docs/STATE.md
- Handoff: https://github.com/Nolane-x/video/blob/main/docs/AI_HANDOFF.md
- Tool inventory: https://github.com/Nolane-x/video/blob/main/docs/TOOL_INVENTORY.md
- Film manifest: video-library/one-more-scroll/manifest.json.

## Luôn xác minh lại
Kiểm tra HEAD và workflow mới nhất; không tin snapshot cũ mà không đối chiếu source. Xác minh tệp là ChatGPT attachment, file trong Git, GitHub Release asset hay artifact có thời hạn. Kiểm tra checksum/metadata thực tế trước khi gọi artifact là archived.

## Handoff tối thiểu
- Source commit và engine cụ thể.
- CI/workflow run URL + kết quả.
- Master/preview paths, SHA-256, duration/resolution/FPS/codecs.
- Audio LUFS/true peak đã đo.
- Contact sheets và clip motion proof đã xem hay chưa.
- P0/P1/P2 còn lại, phần source-only chưa render.
- Next action chính xác.

Không bao giờ biến “đã tạo ZIP” thành “đã tạo plugin mới” nếu Plugin Creator chưa trả release ID mới.
