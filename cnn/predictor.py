"""
CNN Image Predictor

Loads the trained V3 MobileNetV2 model, predicts the disease class
for an image, and maps the prediction to the PostgreSQL knowledge base.

CNN classes:

    0 → Blight
    1 → Common_Rust
    2 → Gray_Leaf_Spot
    3 → Healthy
"""

import os
import sys
try:
    import resource
except ImportError:
    resource = None

import joblib
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

MAIZE_GATE_MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "maize_gate_logistic_regression.joblib"
)

MAIZE_GATE_THRESHOLD = 0.45


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

print("Loading maize gate model...")

if not os.path.exists(MAIZE_GATE_MODEL_PATH):
    raise FileNotFoundError(
        f"Maize gate model not found:\n{MAIZE_GATE_MODEL_PATH}"
    )

try:
    maize_gate_model = joblib.load(
        MAIZE_GATE_MODEL_PATH
    )

    print(
        "Maize gate model loaded successfully."
    )

except Exception as error:
    print(
        f"MAIZE_GATE_LOAD_ERROR: "
        f"{type(error).__name__}: {error}"
    )
    raise


# ============================================================
# MAIZE GATE FEATURE EXTRACTOR
# ============================================================

maize_feature_extractor = tf.keras.Model(
    inputs=model.input,
    outputs=model.get_layer(
        "global_average_pooling2d"
    ).output
)


def check_maize_gate(image_array):
    """Check whether an image appears to contain maize."""

    print(
        "MAIZE_GATE_STEP_1: "
        "starting feature extraction"
    )

    if resource is not None:
        before_memory = resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss

        print(
            "MAIZE_GATE_MEMORY_BEFORE:",
            before_memory,
            "KB"
        )

    features = maize_feature_extractor.predict(
        image_array,
        verbose=0
    )

    if resource is not None:
        after_memory = resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss

        print(
            "MAIZE_GATE_MEMORY_AFTER:",
            after_memory,
            "KB"
        )

    print(
        "MAIZE_GATE_STEP_2: "
        "feature extraction complete"
    )

    maize_probability = float(
        maize_gate_model.predict_proba(
            features
        )[0, 1]
    )

    print(
        "MAIZE_GATE_STEP_3: "
        "gate prediction complete"
    )

    is_maize = (
        maize_probability >= MAIZE_GATE_THRESHOLD
    )

    return {
        "is_maize": is_maize,
        "maize_probability": maize_probability,
        "maize_gate_threshold": MAIZE_GATE_THRESHOLD
    }


# ============================================================
# PREDICT IMAGE
# ============================================================

def predict_image(image_path):
    """
    Predict the maize disease class for one image.

    Diagnostic policy:

        - Global confidence threshold: 70%
        - Blight ↔ Gray Leaf Spot: caution pair

    Returns a dictionary containing maize-gate fields and,
    when accepted by the gate, disease classification fields.
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

    image = tf.io.read_file(
        image_path
    )

    image = tf.image.decode_image(
        image,
        channels=3,
        expand_animations=False,
    )

    image = tf.image.resize(
        image,
        IMAGE_SIZE
    )

    image = tf.cast(
        image,
        tf.float32
    )

    image_array = (
        tf.keras.applications.mobilenet_v2.preprocess_input(
            image
        )
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # ========================================================
    # MAIZE GATE
    #
    # Reject images that do not appear to contain maize
    # before running the disease classifier.
    # ========================================================

    gate_result = check_maize_gate(
        image_array
    )

    if not gate_result["is_maize"]:

        return {
            "image_path": image_path,

            "is_maize": False,

            "maize_probability":
                gate_result["maize_probability"],

            "maize_gate_threshold":
                gate_result["maize_gate_threshold"],

            "maize_gate_status":
                "rejected",

            "class_index": None,

            "class_name": None,

            "confidence": None,

            "confidence_threshold":
                CONFIDENCE_THRESHOLD,

            "confidence_status":
                "not_run",

            "caution_required":
                False,

            "caution_reason":
                None,

            "health_problem_id":
                None,

            "is_healthy":
                None,

            "rejection_reason": (
                "The uploaded image does not appear "
                "to contain maize. Please upload a "
                "clear image of a maize plant or leaf."
            )
        }

    # ========================================================
    # CNN PREDICTION
    # ========================================================

    if resource is not None:
        memory_usage_before = resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss

        print(
            "DISEASE_MODEL_MEMORY_BEFORE: "
            f"{memory_usage_before} KB"
        )

    print(
        "DISEASE_MODEL_STEP_1: "
        "starting disease model prediction"
    )

    predictions = model(
        image_array,
        training=False
    ).numpy()

    print(
        "DISEASE_MODEL_STEP_2: "
        "disease model prediction complete"
    )

    print(
        "DISEASE_MODEL_STEP_3: "
        "processing prediction result"
    )

    # ========================================================
    # TRACE PREDICTION RESULT
    # ========================================================

    try:

        print(
            "PREDICTION_RESULT_STEP_1: "
            "extracting probability array"
        )

        probabilities = predictions[0]

        print(
            "PREDICTION_RESULT_STEP_2: "
            f"probability array extracted; "
            f"shape={np.shape(probabilities)}"
        )

        # ====================================================
        # GET PREDICTED CLASS
        # ====================================================

        print(
            "PREDICTION_RESULT_STEP_3: "
            "calculating predicted class"
        )

        class_index = int(
            np.argmax(probabilities)
        )

        confidence = float(
            probabilities[class_index]
        )

        print(
            "PREDICTION_RESULT_STEP_4: "
            f"class_index={class_index}, "
            f"confidence={confidence}"
        )

        # ====================================================
        # MAP CNN CLASS TO KNOWLEDGE BASE
        # ====================================================

        print(
            "PREDICTION_RESULT_STEP_5: "
            "loading prediction mapping"
        )

        mapping = get_prediction_mapping(
            class_index
        )

        print(
            "PREDICTION_RESULT_STEP_6: "
            f"mapping received: {mapping}"
        )

        class_name = mapping["class_name"]

        print(
            "PREDICTION_RESULT_STEP_7: "
            f"class_name={class_name}"
        )

        # ====================================================
        # CONFIDENCE DECISION
        # ====================================================

        if confidence >= CONFIDENCE_THRESHOLD:

            confidence_status = "accepted"

        else:

            confidence_status = "uncertain"

        print(
            "PREDICTION_RESULT_STEP_8: "
            f"confidence_status={confidence_status}"
        )

        # ====================================================
        # BLIGHT ↔ GRAY LEAF SPOT CAUTION
        # ====================================================

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

        print(
            "PREDICTION_RESULT_STEP_9: "
            f"caution_required={caution_required}"
        )

        # ====================================================
        # BUILD RESULT
        # ====================================================

        result = {

            "image_path": image_path,

            "is_maize": True,

            "maize_probability":
                gate_result["maize_probability"],

            "maize_gate_threshold":
                gate_result["maize_gate_threshold"],

            "maize_gate_status":
                "accepted",

            "class_index":
                class_index,

            "class_name":
                class_name,

            "confidence":
                confidence,

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

        print(
            "PREDICTION_RESULT_STEP_10: "
            "result dictionary built successfully"
        )

        return result

    except Exception as error:

        print(
            "PREDICTION_RESULT_ERROR: "
            f"{type(error).__name__}: {error}"
        )

        raise


# ============================================================
# PREDICT MULTIPLE IMAGES
# ============================================================

def predict_images(image_paths):
    """
    Predict and aggregate multiple images as one diagnostic case.

    Each image is evaluated independently using the existing
    single-image prediction pipeline.

    A diagnostic case may contain multiple findings.

    Returns:
        A dictionary containing:

            total_images
                Total number of submitted images.

            image_results
                Individual prediction result for every image.

            contributing_images
                Images accepted by the maize gate.

            excluded_images
                Images rejected by the maize gate.

            diagnostic_findings
                Grouped diagnostic findings with confidence
                and consistency information.
    """

    if not image_paths:

        raise ValueError(
            "At least one image is required for diagnosis."
        )

    image_results = []

    # ========================================================
    # PREDICT EACH IMAGE INDEPENDENTLY
    # ========================================================

    for image_path in image_paths:

        result = predict_image(
            image_path
        )

        image_results.append(
            result
        )

    # ========================================================
    # SEPARATE CONTRIBUTING AND EXCLUDED IMAGES
    # ========================================================

    contributing_results = [
        result
        for result in image_results
        if result["is_maize"]
    ]

    excluded_results = [
        result
        for result in image_results
        if not result["is_maize"]
    ]

    # ========================================================
    # GROUP DIAGNOSTIC FINDINGS
    # ========================================================

    diagnostic_findings = {}

    for result in contributing_results:

        class_name = result["class_name"]

        if class_name not in diagnostic_findings:

            diagnostic_findings[class_name] = {

                "class_name":
                    class_name,

                "health_problem_id":
                    result["health_problem_id"],

                "is_healthy":
                    result["is_healthy"],

                "image_count":
                    0,

                "accepted_count":
                    0,

                "uncertain_count":
                    0,

                "image_paths":
                    [],

                "confidences":
                    [],

                "caution_required":
                    False,

                "caution_reasons":
                    []
            }

        finding = diagnostic_findings[
            class_name
        ]

        finding["image_count"] += 1

        finding["image_paths"].append(
            result["image_path"]
        )

        if result["confidence"] is not None:

            finding["confidences"].append(
                result["confidence"]
            )

        # ====================================================
        # CONFIDENCE STATUS
        # ====================================================

        if (
            result["confidence_status"]
            == "accepted"
        ):

            finding["accepted_count"] += 1

        elif (
            result["confidence_status"]
            == "uncertain"
        ):

            finding["uncertain_count"] += 1

        # ====================================================
        # CAUTION
        # ====================================================

        if result["caution_required"]:

            finding["caution_required"] = True

            if result["caution_reason"]:

                if (
                    result["caution_reason"]
                    not in finding["caution_reasons"]
                ):

                    finding[
                        "caution_reasons"
                    ].append(
                        result["caution_reason"]
                    )

    # ========================================================
    # DETERMINE FINDING STATUS
    # ========================================================

    for finding in diagnostic_findings.values():

        if (
            finding["accepted_count"]
            == finding["image_count"]
        ):

            finding["finding_status"] = (
                "identified"
            )

        elif (
            finding["accepted_count"] > 0
        ):

            finding["finding_status"] = (
                "identified_with_uncertainty"
            )

        else:

            finding["finding_status"] = (
                "possible"
            )

        # ====================================================
        # AVERAGE CONFIDENCE
        # ====================================================

        if finding["confidences"]:

            finding["average_confidence"] = (
                sum(
                    finding["confidences"]
                )
                / len(
                    finding["confidences"]
                )
            )

        else:

            finding["average_confidence"] = None

    # ========================================================
    # BUILD FINAL RESULT
    # ========================================================

    return {

        "total_images":
            len(image_results),

        "image_results":
            image_results,

        "contributing_images":
            contributing_results,

        "excluded_images":
            excluded_results,

        "diagnostic_findings":
            list(
                diagnostic_findings.values()
            )
    }


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

    print(
        "\n" + "=" * 60
    )

    print(
        "V3 MOBILENETV2 IMAGE PREDICTION TEST"
    )

    print(
        "=" * 60
    )

    result = predict_image(
        image_path
    )

    print("\nImage:")

    print(
        f"  {result['image_path']}"
    )

    print("\nPrediction:")

    print(
        f"  Class index : "
        f"{result['class_index']}"
    )

    print(
        f"  Class name  : "
        f"{result['class_name']}"
    )

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