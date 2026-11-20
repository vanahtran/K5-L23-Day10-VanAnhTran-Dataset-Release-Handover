# Đánh giá Bảo mật & Quyền riêng tư — r7007

## 1. Dữ liệu khuôn mặt & PII (Face / Personal Data)
- Phát hiện ảnh chứa người rõ nét trong lô như 000000013177, 000000016228.
- Kết luận: Hold — Cần che mờ khuôn mặt (blur/redact) trước khi chia sẻ ra bên ngoài hoặc đưa vào môi trường công khai.

## 2. Kiểm soát truy cập & Phân quyền (Access Control)
- Chỉ cấp quyền đọc/ghi thư mục delivery và handover cho các thành viên được phân công trong jobs.csv, thu hồi quyền truy cập công khai.

## 3. Toàn vẹn dữ liệu & Mã kiểm tra (Integrity & SHA256)
- Toàn bộ tệp ảnh và nhãn trong lô v2 đã được tính mã băm SHA256 trong manifest.csv và đóng gói kèm tệp .sha256 để chống chỉnh sửa trái phép.
