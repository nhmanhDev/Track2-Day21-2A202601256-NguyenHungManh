import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import yaml
import json
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix

# Nguong chat luong cua lab nay la f1_score, KHONG phai accuracy.
# Ly do: bo du lieu Adult co ty le lop 75/25. Mot mo hinh doan bua
# "thu nhap thap" cho moi mau da dat accuracy 0.75 ma khong hoc duoc gi.
F1_THRESHOLD = 0.65
BASELINE_POSITIVE_RATIO = 0.248  # Ty le lop duong tham chieu 24.8%

if "MLFLOW_TRACKING_URI" not in os.environ:
    mlflow.set_tracking_uri("sqlite:///mlflow.db")


def train(
    params: dict,
    data_path: str = "data/train_batch1.csv",
    eval_path: str = "data/holdout.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho GradientBoostingClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia (holdout).

    Tra ve:
        f1 (float): diem F1 cua lop duong (thu nhap > 50K) tren tap holdout tai nguong 0.5.
    """

    # 1. Doc du lieu huan luyen va danh gia
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    # 2. Tach dac trung (X) va nhan (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    # Bonus 5: Kiem tra Lech lac du lieu (Data Drift Detection)
    positive_ratio = float(y_train.mean())
    drift_diff = abs(positive_ratio - BASELINE_POSITIVE_RATIO)
    drift_detected = drift_diff > 0.05
    if drift_detected:
        print(f"[CANH BAO DRIFT] Ty le lop duong trong tap train: {positive_ratio:.1%}, "
              f"lech {drift_diff:.1%} so voi tham chieu {BASELINE_POSITIVE_RATIO:.1%} (> 5%)!")
    else:
        print(f"[DRIFT CHECK] Ty le lop duong trong tap train: {positive_ratio:.1%} (chuan tham chieu {BASELINE_POSITIVE_RATIO:.1%}).")

    with mlflow.start_run():

        # 3. Ghi nhan cac sieu tham so
        mlflow.log_params(params)

        # 4. Khoi tao va huan luyen GradientBoostingClassifier
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        # 5. Du doan tren tap holdout va tinh chi so tai nguong mac dinh 0.5
        preds = model.predict(X_eval)
        f1 = float(f1_score(y_eval, preds))  # Lop duong mac dinh
        acc = float(accuracy_score(y_eval, preds))

        # Bonus 2: Dieu chinh nguong quyet dinh (Decision Threshold Tuning)
        probs_eval = model.predict_proba(X_eval)[:, 1]
        best_threshold = 0.5
        best_f1 = f1
        threshold_records = {}
        for th in np.arange(0.1, 0.95, 0.05):
            th_round = round(float(th), 2)
            th_preds = (probs_eval >= th_round).astype(int)
            th_f1 = float(f1_score(y_eval, th_preds, zero_division=0))
            threshold_records[th_round] = th_f1
            if th_f1 > best_f1:
                best_f1 = th_f1
                best_threshold = th_round

        # Bonus 3: Bao cao Precision / Recall va Confusion Matrix
        cm = confusion_matrix(y_eval, preds)
        prec_0 = float(precision_score(y_eval, preds, pos_label=0, zero_division=0))
        rec_0 = float(recall_score(y_eval, preds, pos_label=0, zero_division=0))
        prec_1 = float(precision_score(y_eval, preds, pos_label=1, zero_division=0))
        rec_1 = float(recall_score(y_eval, preds, pos_label=1, zero_division=0))

        # 6. Ghi nhan chi so vao MLflow
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("optimal_f1_score", best_f1)
        mlflow.log_metric("optimal_threshold", best_threshold)
        mlflow.log_metric("positive_class_ratio", positive_ratio)
        mlflow.log_metric("precision_class_0", prec_0)
        mlflow.log_metric("recall_class_0", rec_0)
        mlflow.log_metric("precision_class_1", prec_1)
        mlflow.log_metric("recall_class_1", rec_1)
        mlflow.sklearn.log_model(model, "model")

        # 7. In ket qua ra man hinh
        print(f"F1 (nguong 0.5): {f1:.4f} | Accuracy: {acc:.4f} | Optimal F1 (nguong {best_threshold}): {best_f1:.4f}")

        # 8. Luu metrics ra file outputs/report.json (cho CI/CD va Quality Gate)
        os.makedirs("outputs", exist_ok=True)
        report_data = {
            "f1_score": f1,
            "accuracy": acc,
            "optimal_f1_score": best_f1,
            "optimal_threshold": best_threshold,
            "positive_class_ratio": positive_ratio,
            "drift_detected": drift_detected,
        }
        with open("outputs/report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        # Bonus 3: Luu outputs/detail.txt
        detail_content = (
            "===========================================================\n"
            "CHI TIET DANH GIA MO HINH (EVALUATION DETAIL REPORT)\n"
            "===========================================================\n\n"
            f"F1 Score (Default th=0.5): {f1:.4f}\n"
            f"Accuracy:                  {acc:.4f}\n"
            f"Optimal Threshold:         {best_threshold:.2f} (F1 = {best_f1:.4f})\n"
            f"Positive Class Ratio:      {positive_ratio:.2%}\n\n"
            "--- CONFUSION MATRIX ---\n"
            f"                  Predicted <=50K    Predicted >50K\n"
            f"Actual <=50K:         {cm[0][0]:<15} {cm[0][1]:<15}\n"
            f"Actual >50K:          {cm[1][0]:<15} {cm[1][1]:<15}\n\n"
            "--- METRICS PER CLASS ---\n"
            f"Class 0 (<=50K): Precision = {prec_0:.4f}, Recall = {rec_0:.4f}\n"
            f"Class 1 (>50K) : Precision = {prec_1:.4f}, Recall = {rec_1:.4f}\n\n"
            "--- PHAN TICH CHI PHI SAI LAM ---\n"
            "- Bo sot nguoi thu nhap cao (False Negative, Recall thap): Doanh nghiep bo lo khach hang tiem nang.\n"
            "- Gan nham nguoi thu nhap thap (False Positive, Precision thap): Ton chi phi marketing vao doi tuong khong phu hop.\n"
            "===========================================================\n"
        )
        with open("outputs/detail.txt", "w", encoding="utf-8") as f:
            f.write(detail_content)

        # 9. Luu mo hinh ra file models/model.joblib
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")

    # 10. Tra ve f1
    return f1


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
