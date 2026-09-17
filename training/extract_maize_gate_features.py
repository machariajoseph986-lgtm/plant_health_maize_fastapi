from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

MODEL_PATH = Path("training_output/v3/best_maize_disease_mobilenetv2_v3_finetuned.keras")
DATA_ROOT = Path("data/maize_gate/split")
OUTPUT_ROOT = Path("training_output/maize_gate_features")

IMAGE_SIZE = (320, 320)
BATCH_SIZE = 16

CLASS_MAP = {
    "positive": 1,
    "negative": 0,
}


def build_feature_extractor():
    model = load_model(MODEL_PATH, compile=False)
    feature_layer = model.get_layer("global_average_pooling2d")
    return tf.keras.Model(
        inputs=model.input,
        outputs=feature_layer.output,
    )


def collect_images(split):
    records = []

    split_dir = DATA_ROOT / split

    for class_name, label in CLASS_MAP.items():
        class_dir = split_dir / class_name

        for path in sorted(class_dir.iterdir()):
            if path.is_file() and path.suffix.lower() in {
                ".jpg", ".jpeg", ".png", ".webp"
            }:
                records.append((path, label))

    return records


def load_image(path):
    image = tf.io.read_file(str(path))
    image = tf.image.decode_image(
        image,
        channels=3,
        expand_animations=False,
    )
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.cast(image, tf.float32)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)         
    return image


def extract_split(extractor, split):
    records = collect_images(split)

    print(f"{split}: {len(records)} images")

    features = []
    labels = []

    for start in range(0, len(records), BATCH_SIZE):
        batch_records = records[start:start + BATCH_SIZE]

        batch_images = tf.stack([
            load_image(path)
            for path, _ in batch_records
        ])

        batch_features = extractor.predict(
            batch_images,
            verbose=0,
        )

        features.append(batch_features.astype(np.float32))
        labels.extend(label for _, label in batch_records)

        print(
            f"  processed {min(start + BATCH_SIZE, len(records))}"
            f"/{len(records)}",
            end="\r",
        )

    print()

    return (
        np.concatenate(features, axis=0),
        np.asarray(labels, dtype=np.int32),
    )


def main():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    extractor = build_feature_extractor()

    print("Feature extractor output shape:", extractor.output_shape)

    for split in ("train", "val", "test"):
        features, labels = extract_split(extractor, split)

        output_path = OUTPUT_ROOT / f"{split}.npz"

        np.savez_compressed(
            output_path,
            features=features,
            labels=labels,
        )

        print(
            f"Saved {output_path}: "
            f"features={features.shape}, "
            f"labels={labels.shape}"
        )


if __name__ == "__main__":
    main()
