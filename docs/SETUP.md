# Hướng Dẫn Cài Đặt & Thiết Lập (Setup Guide)

## 1. Yêu cầu hệ thống
- Python 3.10 trở lên
- Git
- Tài khoản Cloud (GCP / AWS / Azure)

## 2. Cài đặt môi trường cục bộ
```bash
# 1. Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# hoặc .venv\Scripts\activate trên Windows

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chuẩn bị dữ liệu
python prepare_data.py
```

## 3. Cấu hình Cloud & GitHub Secrets
Cần cấu hình 5 secrets trên GitHub Actions:
- `STORAGE_CREDENTIALS`: Nội dung file Service Account JSON (`sa-key.json`).
- `ARTIFACT_BUCKET`: Tên Cloud Storage bucket.
- `SERVER_HOST`: Public IP của Cloud VM.
- `SERVER_USER`: Username SSH trên Cloud VM.
- `SERVER_SSH_KEY`: Nội dung private key SSH.
