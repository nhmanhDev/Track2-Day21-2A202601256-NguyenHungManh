# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | ___ |
| MSSV | ___ |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/___/___ |
| Ngày nộp | ___ |

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

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
