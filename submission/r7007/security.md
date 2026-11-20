# Bảo mật khi làm việc

## 1. Ca USB: hết giờ, muốn chép lô về nhà làm tiếp
- Khi hết giờ làm việc mà chưa hoàn thành công việc, nhân viên tuyệt đối không được tự ý chép dữ liệu ra USB, gửi qua email cá nhân hoặc nhờ người ngoài làm hộ. Dữ liệu gán nhãn có thể chứa hình ảnh nội bộ, thông tin nhận dạng cá nhân hoặc tài sản sở hữu trí tuệ chưa công bố; việc đưa dữ liệu ra ngoài thiết bị công ty quản lý vi phạm nghiêm trọng chính sách an toàn thông tin và thỏa thuận bảo mật dữ liệu (NDA).
- Việc nhờ người khác làm hộ cũng vi phạm nguyên tắc kiểm soát truy cập định danh (IAM) và làm sai lệch nguồn gốc kiểm toán chất lượng (audit trail).
- Biện pháp xử lý đúng: Báo cáo trưởng nhóm xin gia hạn deadline hoặc sử dụng hạ tầng làm việc từ xa an toàn (VPN/VDI có xác thực đa yếu tố MFA) được công ty phê duyệt chính thức.

## 2. Năm việc: được hay không
1. Mở job được giao trên máy công ty: ĐƯỢC. Đây là tác vụ đúng thẩm quyền, đúng môi trường kiểm soát và phục vụ công việc được phân công.
2. Chụp màn hình gửi người quen: KHÔNG ĐƯỢC. Hành vi phát tán hình ảnh dữ liệu ra bên ngoài làm rò rỉ dữ liệu nhạy cảm, vi phạm điều khoản bảo mật của dự án.
3. Chép lô ra USB: KHÔNG ĐƯỢC. Sao chép dữ liệu sang thiết bị lưu trữ cá nhân không mã hóa tiềm ẩn rủi ro thất thoát dữ liệu và lây nhiễm mã độc.
4. Dán nhãn thật lên chatbot công cộng: KHÔNG ĐƯỢC. Các chatbot công cộng có thể lưu trữ và sử dụng dữ liệu nhập vào để tái huấn luyện, làm lộ dữ liệu nội bộ ra bên ngoài.
5. Đưa tài khoản CVAT cho đồng nghiệp: KHÔNG ĐƯỢC. Vi phạm nguyên tắc định danh tài khoản cá nhân, làm sai lệch log kiểm toán (audit log) về người thực sự thao tác và gán nhãn.

## 3. Ca khuôn mặt: thấy mặt người rõ trong lô, guideline yêu cầu làm mờ
- Hành động xử lý: Tạm dừng phát hành lô dữ liệu, chuyển trạng thái lô sang Hold và báo cáo ngay lập tức cho người phụ trách/quản lý dự án để chuyển giao bộ phận tiền xử lý dữ liệu làm mờ.
- Lý do không tự ý làm mờ hay xóa ảnh: Việc tự ý can thiệp chỉnh sửa pixel hoặc xóa ảnh trực tiếp sẽ làm thay đổi mã hash SHA-256 của file ảnh, gây sai lệch toàn bộ manifest.json, phá vỡ tính toàn vẹn và mất dấu vết kiểm toán dữ liệu.
- Minh chứng ảnh thực tế trong lô seed 7007: Ảnh 000000001296 (và các ảnh 000000004395, 000000020992) có khuôn mặt người cận cảnh nhìn rất rõ, cần được chuyển cho đội chuyên trách làm mờ trước khi đưa vào tập huấn luyện chính thức.
