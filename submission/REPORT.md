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
- **Đánh giá chất lượng lô v1:**
  + Tổng số ảnh của lô: 250 ảnh.
  + Số lỗi phát hiện qua QC v1: 19 lỗi / 250 ảnh (chiếm tỷ lệ 7.6%).
  + Theo quy tắc ngưỡng Day 7 (nếu tỷ lệ ảnh lỗi > 2.0% thì không Release), lô v1 vượt ngưỡng an toàn nghiêm trọng (7.6% > 2.0%).
  + **Kết luận v1:** Quyết định **HOLD** lô v1, không đưa vào triển khai hoặc huấn luyện sản xuất.
- **Tác động tới training run R-021 (Blast radius):**
  + Khi truy vấn tác động qua `scripts/lineage.py impact --release-id lab250_42b020af0ffa`: kết quả hiển thị `R-021: affected=True action=review_or_retrain`.
  + **Vì sao R-021 phải xem lại hoặc train lại?** Mô hình R-021 đã được huấn luyện trực tiếp trên các nhãn và ảnh bị lỗi của lô v1 (bao gồm cả box bị gán nhầm lớp `class_swap`, box bị lệch `bbox_drift`, nhãn sai chuẩn `guideline_mismatch`). Trọng số (weights) của mô hình đã học theo các mẫu dữ liệu sai lệch này. Việc sửa dataset và phát hành lô v2 sạch chỉ khắc phục dữ liệu tĩnh trong kho, không thể tự động đảo ngược hay chữa lành các tham số mô hình đã học. Do đó, run R-021 bắt buộc phải được đánh giá lại độ chính xác hoặc tiến hành huấn luyện lại (retrain) hoàn toàn trên lô dữ liệu v2.

## 4. Hash chứng minh gì, không chứng minh gì?
- **Hash chứng minh điều gì?**
  + **Tính toàn vẹn của dữ liệu (Data Integrity):** Chứng minh file ảnh và file nhãn trên đĩa hoàn toàn nguyên vẹn, không bị hỏng hóc trong quá trình truyền tải, lưu trữ hoặc sao chép.
  + **Tính chống giả mạo / truy nguyên (Tamper Evidence):** Xác nhận nội dung bit/byte chính xác tại thời điểm bàn giao, không bị chỉnh sửa lén lút hay ghi đè ngoài ý muốn so với bản đã kiểm kê trong `manifest.csv`.
- **Hash KHÔNG chứng minh điều gì?**
  + Hash không chứng minh được **tính đúng đắn về mặt ngữ nghĩa của nhãn (Label Correctness)**. Một file nhãn gán sai lớp (ví dụ xe tải gán nhầm thành ô tô con) hoặc box vẽ lệch tâm vẫn có thể có mã băm SHA-256 hoàn toàn hợp lệ.
  + Hash không chứng minh được **tính phù hợp của dữ liệu (Data Usability & Quality)** đối với bài toán học máy. Dữ liệu rác hoặc ảnh nhiễu nếu được băm đúng chuẩn vẫn vượt qua kiểm tra hash. Do đó, kiểm tra hash chỉ là điều kiện cần về mặt quản trị kỹ thuật, không thay thế được quy trình kiểm thử chất lượng dữ liệu (Data Quality Assurance).

## 5. Truy vết
- **Tiêu chí phân tầng:**
  + `tier_a`: Các ảnh nằm trong các cảnh (scenes) cụ thể mà team AI đã nêu rõ trong ticket báo lỗi, đồng thời thuộc các job được gán nhãn theo phiên bản guideline cũ (v1.2), và trong nhãn detection YOLO có chứa ít nhất một box thuộc lớp bị thay đổi quy tắc (`rule_class`).
  + `tier_b`: Toàn bộ các ảnh khác trong lô bàn giao cũng thuộc các job gán theo guideline cũ v1.2 và chứa ít nhất một box thuộc `rule_class`, nhưng nằm ở các cảnh khác mà team AI chưa phát hiện hoặc chưa báo cáo.
  + `notify`: Danh sách gồm toàn bộ người gán nhãn (`annotator`) và người kiểm định (`reviewer`) phụ trách các job chứa ảnh thuộc tầng a và tầng b, nhằm yêu cầu đào tạo lại hoặc rà soát lại công việc.
- **Vì sao lấy guideline theo job (`jobs.csv`) chứ không lấy theo metadata của ảnh?**
  + Trong lô dữ liệu tồn tại lỗi `guideline_mismatch`, tức là trường `guideline_version` được ghi tại metadata của từng ảnh có thể đã bị ghi sai hoặc lệch so với thực tế ban hành của job đó.
  + Phiên bản guideline thực tế mà annotator và reviewer tuân thủ khi thực hiện công việc được quy định tập trung ở cấp độ hợp đồng công việc (job level trong `jobs.csv`). Do đó, lấy guideline theo job đảm bảo căn cứ pháp lý và nghiệp vụ chính xác nhất để khoanh vùng các ảnh có nguy cơ bị gán nhãn sai quy chuẩn.

## 6. Bug hoặc điểm chưa rõ trong lab (nếu có)
- Nhóm ghi nhận định dạng COCO panoptic và YOLO detection có sự bất đồng tự nhiên ở các vật thể bị che khuất một phần (occlusion) hoặc vật thể dạng đám đông (crowd). Thuật toán đối chiếu tự động cần kết hợp thêm tỷ lệ diện tích mask và pixel containment thay vì chỉ dựa vào IoU của bounding box để giảm thiểu số lượng ứng viên rác.
