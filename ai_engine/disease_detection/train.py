"""Disease Detection training — MobileNetV2 feature extraction on PlantVillage."""

import os
import sys
import tarfile
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ---- Config ----
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 38  # PlantVillage has 38 disease classes
MODEL_DIR = Path(__file__).parent / "models"
DATASET_DIR = Path(__file__).parent.parent.parent / "datasets" / "plantvillage"

os.makedirs(MODEL_DIR, exist_ok=True)


def download_plantvillage(target_dir: Path) -> bool:
    """Download PlantVillage dataset archive."""
    url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    archive_path = target_dir / "plantvillage.tgz"
    os.makedirs(target_dir, exist_ok=True)

    if not archive_path.exists():
        print("Downloading sample dataset (for demo — use real PlantVillage for production)...")
        tf.keras.utils.get_file(archive_path, url, cache_dir=str(target_dir), cache_subdir=".")
        return True

    print("Dataset already downloaded.")
    return False


def build_model() -> tf.keras.Model:
    """Build MobileNetV2 with frozen base + new classification head."""
    base = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False  # Freeze — feature extraction only

    inputs = keras.Input(shape=(*IMG_SIZE, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train():
    print("TensorFlow version:", tf.__version__)
    print("Building MobileNetV2 model...")
    model = build_model()
    model.summary()

    # Check for real PlantVillage data, use sample if not available
    if DATASET_DIR.exists() and any(DATASET_DIR.iterdir()):
        print(f"Loading dataset from {DATASET_DIR}...")
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            str(DATASET_DIR),
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
        )
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            str(DATASET_DIR),
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
        )
    else:
        print(f"PlantVillage dataset not found at {DATASET_DIR}.")
        print("Using synthetic data for demonstration — train with real data for production.")
        # Create synthetic dataset for testing the pipeline
        num_samples = 100
        x_train = np.random.rand(num_samples, *IMG_SIZE, 3).astype(np.float32)
        y_train = tf.keras.utils.to_categorical(np.random.randint(0, NUM_CLASSES, num_samples), NUM_CLASSES)
        x_val = np.random.rand(20, *IMG_SIZE, 3).astype(np.float32)
        y_val = tf.keras.utils.to_categorical(np.random.randint(0, NUM_CLASSES, 20), NUM_CLASSES)
        train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(BATCH_SIZE)
        val_ds = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(BATCH_SIZE)
        print("*** TRAINING ON SYNTHETIC DATA — MODEL WILL NOT PREDICT REAL DISEASES ***")
        print(f"    Place real PlantVillage images in: {DATASET_DIR}")

    print("Training...")
    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

    model_path = MODEL_DIR / "mobilenetv2_plantvillage.h5"
    model.save(str(model_path))
    print(f"Model saved to {model_path}")

    # Save class names
    class_path = MODEL_DIR / "class_names.txt"
    if DATASET_DIR.exists() and any(DATASET_DIR.iterdir()):
        class_names = sorted(d.name for d in DATASET_DIR.iterdir() if d.is_dir())
    else:
        class_names = [f"class_{i}" for i in range(NUM_CLASSES)]
    with open(class_path, "w") as f:
        f.write("\n".join(class_names))
    print(f"Class names saved to {class_path}")

    val_acc = max(history.history["val_accuracy"])
    print(f"Validation accuracy: {val_acc:.2%}")
    return model


if __name__ == "__main__":
    train()
