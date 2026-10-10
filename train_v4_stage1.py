import json
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# ============================================================
# V4 STAGE 1 CONFIGURATION
# ============================================================

SEED = 42
IMAGE_SIZE = (320, 320)
BATCH_SIZE = 16
NUM_CLASSES = 6
MAX_EPOCHS = 20

DATASET_ROOT = Path("../v4_dataset")

TRAIN_DIR = DATASET_ROOT / "train"
VAL_DIR = DATASET_ROOT / "validation"

OUTPUT_DIR = Path("training_output/v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = OUTPUT_DIR / "stage1_best.keras"
FINAL_MODEL_PATH = OUTPUT_DIR / "stage1_final.keras"
HISTORY_PATH = OUTPUT_DIR / "stage1_history.json"
CONFIG_PATH = OUTPUT_DIR / "stage1_config.json"
CSV_LOG_PATH = OUTPUT_DIR / "stage1_training.csv"

CLASS_NAMES = [
    "Northern_Leaf_Blight",
    "Common_Rust",
    "Gray_Leaf_Spot",
    "Healthy",
    "Maize_Lethal_Necrosis",
    "Maize_Streak_Virus",
]

# Calculated from the V4 TRAINING split only.
CLASS_WEIGHTS = {
    0: 2.845717,
    1: 2.492726,
    2: 5.691434,
    3: 0.518474,
    4: 0.817965,
    5: 0.520713,
}

STAGE1_LEARNING_RATE = 1e-4


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


# ============================================================
# INFORMATION
# ============================================================

print("=" * 80)
print("MAIZE DISEASE CNN V4 — STAGE 1 TRAINING")
print("=" * 80)

print("TensorFlow:", tf.__version__)
print("Keras:", keras.__version__)
print("Seed:", SEED)
print("Image size:", IMAGE_SIZE)
print("Batch size:", BATCH_SIZE)
print("Maximum epochs:", MAX_EPOCHS)
print("Learning rate:", STAGE1_LEARNING_RATE)
print("Classes:", NUM_CLASSES)

print("\nOutput directory:")
print(OUTPUT_DIR)


# ============================================================
# DATASETS
# ============================================================

print("\n" + "=" * 80)
print("LOADING DATASETS")
print("=" * 80)

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

print("\nDetected classes:")
for i, name in enumerate(train_ds.class_names):
    print(f"{i}: {name}")


# ============================================================
# PREPROCESSING
# ============================================================

def mobilenet_preprocess(images, labels):
    images = tf.cast(images, tf.float32)
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


# ============================================================
# PERFORMANCE PIPELINE
# ============================================================

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)


# ============================================================
# AUGMENTATION
# ============================================================

augmentation = keras.Sequential(
    [
        layers.RandomFlip(
            "horizontal",
            seed=SEED,
        ),
        layers.RandomRotation(
            0.08,
            seed=SEED,
        ),
        layers.RandomZoom(
            0.10,
            seed=SEED,
        ),
        layers.RandomContrast(
            0.10,
            seed=SEED,
        ),
    ],
    name="v4_augmentation",
)


# ============================================================
# MODEL
# ============================================================

print("\n" + "=" * 80)
print("BUILDING MODEL")
print("=" * 80)

backbone = keras.applications.MobileNetV2(
    input_shape=(*IMAGE_SIZE, 3),
    include_top=False,
    weights="imagenet",
)

# Stage 1:
# Keep the complete pretrained feature extractor frozen.
backbone.trainable = False

inputs = keras.Input(
    shape=(*IMAGE_SIZE, 3),
    name="image",
)

x = augmentation(inputs)

x = backbone(
    x,
    training=False,
)

x = layers.GlobalAveragePooling2D(
    name="global_average_pooling2d",
)(x)

x = layers.Dropout(
    0.30,
    name="dropout",
)(x)

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
        learning_rate=STAGE1_LEARNING_RATE,
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)


# ============================================================
# PARAMETER REPORT
# ============================================================

total_params = model.count_params()

trainable_params = sum(
    np.prod(variable.shape)
    for variable in model.trainable_variables
)

non_trainable_params = sum(
    np.prod(variable.shape)
    for variable in model.non_trainable_variables
)

print("\nParameter counts:")
print(f"Total:           {total_params:,}")
print(f"Trainable:       {trainable_params:,}")
print(f"Non-trainable:   {non_trainable_params:,}")


# ============================================================
# CONFIGURATION RECORD
# ============================================================

config = {
    "experiment": "Maize Disease CNN V4",
    "stage": 1,
    "seed": SEED,
    "tensorflow_version": tf.__version__,
    "keras_version": keras.__version__,
    "image_size": list(IMAGE_SIZE),
    "batch_size": BATCH_SIZE,
    "num_classes": NUM_CLASSES,
    "class_names": CLASS_NAMES,
    "max_epochs": MAX_EPOCHS,
    "learning_rate": STAGE1_LEARNING_RATE,
    "optimizer": "Adam",
    "loss": "categorical_crossentropy",
    "dropout": 0.30,
    "backbone": "MobileNetV2",
    "weights": "ImageNet",
    "include_top": False,
    "backbone_trainable": False,
    "preprocessing": "MobileNetV2: (pixel / 127.5) - 1.0",
    "augmentation": {
        "horizontal_flip": True,
        "rotation": 0.08,
        "zoom": 0.10,
        "contrast": 0.10,
    },
    "class_weights": {
        CLASS_NAMES[int(k)]: float(v)
        for k, v in CLASS_WEIGHTS.items()
    },
    "total_parameters": int(total_params),
    "trainable_parameters": int(trainable_params),
    "non_trainable_parameters": int(non_trainable_params),
}

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)


# ============================================================
# CALLBACKS
# ============================================================

checkpoint = keras.callbacks.ModelCheckpoint(
    filepath=str(BEST_MODEL_PATH),
    monitor="val_loss",
    mode="min",
    save_best_only=True,
    verbose=1,
)

early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    mode="min",
    patience=4,
    restore_best_weights=True,
    verbose=1,
)

csv_logger = keras.callbacks.CSVLogger(
    str(CSV_LOG_PATH),
    append=False,
)


# ============================================================
# STAGE 1 TRAINING
# ============================================================

print("\n" + "=" * 80)
print("STARTING STAGE 1 TRAINING")
print("=" * 80)

print("Backbone: FROZEN")
print("Classification head: TRAINABLE")
print("Maximum epochs:", MAX_EPOCHS)
print("Early stopping patience:", 4)
print("\nTraining is starting now...\n")

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
    verbose=1,
)


# ============================================================
# SAVE FINAL STAGE 1 MODEL
# ============================================================

model.save(FINAL_MODEL_PATH)


# ============================================================
# SAVE HISTORY
# ============================================================

history_data = {
    key: [float(value) for value in values]
    for key, values in history.history.items()
}

with open(HISTORY_PATH, "w", encoding="utf-8") as f:
    json.dump(history_data, f, indent=2)


# ============================================================
# FINAL REPORT
# ============================================================

epochs_completed = len(history.history["loss"])

best_epoch = (
    int(np.argmin(history.history["val_loss"])) + 1
)

best_val_loss = float(
    min(history.history["val_loss"])
)

best_val_accuracy = float(
    history.history["val_accuracy"][best_epoch - 1]
)

final_train_loss = float(
    history.history["loss"][-1]
)

final_train_accuracy = float(
    history.history["accuracy"][-1]
)

print("\n" + "=" * 80)
print("STAGE 1 TRAINING COMPLETE")
print("=" * 80)

print("Epochs completed:", epochs_completed)
print("Best epoch:", best_epoch)
print("Best validation loss:", best_val_loss)
print("Validation accuracy at best epoch:", best_val_accuracy)
print("Final training loss:", final_train_loss)
print("Final training accuracy:", final_train_accuracy)

print("\nSaved files:")
print("Best model:", BEST_MODEL_PATH)
print("Final model:", FINAL_MODEL_PATH)
print("History:", HISTORY_PATH)
print("CSV log:", CSV_LOG_PATH)
print("Configuration:", CONFIG_PATH)

print("\n" + "=" * 80)
print("STAGE 1 READY FOR EVALUATION")
print("=" * 80)
