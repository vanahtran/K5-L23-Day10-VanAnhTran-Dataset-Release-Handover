# Phân công Review Đề ẩn — Nhóm 07

Mỗi bạn mở ảnh tương ứng trong thư mục `delivery/images/<tên_ảnh>.jpg` để xem, xác định `confirmed` (lỗi thật) hoặc `rejected` (nhiễu tự nhiên / che khuất), ghi nhận xét $\ge 20$ ký tự rồi gửi cho Văn gộp vào `submission/de_an/review_log.csv`.

---

### 1. Trần Anh Văn (Văn) — 9 ứng viên
- **img_0002** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=truck vs Panoptic=car (IoU=0.90)
- **img_0005** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask chair phủ 2 box YOLO
- **img_0008** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=microwave vs Panoptic=oven (IoU=0.79)
- **img_0010** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=bird vs Panoptic=kite (IoU=0.97)
- **img_0012** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask chair phủ 2 box YOLO
- **img_0024** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0027** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0039** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=orange vs Panoptic=apple (IoU=0.89)
- **img_0045** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask book phủ 2 box YOLO

---

### 2. Đinh Hữu Minh (Minh) — 9 ứng viên
- **img_0048** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask dog phủ 2 box YOLO
- **img_0060** | Nghi ngờ: `missing_box` | Gợi ý: Panoptic có hot dog (area=19913) nhưng YOLO thiếu box
- **img_0065** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0076** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask carrot phủ 2 box YOLO
- **img_0078** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=bed vs Panoptic=couch (IoU=0.85)
- **img_0090** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=cow vs Panoptic=elephant (IoU=0.89)
- **img_0100** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=cat vs Panoptic=suitcase (IoU=0.44)
- **img_0110** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask boat phủ 2 box YOLO
- **img_0121** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=dog vs Panoptic=cat (IoU=1.00)

---

### 3. Tạ Xuân Anh Vũ (Vũ) — 9 ứng viên
- **img_0134** | Nghi ngờ: `bbox_drift` | Gợi ý: Box lệch: cow IoU=0.24
- **img_0137** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0140** | Nghi ngờ: `missing_box` | Gợi ý: Panoptic có person (area=6836) nhưng YOLO thiếu box
- **img_0143** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0145** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0147** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=motorcycle vs Panoptic=bicycle (IoU=0.97)
- **img_0152** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask knife phủ 2 box YOLO
- **img_0155** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask scissors phủ 2 box YOLO
- **img_0168** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask train phủ 2 box YOLO

---

### 4. Ngọ Đức Trinh (Trinh) — 8 ứng viên
- **img_0172** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=hot dog vs Panoptic=sandwich (IoU=0.43)
- **img_0175** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=spoon vs Panoptic=fork (IoU=0.89)
- **img_0179** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask cow phủ 2 box YOLO
- **img_0180** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=truck vs Panoptic=car (IoU=0.95)
- **img_0195** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask car phủ 2 box YOLO
- **img_0197** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask umbrella phủ 2 box YOLO
- **img_0203** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask teddy bear phủ 2 box YOLO
- **img_0222** | Nghi ngờ: `missing_box` | Gợi ý: Panoptic có baseball bat (area=5279) nhưng YOLO thiếu box

---

### 5. Giang Nguyễn Xuân Bách (Bách) — 8 ứng viên
- **img_0222** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask baseball bat phủ 2 box YOLO
- **img_0227** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=book vs Panoptic=chair (IoU=0.98)
- **img_0227** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask book phủ 2 box YOLO
- **img_0235** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask person phủ 2 box YOLO
- **img_0240** | Nghi ngờ: `class_swap` | Gợi ý: YOLO=chair vs Panoptic=couch (IoU=0.98)
- **img_0245** | Nghi ngờ: `bbox_drift` | Gợi ý: Box lệch: cow IoU=0.23
- **img_0245** | Nghi ngờ: `instance_merge` | Gợi ý: 1 mask cow phủ 2 box YOLO
- **img_0248** | Nghi ngờ: `bbox_drift` | Gợi ý: Box lệch: bench IoU=0.39
