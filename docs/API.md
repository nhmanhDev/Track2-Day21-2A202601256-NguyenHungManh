# API Documentation

Tài liệu chi tiết các endpoint của Inference Server (`src/serve.py`).

## 1. Health Check Endpoint
Kiểm tra trạng thái sẵn sàng của dịch vụ.

- **URL**: `/healthz`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

---

## 2. Prediction / Scoring Endpoint
Dự đoán mức thu nhập dựa trên 10 đặc trưng nhân khẩu học.

- **URL**: `/score`
- **Method**: `POST`
- **Header**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "features": [
      60,  // age (17-90)
      2,   // workclass (0-6)
      5,   // education_num (1-16)
      2,   // marital_status (0-6)
      4,   // occupation (0-13)
      0,   // relationship (0-5)
      1,   // sex (0: Female, 1: Male)
      0,   // capital_gain
      0,   // capital_loss
      45   // hours_per_week (1-99)
    ]
  }
  ```
- **Response thành công (200 OK)**:
  ```json
  {
    "prediction": 0,
    "label": "thu_nhap_thap"
  }
  ```
- **Response lỗi đầu vào (400 Bad Request)**:
  ```json
  {
    "detail": "Expected 10 features (adult income)"
  }
  ```
