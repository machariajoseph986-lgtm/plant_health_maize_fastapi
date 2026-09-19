import os
import sys


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


# ============================================================
# IMPORT PROJECT COMPONENTS
# ============================================================

from cnn.predictor import (
    predict_image,
    predict_images
)
from cnn.mapping import get_prediction_mapping
from knowledge_base.database_postgresql import get_disease_profile


# ============================================================
# CNN → DATABASE INTEGRATION
# ============================================================

def diagnose_from_image(image_path):
    """
    Complete plant-health diagnosis pipeline:

    Image
      ↓
    CNN prediction
      ↓
    CNN class → Knowledge Base ID
      ↓
    PostgreSQL disease profile

    The result also preserves the CNN diagnostic decision
    information:

        - confidence_status
        - caution_required
        - caution_reason
    """

    # --------------------------------------------------------
    # STEP 1: CNN PREDICTION
    # --------------------------------------------------------

    prediction = predict_image(
        image_path
    )

    if prediction.get("is_maize") is False:
        return prediction

    class_index = prediction["class_index"]
    class_name = prediction["class_name"]
    confidence = prediction["confidence"]

    # Preserve CNN diagnostic decision information
    confidence_status = prediction[
        "confidence_status"
    ]

    caution_required = prediction[
        "caution_required"
    ]

    caution_reason = prediction[
        "caution_reason"
    ]


    # --------------------------------------------------------
    # STEP 2: CNN → KNOWLEDGE BASE MAPPING
    # --------------------------------------------------------

    mapping = get_prediction_mapping(
        class_index
    )

    health_problem_id = mapping[
        "health_problem_id"
    ]

    is_healthy = mapping[
        "is_healthy"
    ]


    # --------------------------------------------------------
    # STEP 3: HEALTHY CASE
    # --------------------------------------------------------

    if is_healthy:

        return {
            "image_path": image_path,

            "class_index": class_index,

            "class_name": class_name,

            "confidence": confidence,

            "confidence_status":
                confidence_status,

            "caution_required":
                caution_required,

            "caution_reason":
                caution_reason,

            "health_problem_id": None,

            "is_healthy": True,

            "disease_profile": None
        }


    # --------------------------------------------------------
    # STEP 4: DATABASE LOOKUP
    # --------------------------------------------------------

    disease_profile = get_disease_profile(
        health_problem_id
    )


    # --------------------------------------------------------
    # STEP 5: RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return {
        "image_path": image_path,

        "class_index": class_index,

        "class_name": class_name,

        "confidence": confidence,

        "confidence_status":
            confidence_status,

        "caution_required":
            caution_required,

        "caution_reason":
            caution_reason,

        "health_problem_id":
            health_problem_id,

        "is_healthy": False,

        "disease_profile":
            disease_profile
    }

def diagnose_from_images(image_paths):
    """
    Complete plant-health diagnosis pipeline for multiple images.

    Each image is evaluated independently by the CNN maize gate
    and disease classifier. Matching disease findings are grouped,
    and each disease finding receives its PostgreSQL profile once.

    Healthy findings do not receive a disease profile.

    Returns:
        A dictionary containing:
            - total_images
            - image_results
            - contributing_images
            - excluded_images
            - diagnostic_findings
    """

    if not image_paths:
        raise ValueError(
            "At least one image is required for diagnosis."
        )

    prediction_result = predict_images(
        image_paths
    )

    diagnostic_findings = []

    for finding in prediction_result[
        "diagnostic_findings"
    ]:

        finding_result = dict(
            finding
        )

        is_healthy = finding[
            "is_healthy"
        ]

        health_problem_id = finding[
            "health_problem_id"
        ]

        if (
            not is_healthy
            and health_problem_id
        ):

            finding_result[
                "disease_profile"
            ] = get_disease_profile(
                health_problem_id
            )

        else:

            finding_result[
                "disease_profile"
            ] = None

        diagnostic_findings.append(
            finding_result
        )

    return {
        "total_images":
            prediction_result[
                "total_images"
            ],

        "image_results":
            prediction_result[
                "image_results"
            ],

        "contributing_images":
            prediction_result[
                "contributing_images"
            ],

        "excluded_images":
            prediction_result[
                "excluded_images"
            ],

        "diagnostic_findings":
            diagnostic_findings
    }

# ============================================================
# COMMAND-LINE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CNN → DATABASE INTEGRATION TEST")
    print("=" * 60)


    # --------------------------------------------------------
    # CHECK IMAGE ARGUMENT
    # --------------------------------------------------------

    if len(sys.argv) != 2:

        print("\nUsage:")

        print(
            "python cnn/database_integration.py "
            "<image_path>"
        )

        sys.exit(1)


    image_path = sys.argv[1]


    # --------------------------------------------------------
    # CHECK IMAGE EXISTS
    # --------------------------------------------------------

    if not os.path.exists(image_path):

        print("\nERROR: Image not found:")

        print(image_path)

        sys.exit(1)


    print("\nImage:")

    print(
        f"  {image_path}"
    )


    print(
        "\nRunning complete pipeline..."
    )


    try:

        result = diagnose_from_image(
            image_path
        )


        # ----------------------------------------------------
        # DISPLAY CNN RESULT
        # ----------------------------------------------------

        print(
            "\n" + "-" * 60
        )

        print(
            "CNN RESULT"
        )

        print(
            "-" * 60
        )

        print(
            f"\nPredicted class : "
            f"{result['class_name']}"
        )

        print(
            f"Confidence      : "
            f"{result['confidence']:.2%}"
        )

        print(
            f"Class index     : "
            f"{result['class_index']}"
        )

        print(
            f"Confidence status: "
            f"{result['confidence_status'].upper()}"
        )


        # ----------------------------------------------------
        # DISPLAY DIAGNOSTIC CAUTION
        # ----------------------------------------------------

        print(
            f"Caution required : "
            f"{'YES' if result['caution_required'] else 'NO'}"
        )

        if result["caution_required"]:

            print(
                f"Caution reason   : "
                f"{result['caution_reason']}"
            )


        # ----------------------------------------------------
        # DISPLAY MAPPING RESULT
        # ----------------------------------------------------

        print(
            "\n" + "-" * 60
        )

        print(
            "KNOWLEDGE BASE MAPPING"
        )

        print(
            "-" * 60
        )

        if result["health_problem_id"]:

            print(
                f"\nKnowledge Base ID : "
                f"{result['health_problem_id']}"
            )

        else:

            print(
                "\nKnowledge Base ID : "
                "None (Healthy)"
            )


        # ----------------------------------------------------
        # HEALTHY CASE
        # ----------------------------------------------------

        if result["is_healthy"]:

            print("\nResult:")

            print(
                "  Healthy maize detected."
            )

            print(
                "  No disease profile required."
            )


        # ----------------------------------------------------
        # DISEASE CASE
        # ----------------------------------------------------

        else:

            profile = result[
                "disease_profile"
            ]


            if profile is None:

                print(
                    "\nERROR: The CNN mapped to a "
                    "knowledge-base ID, but no disease "
                    "profile was found in PostgreSQL."
                )

                sys.exit(1)


            print(
                "\n" + "-" * 60
            )

            print(
                "DATABASE RESULT"
            )

            print(
                "-" * 60
            )


            # ------------------------------------------------
            # BASIC INFORMATION
            # ------------------------------------------------

            print(
                f"\nDisease : "
                f"{profile['disease']}"
            )

            print(
                f"Crop    : "
                f"{profile['crop']}"
            )

            print(
                f"Type    : "
                f"{profile['type']}"
            )


            # ------------------------------------------------
            # PATHOGENS
            # ------------------------------------------------

            print(
                "\nCause / Pathogen:"
            )

            for pathogen in profile[
                "pathogens"
            ]:

                scientific_name = pathogen.get(
                    "scientific_name",
                    ""
                )

                pathogen_type = pathogen.get(
                    "type",
                    ""
                )

                role = pathogen.get(
                    "role",
                    ""
                )

                text = scientific_name

                if pathogen_type:

                    text += (
                        f" ({pathogen_type})"
                    )

                if role:

                    text += (
                        f": {role}"
                    )

                print(
                    f"- {text}"
                )


            # ------------------------------------------------
            # SYMPTOMS
            # ------------------------------------------------

            print(
                "\nSymptoms:"
            )

            for symptom in profile[
                "symptoms"
            ]:

                category = symptom.get(
                    "category",
                    ""
                )

                description = symptom.get(
                    "description",
                    ""
                )

                if category:

                    print(
                        f"- [{category}] "
                        f"{description}"
                    )

                else:

                    print(
                        f"- {description}"
                    )


            # ------------------------------------------------
            # TRANSMISSION
            # ------------------------------------------------

            print(
                "\nTransmission:"
            )

            for item in profile[
                "transmission"
            ]:

                method = item.get(
                    "method",
                    ""
                )

                description = item.get(
                    "description",
                    ""
                )

                print(
                    f"- {method}: "
                    f"{description}"
                )


            # ------------------------------------------------
            # FAVOURABLE CONDITIONS
            # ------------------------------------------------

            print(
                "\nFavourable conditions:"
            )

            for condition in profile[
                "conditions"
            ]:

                factor = condition.get(
                    "factor",
                    ""
                )

                value = condition.get(
                    "value",
                    ""
                )

                description = condition.get(
                    "description",
                    ""
                )

                text = factor

                if value:

                    text += (
                        f" ({value})"
                    )

                if description:

                    text += (
                        f": {description}"
                    )

                print(
                    f"- {text}"
                )


            # ------------------------------------------------
            # MANAGEMENT
            # ------------------------------------------------

            print(
                "\nManagement:"
            )

            for item in profile[
                "management"
            ]:

                category = item.get(
                    "category",
                    ""
                )

                action = item.get(
                    "action",
                    ""
                )

                if category:

                    print(
                        f"- [{category}] "
                        f"{action}"
                    )

                else:

                    print(
                        f"- {action}"
                    )


            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            print(
                "\nSources:"
            )

            for source in profile[
                "sources"
            ]:

                organization = source.get(
                    "organization",
                    ""
                )

                title = source.get(
                    "title",
                    ""
                )

                url = source.get(
                    "url",
                    ""
                )

                text = ""

                if organization:

                    text += organization

                if title:

                    text += (
                        f": {title}"
                    )

                if text:

                    print(
                        f"- {text}"
                    )

                if url:

                    print(
                        f"  {url}"
                    )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print(
            "\n" + "=" * 60
        )

        print(
            "CNN → DATABASE INTEGRATION TEST PASSED"
        )

        print(
            "=" * 60
        )


    except Exception as error:

        print(
            "\n" + "=" * 60
        )

        print(
            "CNN → DATABASE INTEGRATION TEST FAILED"
        )

        print(
            "=" * 60
        )

        print(
            "\nError:"
        )

        print(error)

        sys.exit(1)