# Dùng AI

| # | Ai dùng | Công cụ | Prompt (tóm tắt) | AI sai ở đâu | Nhóm kiểm lại thế nào |
|---|---|---|---|---|---|
| 1 | Minh | Gemini (Antigravity) | Viết module kiểm tra lỗi luật YOLO và Panoptic (duplicate_box, invalid_class, thing_overlap, invalid_category_id) | AI ban đầu định bắt duplicate_box bằng IoU, nhóm nhận thấy COCO tự nhiên có IoU cao nên sửa lại kiểm tra kích thước giống nhau và lệch tâm 1-2 pixel | Thử nghiệm trên lô sạch (`runs/clean`), kết quả ra 0 lỗi ảo (FP = 0), F1 luật trên seed 7007 đạt 1.0 |
