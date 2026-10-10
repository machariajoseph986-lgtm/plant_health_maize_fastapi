import json
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# ============================================================
# V4 CONFIGURATION
# ============================================================

SEED = 42
IMAGE_SIZE = (320, 320)
BATCH_SIZE = 16
NUM_CLASSES = 6

DATASET_ROOT = Path("../v4_dataset")

CLASS_NAMES = [
    "Northern_Leaf_Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy",
    "Maize_Lethal_Necrosis",
    "Maize_Streak_Virus",
]

TRAIN_DIR = DATASET_ROOT / "train"
VAL_DIR = DATASET_ROOT / "validation"

# V4 class weights calculated from the training split only.
CLASS_WEIGHTS = {
    0: 2.845717,
    1: 2.492726,
    2: 5.691434,
    3: 0.518474,
    4: 0.817965,
    5: 0.520713,
}


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

print("V4 CNN DRY RUN")
print("=" * 80)

print("TensorFlow:", tf.__version__)
print("Keras:", keras.__version__)
print("Seed:", SEED)
print("Image size:", IMAGE_SIZE)
print("Batch size:", BATCH_SIZE)
print("Classes:", NUM_CLASSES)


# ============================================================
# DATASETS
# ============================================================

print("\nLoading datasets...")

train_ds = keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
)

val_ds = keras.utils.image_dataset_from_directory(
    VAL_DIR,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print("\nDetected class names:")
print(train_ds.class_names)

print("\nClass weights:")
for class_id, weight in CLASS_WEIGHTS.items():
    print(f"{class_id}: {CLASS_NAMES[class_id]:25s} -> {weight}")


# ============================================================
# PREPROCESSING
# ============================================================

def mobilenet_preprocess(images, labels):
    images = tf.cast(images, tf.float32)

    # MobileNetV2 preprocess_input:
    # scales pixel values from [0, 255] to [-1, 1]
    images = (images / 127.5) - 1.0

    return images, labels


train_ds = train_ds.map(
    mobilenet_preprocess,
    num_parallel_calls=tf.data.AUTOTUNE,
)

val_ds = val_ds.map(
    mobilenet_preprocess,
    num_parallel_calls=tf.data.AUTOTUNE,
)

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)


# ============================================================
# AUGMENTATION
# ============================================================

augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal", seed=SEED),
        layers.RandomRotation(0.08, seed=SEED),
        layers.RandomZoom(0.10, seed=SEED),
        layers.RandomContrast(0.10, seed=SEED),
    ],
    name="v4_augmentation",
)


# ============================================================
# MODEL
# ============================================================

print("\nBuilding MobileNetV2 model...")

backbone = keras.applications.MobileNetV2(
    input_shape=(*IMAGE_SIZE, 3),
    include_top=False,
    weights="imagenet",
)

# Stage 1: backbone frozen.
backbone.trainable = False

inputs = keras.Input(
    shape=(*IMAGE_SIZE, 3),
    name="image",
)

x = augmentation(inputs)
x = backbone(x, training=False)
x = layers.GlobalAveragePooling2D(name="global_average_pooling2d")(x)
x = layers.Dropout(0.30, name="dropout")(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax",
    name="classifier",
)(x)

model = keras.Model(
    inputs=inputs,
    outputs=outputs,
    name="maize_disease_mobilenetv2_v4",
)


# ============================================================
# COMPILE
# ============================================================

model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=1e-4,
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)


# ============================================================
# MODEL CHECK
# ============================================================

print("\nMODEL SUMMARY")
print("=" * 80)

model.summary()

print("\nTrainable parameters:", model.count_params())

trainable_params = sum(
    np.prod(variable.shape)
    for variable in model.trainable_variables
)

non_trainable_params = sum(
    np.prod(variable.shape)
    for variable in model.non_trainable_variables
)

print("Trainable parameters:", trainable_params)
print("Non-trainable parameters:", non_trainable_params)


# ============================================================
# ONE-BATCH DRY RUN
# ============================================================

print("\nRUNNING ONE-BATCH DRY RUN")
print("=" * 80)

images, labels = next(iter(train_ds))

print("Input batch shape:", images.shape)
print("Label batch shape:", labels.shape)

print(
    "Input range:",
    float(tf.reduce_min(images).numpy()),
    "to",
    float(tf.reduce_max(images).numpy()),
)

print("Labels per batch:")
print(labels.numpy())

print("\nRunning one training batch...")

result = model.train_on_batch(
    images,
    labels,
    return_dict=True,
)

print("\nTraining batch result:")
print(result)

print("\nRunning validation prediction...")

val_images, val_labels = next(iter(val_ds))

predictions = model.predict(
    val_images,
    verbose=0,
)

print("Validation batch input shape:", val_images.shape)
print("Prediction shape:", predictions.shape)
print("Prediction range:", float(predictions.min()), "to", float(predictions.max()))

print("\nProbability sums for first 5 samples:")

for i, row in enumerate(predictions[:5]):
    print(
        f"Sample {i}: "
        f"sum={row.sum():.6f}, "
        f"class={CLASS_NAMES[int(np.argmax(row))]}"
    )


# ============================================================
# SAVE DRY-RUN CONFIGURATION
# ============================================================

config = {
    "seed": SEED,
    "image_size": list(IMAGE_SIZE),
    "batch_size": BATCH_SIZE,
    "num_classes": NUM_CLASSES,
    "class_names": CLASS_NAMES,
    "stage_1_learning_rate": 1e-4,
    "stage_1_max_epochs": 20,
    "stage_2_learning_rate": 2e-6,
    "stage_2_max_epochs": 20,
    "dropout": 0.30,
    "augmentation": {
        "horizontal_flip": True,
        "rotation": 0.08,
        "zoom": 0.10,
        "contrast": 0.10,
    },
    "class_weights": CLASS_WEIGHTS,
}

config_path = Path("training_output/v4_dry_run_config.json")
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print("\nConfiguration saved to:")
print(config_path)

print("\n" + "=" * 80)
print("V4 DRY RUN COMPLETE")
print("=" * 80)
