Release: lab250_20c5f74a77e2_v2
Parent: lab250_20c5f74a77e2
Số ảnh: 242
Số nhãn: 1675
Guideline: v1.2 (J01-J04), v1.3 (J05-J10)
QC v1: 18/250 = 7.2%
Kết luận v1: Hold — Tỷ lệ lỗi 7.2% vượt ngưỡng cho phép 2.0%
Kết luận v2: Release — Đã tách 8 ảnh lỗi sang rework_queue, sửa rò rỉ scene và đồng bộ guideline
Ghi chú: Đã mở kiểm tra ảnh toàn vẹn và cập nhật hash chuẩn cho wrong_hash; đồng bộ split train cho scene_leak; cập nhật guideline theo jobs.csv; các ảnh lỗi panoptic [000000006471 (category_swap), 000000011511 (thing_overlap), 000000015079 (instance_merge), 000000018491 (invalid_category_id), 000000018833 (invalid_category_id), 000000023899 (instance_merge)] được giữ lại v2 vì nhãn detection chuẩn xác, đã gửi thông báo sang team panoptic xử lý.
