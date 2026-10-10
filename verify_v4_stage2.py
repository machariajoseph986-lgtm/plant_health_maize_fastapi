import json
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# ============================================================
# V4 STAGE 2 FINE-TUNING
# ============================================================

SEED = 42
IMAGE_SIZE = (320, 320)
BATCH_SIZE = 16
NUM_CLASSES = 6
MAX_EPOCHS = 20

DATASET_ROOT = Path("../v4_dataset")
OUTPUT_DIR = Path("training_output/v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STAGE1_MODEL = OUTPUT_DIR / "stage1_best.keras"

CLASS_NAMES = [
    "Northern_Leaf_Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy",
    "Maize_Lethal_Necrosis",
    "Maize_Streak_Virus",
]

CLASS_WEIGHTS = {
    0: 2.845717,
    1: 2.492726,
    2: 5.691434,
    3: 0.518474,
    4: 0.817965,
    5: 0.520713,
}

STAGE2_LEARNING_RATE = 2e-6
FINE_TUNE_START = 116


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


# ============================================================
# DATASETS
# ============================================================

train_dir = DATASET_ROOT / "train"
val_dir = DATASET_ROOT / "validation"

train_ds = keras.utils.image_dataset_from_directory(
    train_dir,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=SEED,
)

val_ds = keras.utils.image_dataset_from_directory(
    val_dir,
    labels="inferred",
    label_mode="categorical",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)


# ============================================================
# PREPROCESSING
# ============================================================

def preprocess(images, labels):
    images = tf.cast(images, tf.float32)
    images = (images / 127.5) - 1.0
    return images, labels


train_ds = train_ds.map(
    preprocess,
    num_parallel_calls=tf.data.AUTOTUNE,
)

val_ds = val_ds.map(
    preprocess,
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
# LOAD STAGE 1 MODEL
# ============================================================

model = keras.models.load_model(STAGE1_MODEL)

backbone = next(
    layer
    for layer in model.layers
    if layer.name.startswith("mobilenetv2")
)


# ============================================================
# STAGE 2 TRAINABILITY
# ============================================================

for i, layer in enumerate(backbone.layers):
    if i < FINE_TUNE_START:
        layer.trainable = False
    else:
        layer.trainable = True

    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

# Keep the nested layer trainability settings established above.
# Do NOT reset backbone.trainable here, because that would re-enable all nested layers.

# Keep the classifier trainable.
model.get_layer("classifier").trainable = True


# ============================================================
# COMPILE
# ============================================================

optimizer = keras.optimizers.Adam(
    learning_rate=STAGE2_LEARNING_RATE
)

model.compile(
    optimizer=optimizer,
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)


# ============================================================
# VERIFY TRAINABILITY BEFORE TRAINING
# ============================================================

trainable_internal = [
    (i, layer.name, type(layer).__name__)
    for i, layer in enumerate(backbone.layers)
    if layer.trainable
]

trainable_bn = [
    (i, layer.name)
    for i, layer in enumerate(backbone.layers)
    if isinstance(layer, layers.BatchNormalization)
    and layer.trainable
]

print("\n=== V4 STAGE 2 TRAINABILITY CHECK ===")
print("Backbone:", backbone.name)
print("Internal layers:", len(backbone.layers))
print("Layer 115:", backbone.layers[115].name,
      "trainable=", backbone.layers[115].trainable)
print("Layer 116:", backbone.layers[116].name,
      "trainable=", backbone.layers[116].trainable)
print("BatchNorm layers:", sum(
    isinstance(layer, layers.BatchNormalization)
    for layer in backbone.layers
))
print("Trainable backbone layers:", len(trainable_internal))
print("Trainable BatchNorm layers:", len(trainable_bn))
print("First trainable internal layer:", trainable_internal[0])
print("Last trainable internal layer:", trainable_internal[-1])
print("Classifier trainable:", model.get_layer("classifier").trainable)
print("Learning rate:", STAGE2_LEARNING_RATE)


raise SystemExit("VERIFICATION ONLY - TRAINING NOT STARTED")

# ============================================================
# CALLBACKS
# ============================================================

best_path = OUTPUT_DIR / "stage2_best.keras"
final_path = OUTPUT_DIR / "stage2_final.keras"
history_path = OUTPUT_DIR / "stage2_history.json"
config_path = OUTPUT_DIR / "stage2_config.json"
csv_path = OUTPUT_DIR / "stage2_training.csv"

checkpoint = keras.callbacks.ModelCheckpoint(
    best_path,
    monitor="val_loss",
    save_best_only=True,
    mode="min",
    verbose=1,
)

early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=4,
    mode="min",
    restore_best_weights=True,
    verbose=1,
)

csv_logger = keras.callbacks.CSVLogger(
    csv_path,
    append=False,
)


# ============================================================
# CONFIG
# ============================================================

config = {
    "stage": "V4 Stage 2 fine-tuning",
    "seed": SEED,
    "image_size": list(IMAGE_SIZE),
    "batch_size": BATCH_SIZE,
    "num_classes": NUM_CLASSES,
    "class_names": CLASS_NAMES,
    "dataset_root": str(DATASET_ROOT),
    "starting_model": str(STAGE1_MODEL),
    "backbone": backbone.name,
    "fine_tune_start": FINE_TUNE_START,
    "frozen_internal_layers": "0-115",
    "candidate_trainable_internal_layers": "116-153",
    "batch_normalization_frozen": True,
    "learning_rate": STAGE2_LEARNING_RATE,
    "optimizer": "Adam",
    "loss": "categorical_crossentropy",
    "augmentation": [
        "RandomFlip(horizontal)",
        "RandomRotation(0.08)",
        "RandomZoom(0.10)",
        "RandomContrast(0.10)",
    ],
    "class_weights": {
        str(k): v for k, v in CLASS_WEIGHTS.items()
    },
    "max_epochs": MAX_EPOCHS,
    "early_stopping": {
        "monitor": "val_loss",
        "patience": 4,
        "restore_best_weights": True,
    },
    "checkpoint": {
        "monitor": "val_loss",
        "save_best_only": True,
    },
}

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)


# ============================================================
# TRAIN
# ============================================================

print("\n=== STARTING V4 STAGE 2 TRAINING ===")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=MAX_EPOCHS,
    class_weight=CLASS_WEIGHTS,
    callbacks=[
        checkpoint,
        early_stopping,
        csv_logger,
    ],
)


# ============================================================
# SAVE FINAL MODEL
# ============================================================

model.save(final_path)


# ============================================================
# SAVE HISTORY
# ============================================================

history_data = {
    key: [float(value) for value in values]
    for key, values in history.history.items()
}

with open(history_path, "w", encoding="utf-8") as f:
    json.dump(history_data, f, indent=2)


# ============================================================
# SUMMARY
# ============================================================

val_losses = history_data["val_loss"]
best_epoch = int(np.argmin(val_losses)) + 1
best_val_loss = float(val_losses[best_epoch - 1])
best_val_accuracy = float(
    history_data["val_accuracy"][best_epoch - 1]
)

print("\n=== V4 STAGE 2 COMPLETE ===")
print("Epochs completed:", len(history_data["loss"]))
print("Best epoch:", best_epoch)
print("Best val loss:", best_val_loss)
print("Best val accuracy:", best_val_accuracy)
print("Best model:", best_path)
print("Final model:", final_path)
print("History:", history_path)
print("Config:", config_path)
print("CSV log:", csv_path)
