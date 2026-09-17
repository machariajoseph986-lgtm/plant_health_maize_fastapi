from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

FEATURE_ROOT = Path("training_output/maize_gate_features")
OUTPUT_PATH = Path("training_output/maize_gate_logistic_regression.joblib")


def load_split(name):
    data = np.load(FEATURE_ROOT / f"{name}.npz")
    return data["features"], data["labels"]


def main():
    X_train, y_train = load_split("train")
    X_val, y_val = load_split("val")

    print(f"Train: X={X_train.shape}, y={y_train.shape}")
    print(f"Validation: X={X_val.shape}, y={y_val.shape}")
    print(f"Train class counts: {dict(zip(*np.unique(y_train, return_counts=True)))}")
    print(f"Validation class counts: {dict(zip(*np.unique(y_val, return_counts=True)))}")

    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    val_pred = model.predict(X_val)
    val_prob = model.predict_proba(X_val)[:, 1]

    print(f"Validation accuracy: {accuracy_score(y_val, val_pred):.4f}")
    print("Validation confusion matrix [rows=true, cols=predicted]:")
    print(confusion_matrix(y_val, val_pred))
    print("Validation classification report:")
    print(classification_report(y_val, val_pred, target_names=["not_maize", "maize"], digits=4))
    print(f"Validation maize probability range: {val_prob.min():.4f} - {val_prob.max():.4f}")

    import joblib
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
