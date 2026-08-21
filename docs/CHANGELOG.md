# Changelog

Tất cả những thay đổi, sửa lỗi và cập nhật tính năng đáng kể của dự án được ghi nhận tại đây.

| Thời gian | Lỗi / Thay đổi | Nguyên nhân gốc | Giải pháp thực hiện |
|---|---|---|---|
| 2026-08-21 | Khởi tạo cấu trúc docs theo quy chuẩn AI Repo Rules | Cần tài liệu chuẩn kiến trúc & quy trình | Tạo đầy đủ `docs/ARCHITECTURE.md`, `docs/SETUP.md`, `docs/API.md`, `docs/CHANGELOG.md`, `docs/JOURNAL.md` |
| 2026-08-21 | Hoàn thiện code lõi `train.py`, `serve.py`, `test_train.py` | Yêu cầu nghiệp vụ phân loại thu nhập & CI/CD | Xây dựng pipeline Scikit-learn + MLflow tracking + FastAPI inference server + 3 unit tests pytest |
| 2026-08-21 | Tích hợp các tính năng Bonus 1-5 | Tối ưu hóa mô hình và tự động hóa hệ thống MLOps | Cài đặt threshold search (Bonus 2), confusion matrix/detail report (Bonus 3), drift detection (Bonus 5) |
| 2026-08-21 | Sửa lỗi unpickling Cython loss khi release lên VM | Lệch phiên bản `scikit-learn` giữa CI runner và VM (1.4.2 vs 1.7.2) | Đồng bộ chặt chẽ dependencies trên VM qua `requirements.txt` (`scikit-learn==1.4.2`) |
| 2026-08-21 | Triển khai thành công Bước 2 & Bước 3 CI/CD | Tự động hóa huấn luyện, đánh giá và release lên Cloud VM | Cấu hình 5 GitHub Secrets, DVC data tracking trên GCS, hoàn thiện 5/5 ảnh chụp và báo cáo nộp bài |
