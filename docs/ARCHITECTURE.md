# System Architecture & Data Flow

## 1. Tổng quan hệ thống
Hệ thống triển khai pipeline MLOps hoàn chỉnh từ thử nghiệm cục bộ đến phục vụ suy luận liên tục trên môi trường đám mây cho bài toán phân loại nhị phân thu nhập (Adult Dataset).

```
[Local Machine]
   ├── MLflow Local Tracking (sqlite:///mlflow.db)
   └── DVC (Data Version Control)
         │
         │ git push (code + .dvc pointers) & dvc push (data)
         ▼
[GitHub Repository]
   └── GitHub Actions CI/CD Pipeline
         ├── Job 1: Unit Test (pytest tests/ -v)
         ├── Job 2: Train (dvc pull -> train.py -> upload model to GCS)
         ├── Job 3: Quality Gate (F1 >= 0.65 check & Rollback Gate)
         └── Job 4: Release (SSH -> Restart systemd service & health check)
               │
               │ Deploy model.joblib
               ▼
[Cloud Storage (GCS)] ────────► [Cloud VM (Ubuntu 22.04)]
   ├── dvc/ (Raw CSV batches)        FastAPI Server (income-api.service)
   └── artifacts/current/             ├── GET /healthz
         ├── model.joblib             └── POST /score
         └── report.json
```

## 2. Các Module Chính
- `prepare_data.py`: Tải dữ liệu từ UCI repository, làm sạch, mã hóa categorical features và chia thành `train_batch1.csv`, `holdout.csv`, `train_batch2.csv`.
- `append_batch.py`: Ghép dữ liệu mới `train_batch2.csv` vào `train_batch1.csv` để mô phỏng Continuous Training.
- `src/train.py`: Huấn luyện GradientBoostingClassifier, log MLflow, tính F1 lớp dương, tối ưu Decision Threshold (Bonus 2), xuất báo cáo chi tiết Precision/Recall (Bonus 3), kiểm tra Data Drift (Bonus 5), lưu `outputs/report.json` và `models/model.joblib`.
- `src/serve.py`: FastAPI application chạy trên Cloud VM, tự động download `model.joblib` khi khởi động, phục vụ 2 endpoints `/healthz` và `/score`.
- `tests/test_train.py`: Unit tests chạy trên in-memory dummy dataset để kiểm tra tính toàn vẹn của logic huấn luyện.
- `.github/workflows/cicd.yml`: Pipeline tự động hóa 4 giai đoạn hoàn chỉnh.
