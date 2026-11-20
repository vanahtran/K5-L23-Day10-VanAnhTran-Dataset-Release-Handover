# Báo cáo nhóm 07

## 1. Số liệu luyện tập
- F1 theo seed (rule / cross_check / overall): seed 7007: 1.0 / 1.0 / 1.0 (lỗi luật 12/12, lỗi gán nhãn sau review đạt độ chính xác tối ưu).
- Số ứng viên trên lô sạch (`--no-faults`): 6 ứng viên / 50 ảnh (~12% độ lệch tự nhiên của COCO); hàng đợi trên seed luyện tập: 37 ứng viên / 250 ảnh.
- Ngưỡng đã chọn và cách chọn (không dùng `_private`):
  + Đối với `class_swap` / `category_swap`: Yêu cầu IoU bbox giữa YOLO và Panoptic >= 0.70 và tên lớp khác nhau (đối chiếu tên chuẩn hóa qua `classes.txt` và Panoptic categories).
  + Đối với `bbox_drift`: Đo tỷ lệ pixel của thing segment rơi vào bên trong box YOLO; gắn cờ khi tỷ lệ này < 0.70 hoặc IoU < 0.30 với segment cùng lớp lớn nhất.
  + Đối với `missing_box`: Panoptic có thing segment diện tích lớn (> 3000 pixel) nhưng không có box YOLO nào có IoU > 0.10.
  + Đối với `instance_merge`: Một thing segment bao phủ đồng thời >= 2 box YOLO cùng lớp với IoU mỗi box > 0.20.
  + Thử nghiệm trên lô sạch (`runs/clean`) chỉ sinh 6 ứng viên, chứng minh bộ lọc đã loại bỏ hầu hết nhiễu che khuất tự nhiên mà không làm quá tải hàng đợi review (37 ảnh chia 5 người = 7–8 ảnh/người, xem trong khoảng 15 phút).

## 2. Vì sao báo hết ứng viên làm F1 giảm?
- **Minh chứng bằng số liệu thực nghiệm của nhóm trên seed 7007:**
  + Thuật toán đối chiếu tự động sinh ra hàng đợi gồm 37 ứng viên khả nghi.
  + Tuy nhiên, qua review mắt thật của cả nhóm, trong 37 ứng viên này chỉ có 7 lỗi gán nhãn thực sự (True Positives = 7). 30 ứng viên còn lại là do độ lệch tự nhiên của bộ dữ liệu COCO (ví dụ: chén trà kiểu Nhật không quai lẫn giữa `cup`/`bowl`, bánh burger kẹp vừng lẫn giữa `sandwich`/`hot dog`, người lớn bế em bé...) hoặc do lỗi từ phía mask Panoptic.
  + Nếu báo thẳng toàn bộ 37 ứng viên vào `errors.json` mà không qua bước review bằng mắt người:
    * TP = 7, FP = 30.
    * Precision của lỗi gán nhãn sẽ tụt dốc nghiêm trọng: $Precision = \frac{7}{7 + 30} \approx 18.9\%$.
    * Điểm F1 lỗi gán nhãn sẽ giảm từ 1.0 xuống chỉ còn $F_1 \approx 0.318$.
  + **Kết luận:** Bước review bằng mắt người ở Pha 2 là khâu chốt chặn bắt buộc để loại bỏ 30 cảnh báo sai (False Positives), đưa Precision và F1 trở lại mức tối đa.

## 3. Quyết định và lineage
<<QC v1 a/b, kết luận, vì sao R-021 phải xem lại hoặc train lại.>>

## 4. Hash chứng minh gì, không chứng minh gì?
<<>>

## 5. Truy vết
<<Tiêu chí tầng a/b, vì sao lấy guideline theo job.>>

## 6. Bug hoặc điểm chưa rõ trong lab (nếu có)
<<>>
