"""
CNN → Knowledge Base Mapping

Maps the class indices produced by the trained maize CNN
to the corresponding health-problem IDs in the SQLite
knowledge base.

CNN class mapping verified from train_cnn.py and evaluate_model.py:

    0 → Blight
    1 → Common_Rust
    2 → Gray_Leaf_Spot
    3 → Healthy

Only the three disease classes have knowledge-base records.
Healthy is handled as a non-disease result.
"""


# ============================================================
# VERIFIED CNN CLASS MAPPING
# ============================================================

CLASS_NAMES = [
    "Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy"
]


# ============================================================
# CNN CLASS → KNOWLEDGE BASE MAPPING
# ============================================================

CNN_TO_KB = {
    0: "HP_MAIZE_BLIGHT",
    1: "HP_MAIZE_COMMON_RUST",
    2: "HP_MAIZE_GRAY_LEAF_SPOT",
    3: None
}


# ============================================================
# CLASS NAME → KNOWLEDGE BASE MAPPING
# ============================================================

CLASS_NAME_TO_KB = {
    "Blight": "HP_MAIZE_BLIGHT",
    "Common_Rust": "HP_MAIZE_COMMON_RUST",
    "Gray_Leaf_Spot": "HP_MAIZE_GRAY_LEAF_SPOT",
    "Healthy": None
}


# ============================================================
# GET CLASS NAME
# ============================================================

def get_class_name(class_index):
    """
    Return the CNN class name for a class index.
    """

    if class_index < 0 or class_index >= len(CLASS_NAMES):
        raise ValueError(
            f"Invalid CNN class index: {class_index}"
        )

    return CLASS_NAMES[class_index]


# ============================================================
# GET KNOWLEDGE BASE ID
# ============================================================

def get_knowledge_base_id(class_index):
    """
    Return the SQLite health_problem_id corresponding
    to a CNN class index.

    Returns None for Healthy because Healthy is not
    a disease record in the knowledge base.
    """

    if class_index not in CNN_TO_KB:
        raise ValueError(
            f"Invalid CNN class index: {class_index}"
        )

    return CNN_TO_KB[class_index]


# ============================================================
# GET COMPLETE MAPPING
# ============================================================

def get_prediction_mapping(class_index):
    """
    Return the complete mapping information for a
    CNN prediction.
    """

    class_name = get_class_name(class_index)
    health_problem_id = get_knowledge_base_id(class_index)

    return {
        "class_index": class_index,
        "class_name": class_name,
        "health_problem_id": health_problem_id,
        "is_healthy": class_name == "Healthy"
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CNN → KNOWLEDGE BASE MAPPING TEST")
    print("=" * 60)

    print("\nVerified CNN classes:\n")

    for class_index, class_name in enumerate(CLASS_NAMES):

        health_problem_id = CNN_TO_KB[class_index]

        print(
            f"{class_index}: "
            f"{class_name:<20} → "
            f"{health_problem_id}"
        )

    print("\nDetailed mapping:\n")

    for class_index in range(len(CLASS_NAMES)):

        result = get_prediction_mapping(class_index)

        print(result)

    print("\nMapping test completed successfully.")
    print("=" * 60)