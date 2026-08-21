# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Hùng Mạnh |
| MSSV | 2A202601256 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/nhmanhDev/Track2-Day21-2A202601256-NguyenHungManh |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.10 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.10 | 5 | 0.7149 | 0.8740 |
| 4 | 150 | 0.10 | 3 | 0.7222 | 0.8800 |

**Bộ siêu tham số đã chọn:** `n_estimators=150`, `learning_rate=0.1`, `max_depth=3`.

**Lý do:** Lần chạy 4 đạt điểm F1 cao nhất trên tập holdout (0.7222) và vượt xa ngưỡng chất lượng (0.65). Bộ tham số này cân bằng tốt giữa số lượng cây (150) và tốc độ học (0.1) với độ sâu cây vừa phải (3), giúp mô hình nắm bắt được quan hệ phi tuyến mà không bị quá khớp (overfitting) như lần 3 (max_depth=5 tuy cây sâu và phức tạp hơn nhưng F1 lại thấp hơn 0.7149).

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Census Income bị mất cân bằng lớp nghiêm trọng khi lớp dương (thu nhập >50K) chỉ chiếm 24.8% tổng số mẫu. Trong điều kiện này, một mô hình tầm thường luôn dự đoán nhãn 0 ("thu nhập thấp") cho toàn bộ dữ liệu vẫn dễ dàng đạt Accuracy 75.2%, nhưng hoàn toàn vô dụng trong thực tế vì bỏ sót 100% người có thu nhập cao (Recall = 0, F1 = 0). Do đó, chỉ số Accuracy gây hiểu nhầm lớn và không phản ánh đúng năng lực nhận diện của mô hình. 

Chỉ số F1-score của lớp dương (tính từ Precision và Recall của lớp >50K) đo lường chính xác sự cân bằng giữa việc tìm đúng đối tượng thu nhập cao và không dự đoán nhầm lớp thu nhập thấp. Khi tính F1, tuyệt đối không dùng `average="weighted"` hay `average="macro"` vì trọng số của lớp đa số (75.2%) sẽ kéo điểm tổng thể lên cao giả tạo, làm mất đi ý nghĩa giám sát nghiêm ngặt của Quality Gate.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Mất cân bằng dữ liệu lớp dương (>50K chỉ chiếm 24.8%) | Accuracy cao ảo (75.2%) dù mô hình không nhận diện được lớp thiểu số | Thiết lập Quality Gate bắt buộc kiểm tra F1-score của lớp dương (ngưỡng tối thiểu >= 0.65) |
| Lệch phiên bản thư viện scikit-learn giữa CI runner và VM | Quá trình deserialize model.joblib bị lỗi thuộc tính Cython không tương thích | Đồng bộ phiên bản cố định bằng file `requirements.txt` trên cả môi trường CI và Cloud VM |
| Tự động hóa triển khai an toàn từ GitHub Actions lên Cloud VM | Cần phân quyền SSH và restart service an toàn không lộ thông tin nhạy cảm | Cấu hình SSH key chuyên dụng và quản lý thông tin kết nối qua 5 GitHub Repository Secrets |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`, 22.361 mẫu) | 0.7222 | 0.8800 |
| Bước 3 (thêm `train_batch2`, 44.722 mẫu) | 0.7306 | 0.8820 |

**Nhận xét:** Khi bổ sung thêm `train_batch2`, dung lượng tập huấn luyện tăng gấp đôi (từ 22.361 lên 44.722 mẫu) giúp F1-score tăng từ 0.7222 lên 0.7306 và Accuracy tăng nhẹ lên 0.8820 trên cùng tập holdout cố định. Việc có thêm nhiều mẫu đa dạng giúp mô hình học được ranh giới phân loại chính xác hơn và cải thiện khả năng tổng quát hóa trên dữ liệu thực tế.

---

## 5. Phần Bonus Đã Thực Hiện

- [x] Bonus 1 - Triển khai Serving trên Cloud VM: Triển khai FastAPI inference server trên Google Compute Engine VM với systemd daemon và SSH auto-deploy qua CI/CD.
- [x] Bonus 2 - Điều chỉnh ngưỡng quyết định: Thêm hàm quét ngưỡng xác suất trong `src/train.py`, tìm ra ngưỡng tối ưu 0.40 nâng F1-score lên 0.7438.
- [x] Bonus 3 - Báo cáo precision / recall tự động: Tạo ma trận nhầm lẫn và bảng phân tích chi tiết precision/recall lưu vào file `outputs/detail.txt` thành CI artifact.
- [x] Bonus 4 - Continuous Training tự động: Tích hợp DVC push/pull và workflow trigger tự động chạy lại toàn bộ quy trình khi dữ liệu mới được đẩy lên GitHub.
- [x] Bonus 5 - Cảnh báo lệch lạc dữ liệu: Thêm logic kiểm tra phân phối tỷ lệ lớp dương trong `src/train.py` để cảnh báo data drift trước khi huấn luyện.
