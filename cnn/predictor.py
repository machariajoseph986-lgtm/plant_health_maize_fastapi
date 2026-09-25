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
# PROJECT CONFIGURATION
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# Keep the original Keras path for compatibility/reference.
# The application now uses the TFLite model below.
MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "v3",
    "best_maize_disease_mobilenetv2_v3_finetuned.keras"
)

DISEASE_MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "v3",
    "maize_disease.tflite"
)

FEATURE_EXTRACTOR_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "v3",
    "maize_feature_extractor.tflite"
)

IMAGE_SIZE = (320, 320)

MAIZE_GATE_MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "training_output",
    "maize_gate_logistic_regression.joblib"
)

MAIZE_GATE_THRESHOLD = 0.45


# ============================================================
# MEMORY DIAGNOSTICS
# ============================================================

def get_memory_mb():
    """
    Return the current process memory usage in MB.

    Linux:
        resource.ru_maxrss is reported in KB.

    Other systems:
        resource.ru_maxrss may be reported in bytes.
    """

    try:

        if resource is None:
            return None

        memory = resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss

        if sys.platform.startswith("linux"):
            return memory / 1024

        return memory / (1024 * 1024)

    except Exception:
        return None


def log_memory(label):
    """
    Print memory usage for deployment diagnostics.
    """

    memory_mb = get_memory_mb()

    if memory_mb is not None:

        print(
            f"{label}: "
            f"{memory_mb:.2f} MB"
        )


# ============================================================
# LOAD TFLITE DISEASE MODEL
# ============================================================

print(
    "Loading TFLite disease model..."
)

if not os.path.exists(
    DISEASE_MODEL_PATH
):

    raise FileNotFoundError(
        "TFLite disease model not found:\n"
        f"{DISEASE_MODEL_PATH}"
    )


try:

    disease_interpreter = (
        tf.lite.Interpreter(
            model_path=DISEASE_MODEL_PATH
        )
    )

    disease_interpreter.allocate_tensors()

    disease_input_details = (
        disease_interpreter.get_input_details()
    )

    disease_output_details = (
        disease_interpreter.get_output_details()
    )

    print(
        "TFLite disease model "
        "loaded successfully."
    )

except Exception as error:

    print(
        "DISEASE_TFLITE_LOAD_ERROR: "
        f"{type(error).__name__}: {error}"
    )

    raise


# ============================================================
# LOAD TFLITE MAIZE FEATURE EXTRACTOR
# ============================================================

print(
    "Loading TFLite maize feature extractor..."
)

if not os.path.exists(
    FEATURE_EXTRACTOR_PATH
):

    raise FileNotFoundError(
        "TFLite feature extractor not found:\n"
        f"{FEATURE_EXTRACTOR_PATH}"
    )


try:

    maize_feature_interpreter = (
        tf.lite.Interpreter(
            model_path=FEATURE_EXTRACTOR_PATH
        )
    )

    maize_feature_interpreter.allocate_tensors()

    maize_feature_input_details = (
        maize_feature_interpreter.get_input_details()
    )

    maize_feature_output_details = (
        maize_feature_interpreter.get_output_details()
    )

    print(
        "TFLite maize feature extractor "
        "loaded successfully."
    )

except Exception as error:

    print(
        "FEATURE_TFLITE_LOAD_ERROR: "
        f"{type(error).__name__}: {error}"
    )

    raise


# ============================================================
# LOAD MAIZE GATE MODEL
# ============================================================

print(
    "Loading maize gate model..."
)

if not os.path.exists(
    MAIZE_GATE_MODEL_PATH
):

    raise FileNotFoundError(
        "Maize gate model not found:\n"
        f"{MAIZE_GATE_MODEL_PATH}"
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
        "MAIZE_GATE_LOAD_ERROR: "
        f"{type(error).__name__}: {error}"
    )

    raise


# ============================================================
# TFLITE FEATURE EXTRACTION
# ============================================================

def extract_maize_features(
    image_array
):
    """
    Extract the 1,280 MobileNetV2 features
    required by the maize gate model.
    """

    log_memory(
        "FEATURE_TFLITE_MEMORY_BEFORE"
    )

    print(
        "FEATURE_TFLITE_STEP_1: "
        "starting feature extraction"
    )

    try:

        input_details = (
            maize_feature_input_details[0]
        )

        output_details = (
            maize_feature_output_details[0]
        )

        input_index = (
            input_details["index"]
        )

        output_index = (
            output_details["index"]
        )

        # Make sure the input is float32,
        # matching the original Keras pipeline.
        input_data = np.asarray(
            image_array,
            dtype=np.float32
        )

        maize_feature_interpreter.set_tensor(
            input_index,
            input_data
        )

        maize_feature_interpreter.invoke()

        features = (
            maize_feature_interpreter.get_tensor(
                output_index
            )
        )

        print(
            "FEATURE_TFLITE_STEP_2: "
            "feature extraction complete"
        )

        log_memory(
            "FEATURE_TFLITE_MEMORY_AFTER"
        )

        return features

    except Exception as error:

        print(
            "FEATURE_TFLITE_INFERENCE_ERROR: "
            f"{type(error).__name__}: {error}"
        )

        raise


# ============================================================
# MAIZE GATE CHECK
# ============================================================

def check_maize_gate(
    image_array
):
    """
    Determine whether the uploaded image
    is likely to be a maize image.

    The LogisticRegression gate expects
    1,280 MobileNetV2 features.
    """

    try:

        features = extract_maize_features(
            image_array
        )

        print(
            "MAIZE_GATE_STEP_2: "
            "feature extraction complete"
        )

        gate_probability = (
            maize_gate_model.predict_proba(
                features
            )[0][1]
        )

        print(
            "MAIZE_GATE_STEP_3: "
            "gate prediction complete"
        )

        log_memory(
            "MAIZE_GATE_MEMORY_AFTER"
        )

        gate_probability = float(
            gate_probability
        )

        gate_decision = (
            gate_probability
            >= MAIZE_GATE_THRESHOLD
        )

        return (
            gate_decision,
            gate_probability
        )

    except Exception as error:

        print(
            "MAIZE_GATE_ERROR: "
            f"{type(error).__name__}: {error}"
        )

        raise


# ============================================================
# TFLITE DISEASE PREDICTION
# ============================================================

def predict_disease(
    image_array
):
    """
    Run disease classification using
    the TFLite disease model.
    """

    log_memory(
        "DISEASE_MODEL_MEMORY_BEFORE"
    )

    print(
        "DISEASE_MODEL_STEP_1: "
        "starting disease model prediction"
    )

    try:

        input_details = (
            disease_input_details[0]
        )

        output_details = (
            disease_output_details[0]
        )

        input_index = (
            input_details["index"]
        )

        output_index = (
            output_details["index"]
        )

        input_data = np.asarray(
            image_array,
            dtype=np.float32
        )

        disease_interpreter.set_tensor(
            input_index,
            input_data
        )

        disease_interpreter.invoke()

        predictions = (
            disease_interpreter.get_tensor(
                output_index
            )
        )

        print(
            "DISEASE_MODEL_STEP_2: "
            "disease model prediction complete"
        )

        log_memory(
            "DISEASE_MODEL_MEMORY_AFTER"
        )

        return predictions

    except Exception as error:

        print(
            "DISEASE_TFLITE_INFERENCE_ERROR: "
            f"{type(error).__name__}: {error}"
        )

        raise


# ============================================================
# SINGLE IMAGE PREDICTION
# ============================================================

def predict_image(
    image_path
):
    """
    Predict the disease in one image.
    """

    CONFIDENCE_THRESHOLD = 0.70

    BLIGHT_GRAY_PAIR = {
        "Blight",
        "Gray_Leaf_Spot"
    }

    try:

        # ----------------------------------------------------
        # Validate image path
        # ----------------------------------------------------

        if not os.path.exists(
            image_path
        ):

            raise FileNotFoundError(
                f"Image not found:\n{image_path}"
            )

        print(
            f"Processing image: {image_path}"
        )

        log_memory(
            "IMAGE_MEMORY_START"
        )

        # ----------------------------------------------------
        # Read image
        # ----------------------------------------------------

        image_bytes = tf.io.read_file(
            image_path
        )

        print(
            "IMAGE_STEP_1: image file read"
        )

        # ----------------------------------------------------
        # Decode image
        # ----------------------------------------------------

        image = tf.image.decode_image(
            image_bytes,
            channels=3,
            expand_animations=False
        )

        print(
            "IMAGE_STEP_2: image decoded"
        )

        # ----------------------------------------------------
        # Resize image
        # ----------------------------------------------------

        image = tf.image.resize(
            image,
            IMAGE_SIZE
        )

        print(
            "IMAGE_STEP_3: image resized"
        )

        # ----------------------------------------------------
        # Convert to float32
        # ----------------------------------------------------

        image = tf.cast(
            image,
            tf.float32
        )

        # ----------------------------------------------------
        # MobileNetV2 preprocessing
        #
        # This converts pixel values from
        # [0, 255] to approximately [-1, 1].
        # ----------------------------------------------------

        image = (
            tf.keras.applications
            .mobilenet_v2
            .preprocess_input(
                image
            )
        )

        # ----------------------------------------------------
        # Add batch dimension
        # ----------------------------------------------------

        image_array = tf.expand_dims(
            image,
            axis=0
        )

        image_array = image_array.numpy()

        print(
            "IMAGE_STEP_4: image preprocessing complete"
        )

        print(
            "IMAGE_INPUT_SHAPE:",
            image_array.shape
        )

        print(
            "IMAGE_INPUT_DTYPE:",
            image_array.dtype
        )

        print(
            "IMAGE_INPUT_MIN:",
            float(np.min(image_array))
        )

        print(
            "IMAGE_INPUT_MAX:",
            float(np.max(image_array))
        )

        log_memory(
            "IMAGE_MEMORY_AFTER_PREPROCESS"
        )

        # ----------------------------------------------------
        # MAIZE GATE
        # ----------------------------------------------------

        print(
            "MAIZE_GATE_STEP_1: "
            "starting maize gate"
        )

        (
            maize_gate_accepted,
            maize_gate_probability
        ) = check_maize_gate(
            image_array
        )

        # ----------------------------------------------------
        # Reject non-maize images
        # ----------------------------------------------------

        if not maize_gate_accepted:

            print(
                "MAIZE_GATE_DECISION: "
                "REJECTED"
            )

            print(
                "MAIZE_GATE_PROBABILITY:",
                maize_gate_probability
            )

            return {

                "image_path": image_path,

                "maize_gate_status": "rejected",

                "maize_gate_probability":
                    maize_gate_probability,

                "maize_gate_threshold":
                    MAIZE_GATE_THRESHOLD,

                "disease_status": None,

                "class_index": None,

                "class_name": None,

                "confidence": None,

                "confidence_status": None,

                "prediction": None,

                "health_problem_id": None,

                "pathogen": None,

                "symptoms": None,

                "management": None,

                "chemical_management": None,

                "caution": None,

                "caution_reason": None,

                "rejection_reason":
                    "The uploaded image does not "
                    "appear to contain maize. "
                    "Please upload a clear image "
                    "of a maize plant or maize leaf."

            }

        # ----------------------------------------------------
        # ACCEPTED BY MAIZE GATE
        # ----------------------------------------------------

        print(
            "MAIZE_GATE_DECISION: ACCEPTED"
        )

        print(
            "MAIZE_GATE_PROBABILITY:",
            maize_gate_probability
        )

        # ----------------------------------------------------
        # DISEASE MODEL
        # ----------------------------------------------------

        predictions = predict_disease(
            image_array
        )

        # ----------------------------------------------------
        # Extract probabilities
        # ----------------------------------------------------

        probabilities = predictions[0]

        class_index = int(
            np.argmax(
                probabilities
            )
        )

        confidence = float(
            probabilities[class_index]
        )

        # ----------------------------------------------------
        # Map prediction to application
        # ----------------------------------------------------

        mapping = get_prediction_mapping(
            class_index
        )

        class_name = mapping[
            "class_name"
        ]

        # ----------------------------------------------------
        # Confidence status
        # ----------------------------------------------------

        if confidence >= CONFIDENCE_THRESHOLD:

            confidence_status = "accepted"

        else:

            confidence_status = "uncertain"

        # ----------------------------------------------------
        # Disease status
        # ----------------------------------------------------

        disease_status = (
            "accepted"
            if confidence >= CONFIDENCE_THRESHOLD
            else "uncertain"
        )

        # ----------------------------------------------------
        # Caution handling
        # ----------------------------------------------------

        caution = None
        caution_reason = None

        if class_name in BLIGHT_GRAY_PAIR:

            caution = True

            caution_reason = (
                "Blight and Gray Leaf Spot can "
                "share similar visual symptoms. "
                "Use the diagnosis together with "
                "the visible symptoms and other "
                "available information."
            )

        else:

            caution = False

        # ----------------------------------------------------
        # Build result
        # ----------------------------------------------------

        result = {

            "image_path": image_path,

            "maize_gate_status":
                "accepted",

            "maize_gate_probability":
                maize_gate_probability,

            "maize_gate_threshold":
                MAIZE_GATE_THRESHOLD,

            "disease_status":
                disease_status,

            "class_index":
                class_index,

            "class_name":
                class_name,

            "confidence":
                confidence,

            "confidence_status":
                confidence_status,

            "prediction":
                mapping,

            "health_problem_id":
                mapping.get(
                    "health_problem_id"
                ),

            "pathogen":
                mapping.get(
                    "pathogen"
                ),

            "symptoms":
                mapping.get(
                    "symptoms"
                ),

            "management":
                mapping.get(
                    "management"
                ),

            "chemical_management":
                mapping.get(
                    "chemical_management"
                ),

            "caution":
                caution,

            "caution_reason":
                caution_reason,

            "rejection_reason":
                None

        }

        # ----------------------------------------------------
        # Logging
        # ----------------------------------------------------

        print(
            "DISEASE_CLASS_INDEX:",
            class_index
        )

        print(
            "DISEASE_CLASS_NAME:",
            class_name
        )

        print(
            "DISEASE_CONFIDENCE:",
            confidence
        )

        print(
            "DISEASE_STATUS:",
            disease_status
        )

        log_memory(
            "PREDICTION_MEMORY_FINAL"
        )

        return result

    except Exception as error:

        print(
            "PREDICTION_ERROR: "
            f"{type(error).__name__}: {error}"
        )

        raise


# ============================================================
# MULTIPLE IMAGE PREDICTION
# ============================================================

def predict_images(
    image_paths
):
    """
    Predict multiple images and aggregate
    the contributing findings.

    Existing application behavior is preserved:
    - accepted maize images contribute
    - rejected/non-maize images are excluded
    - findings are grouped
    """

    results = []

    contributing_results = []

    excluded_results = []

    for image_path in image_paths:

        result = predict_image(
            image_path
        )

        results.append(
            result
        )

        if (
            result.get(
                "maize_gate_status"
            )
            == "accepted"
        ):

            contributing_results.append(
                result
            )

        else:

            excluded_results.append(
                result
            )

    # --------------------------------------------------------
    # Group findings
    # --------------------------------------------------------

    findings = {}

    for result in contributing_results:

        health_problem_id = result.get(
            "health_problem_id"
        )

        class_name = result.get(
            "class_name"
        )

        key = (
            health_problem_id
            or class_name
        )

        if key not in findings:

            findings[key] = {
                "health_problem_id":
                    health_problem_id,

                "class_name":
                    class_name,

                "images": [],

                "confidence_values": [],

                "highest_confidence":
                    None
            }

        findings[key][
            "images"
        ].append(
            result.get(
                "image_path"
            )
        )

        confidence = result.get(
            "confidence"
        )

        if confidence is not None:

            findings[key][
                "confidence_values"
            ].append(
                confidence
            )

    # --------------------------------------------------------
    # Calculate highest confidence
    # --------------------------------------------------------

    for finding in findings.values():

        confidence_values = finding[
            "confidence_values"
        ]

        if confidence_values:

            finding[
                "highest_confidence"
            ] = max(
                confidence_values
            )

    # --------------------------------------------------------
    # Return aggregate result
    # --------------------------------------------------------

    return {

        "results":
            results,

        "contributing_results":
            contributing_results,

        "excluded_results":
            excluded_results,

        "findings":
            list(
                findings.values()
            ),

        "total_images":
            len(image_paths),

        "contributing_images":
            len(
                contributing_results
            ),

        "excluded_images":
            len(
                excluded_results
            )

    }


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python -m cnn.predictor "
            "<image_path>"
        )

        sys.exit(1)

    image_path = sys.argv[1]

    result = predict_image(
        image_path
    )

    print(
        "\nPrediction result:"
    )

    print(
        result
    )