import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42
IMAGE_SIZE = (320, 320)
BATCH_SIZE = 16
NUM_CLASSES = 6

DATASET_ROOT = Path("../v4_dataset")
TEST_DIR = DATASET_ROOT / "test"

MODEL_PATH = Path("training_output/v4/stage1_best.keras")
OUTPUT_DIR = Path("training_output/v4")

RESULTS_PATH = OUTPUT_DIR / "stage1_test_results.json"
REPORT_PATH = OUTPUT_DIR / "stage1_classification_report.txt"
CONFUSION_MATRIX_PATH = OUTPUT_DIR / "stage1_confusion_matrix.csv"

CLASS_NAMES = [
    "Northern_Leaf_Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy",
    "Maize_Lethal_Necrosis",
    "Maize_Streak_Virus",
]


# ============================================================
# REPRODUCIBILITY
# ============================================================

np.random.seed(SEED)
tf.random.set_seed(SEED)


# ============================================================
# INFORMATION
# ============================================================

print("=" * 80)
print("V4 STAGE 1 — HELD-OUT TEST EVALUATION")
print("=" * 80)

print("TensorFlow:", tf.__version__)
print("Keras:", keras.__version__)
print("Model:", MODEL_PATH)
print("Test directory:", TEST_DIR)
print("Image size:", IMAGE_SIZE)
print("Batch size:", BATCH_SIZE)

# ============================================================
# LOAD TEST DATA
# ============================================================

print("\n" + "=" * 80)
print("LOADING TEST DATA")
print("=" * 80)

test_ds = keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print("\nDetected classes:")
for i, name in enumerate(test_ds.class_names):
    print(f"{i}: {name}")


# ============================================================
# PREPROCESSING
# ============================================================

def mobilenet_preprocess(images, labels):
    images = tf.cast(images, tf.float32)
    images = (images / 127.5) - 1.0
    return images, labels


test_ds = test_ds.map(
    mobilenet_preprocess,
    num_parallel_calls=tf.data.AUTOTUNE,
)

test_ds = test_ds.prefetch(tf.data.AUTOTUNE)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n" + "=" * 80)
print("LOADING BEST STAGE 1 MODEL")
print("=" * 80)

model = keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)


# ============================================================
# MODEL EVALUATION
# ============================================================

print("\n" + "=" * 80)
print("RUNNING TEST EVALUATION")
print("=" * 80)

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1,
)

print("\nTest loss:", test_loss)
print("Test accuracy:", test_accuracy)


# ============================================================
# COLLECT PREDICTIONS
# ============================================================

print("\n" + "=" * 80)
print("GENERATING TEST PREDICTIONS")
print("=" * 80)

y_true = []
y_pred = []

for images, labels in test_ds:
    predictions = model.predict(
        images,
        verbose=0,
    )

    y_true.extend(
        np.argmax(labels.numpy(), axis=1)
    )

    y_pred.extend(
        np.argmax(predictions, axis=1)
    )

y_true = np.asarray(y_true)
y_pred = np.asarray(y_pred)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

macro_precision = precision_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

macro_recall = recall_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

macro_f1 = f1_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

weighted_precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

weighted_recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

weighted_f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y_true,
    y_pred,
    target_names=CLASS_NAMES,
    digits=4,
    zero_division=0,
)

print("\n" + "=" * 80)
print("CLASSIFICATION REPORT")
print("=" * 80)
print(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred,
)

print("=" * 80)
print("CONFUSION MATRIX")
print("=" * 80)

print("Rows = Actual")
print("Columns = Predicted\n")

print(" " * 30 + " ".join(
    f"{i:>8}"
    for i in range(NUM_CLASSES)
))

for i, row in enumerate(cm):
    print(
        f"{i:>28} "
        + " ".join(f"{value:>8}" for value in row)
    )


# ============================================================
# SAVE CONFUSION MATRIX CSV
# ============================================================

with open(
    CONFUSION_MATRIX_PATH,
    "w",
    encoding="utf-8",
) as f:
    f.write(
        "actual_class,"
        + ",".join(CLASS_NAMES)
        + "\n"
    )

    for i, row in enumerate(cm):
        f.write(
            CLASS_NAMES[i]
            + ","
            + ",".join(str(int(value)) for value in row)
            + "\n"
        )


# ============================================================
# SAVE CLASSIFICATION REPORT
# ============================================================

with open(
    REPORT_PATH,
    "w",
    encoding="utf-8",
) as f:
    f.write("V4 STAGE 1 — HELD-OUT TEST EVALUATION\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"Test loss: {test_loss:.6f}\n")
    f.write(f"Test accuracy: {test_accuracy:.6f}\n")
    f.write(f"Accuracy: {accuracy:.6f}\n")
    f.write(f"Macro precision: {macro_precision:.6f}\n")
    f.write(f"Macro recall: {macro_recall:.6f}\n")
    f.write(f"Macro F1: {macro_f1:.6f}\n")
    f.write(f"Weighted precision: {weighted_precision:.6f}\n")
    f.write(f"Weighted recall: {weighted_recall:.6f}\n")
    f.write(f"Weighted F1: {weighted_f1:.6f}\n\n")

    f.write("Classification report:\n")
    f.write(report)

    f.write("\n\nConfusion matrix:\n")
    f.write("Rows = Actual; Columns = Predicted\n\n")

    for row in cm:
        f.write(
            ",".join(str(int(value)) for value in row)
            + "\n"
        )


# ============================================================
# SAVE JSON RESULTS
# ============================================================

results = {
    "experiment": "Maize Disease CNN V4",
    "stage": 1,
    "model": str(MODEL_PATH),
    "test_samples": int(len(y_true)),
    "test_loss": float(test_loss),
    "test_accuracy": float(test_accuracy),
    "accuracy": float(accuracy),
    "macro_precision": float(macro_precision),
    "macro_recall": float(macro_recall),
    "macro_f1": float(macro_f1),
    "weighted_precision": float(weighted_precision),
    "weighted_recall": float(weighted_recall),
    "weighted_f1": float(weighted_f1),
    "class_names": CLASS_NAMES,
    "confusion_matrix": cm.tolist(),
}

with open(
    RESULTS_PATH,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        results,
        f,
        indent=2,
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("STAGE 1 TEST EVALUATION COMPLETE")
print("=" * 80)

print(f"Test samples:      {len(y_true):,}")
print(f"Test accuracy:     {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"Macro F1:          {macro_f1:.4f} ({macro_f1 * 100:.2f}%)")
print(f"Weighted F1:       {weighted_f1:.4f} ({weighted_f1 * 100:.2f}%)")

print("\nSaved:")
print("Results:", RESULTS_PATH)
print("Report:", REPORT_PATH)
print("Confusion matrix:", CONFUSION_MATRIX_PATH)

print("\n" + "=" * 80)
print("STAGE 1 BASELINE READY FOR COMPARISON")
print("=" * 80)
