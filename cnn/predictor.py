"""
CNN Image Predictor

Loads the trained V3 MobileNetV2 model, predicts the disease class
for an image, and maps the prediction to the SQLite knowledge base.

CNN classes:

    0 → Blight
    1 → Common_Rust
    2 → Gray_Leaf_Spot
    3 → Healthy
"""

import os
import sys

import numpy as np
import tensorflow as tf

try:
    from .mapping import (
        get_prediction_mapping,
    )
except ImportError:
    from mapping import (
        get_prediction_mapping,
    )


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "v3",
    "best_maize_disease_mobilenetv2_v3_finetuned.keras"
)

IMAGE_SIZE = (320, 320)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading V3 MobileNetV2 model...")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"V3 MobileNetV2 model not found:\n{MODEL_PATH}"
    )

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

print("V3 MobileNetV2 model loaded successfully.")


# ============================================================
# PREDICT IMAGE
# ============================================================

def predict_image(image_path):
    """
    Predict the maize disease class for one image.

    Diagnostic policy:

        - Global confidence threshold: 70%
        - Blight ↔ Gray Leaf Spot: caution pair

    Returns a dictionary containing:

        image_path
        class_index
        class_name
        confidence
        confidence_threshold
        confidence_status
        caution_required
        caution_reason
        health_problem_id
        is_healthy
    """

    # ========================================================
    # DIAGNOSTIC POLICY
    # ========================================================

    CONFIDENCE_THRESHOLD = 0.70

    BLIGHT_GRAY_PAIR = {
        "Blight",
        "Gray_Leaf_Spot"
    }

    # ========================================================
    # CHECK IMAGE
    # ========================================================

    if not os.path.exists(image_path):

        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    # ========================================================
    # CONVERT IMAGE TO ARRAY
    # ========================================================

    image_array = tf.keras.utils.img_to_array(
        image
    )

    # ========================================================
    # MOBILENETV2 PREPROCESSING
    #
    # Matches V3 training/evaluation preprocessing.
    # Converts pixel values from [0, 255] to [-1, 1].
    # ========================================================

    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    # ========================================================
    # ADD BATCH DIMENSION
    # ========================================================

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # ========================================================
    # CNN PREDICTION
    # ========================================================

    predictions = model.predict(
        image_array,
        verbose=0
    )

    probabilities = predictions[0]

    # ========================================================
    # GET PREDICTED CLASS
    # ========================================================

    class_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        probabilities[class_index]
    )

    # ========================================================
    # MAP CNN CLASS TO KNOWLEDGE BASE
    # ========================================================

    mapping = get_prediction_mapping(
        class_index
    )

    class_name = mapping["class_name"]

    # ========================================================
    # CONFIDENCE DECISION
    # ========================================================

    if confidence >= CONFIDENCE_THRESHOLD:

        confidence_status = "accepted"

    else:

        confidence_status = "uncertain"

    # ========================================================
    # BLIGHT ↔ GRAY LEAF SPOT CAUTION
    # ========================================================

    caution_required = (
        class_name in BLIGHT_GRAY_PAIR
    )

    if caution_required:

        caution_reason = (
            "Blight and Gray Leaf Spot remain a known "
            "high-confusion disease pair in the evaluated "
            "model results."
        )

    else:

        caution_reason = None

    # ========================================================
    # BUILD RESULT
    # ========================================================

    result = {

        "image_path": image_path,

        "class_index": class_index,

        "class_name": class_name,

        "confidence": confidence,

        "confidence_threshold":
            CONFIDENCE_THRESHOLD,

        "confidence_status":
            confidence_status,

        "caution_required":
            caution_required,

        "caution_reason":
            caution_reason,

        "health_problem_id":
            mapping["health_problem_id"],

        "is_healthy":
            mapping["is_healthy"]
    }

    return result


# ============================================================
# COMMAND-LINE TEST
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("\nUsage:")
        print(
            "python cnn/predictor.py "
            "<image_path>"
        )

        sys.exit(1)

    image_path = sys.argv[1]

    print("\n" + "=" * 60)
    print("V3 MOBILENETV2 IMAGE PREDICTION TEST")
    print("=" * 60)

    result = predict_image(
        image_path
    )

    print("\nImage:")
    print(f"  {result['image_path']}")

    print("\nPrediction:")
    print(f"  Class index : {result['class_index']}")
    print(f"  Class name  : {result['class_name']}")
    print(
        f"  Confidence  : "
        f"{result['confidence'] * 100:.2f}%"
    )

    print(
        f"  Threshold   : "
        f"{result['confidence_threshold'] * 100:.2f}%"
    )

    print(
        f"  Status      : "
        f"{result['confidence_status'].upper()}"
    )

    print(
        f"  Caution     : "
        f"{'YES' if result['caution_required'] else 'NO'}"
    )

    if result["caution_required"]:

        print(
            f"  Reason      : "
            f"{result['caution_reason']}"
        )

    print("\nKnowledge Base:")
    print(
        f"  Health problem ID : "
        f"{result['health_problem_id']}"
    )

    print(
        f"  Healthy           : "
        f"{result['is_healthy']}"
    )

    print("\n" + "=" * 60)