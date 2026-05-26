"""Disease Detection training — MobileNetV2 with augmentation + fine-tuning.

Usage:
  1. Download PlantVillage from https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
  2. Extract into: datasets/plantvillage/  (subfolders per class)
  3. Run: python -m ai_engine.disease_detection.train
"""

import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ── Config ──────────────────────────────────────────────────────────────────
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_FEATURE_EXTRACTION = 15
EPOCHS_FINETUNE = 10
FINETUNE_LEARNING_RATE = 1e-5
MODEL_DIR = Path(__file__).parent / "models"
LOCAL_DATA_DIR = Path(__file__).parent.parent.parent / "datasets" / "plantvillage"

os.makedirs(MODEL_DIR, exist_ok=True)


def build_model(num_classes: int) -> tf.keras.Model:
    """Build MobileNetV2 with frozen base + new classification head."""
    base = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    inputs = keras.Input(shape=(*IMG_SIZE, 3))
    x = layers.RandomFlip("horizontal_and_vertical")(inputs)
    x = layers.RandomRotation(0.15)(x)
    x = layers.RandomZoom(0.1)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    return model


def train():
    print("TensorFlow:", tf.__version__)
    print("GPU available:", tf.config.list_physical_devices("GPU"))

    # ── Load dataset ────────────────────────────────────────────────────────
    if LOCAL_DATA_DIR.exists() and any(LOCAL_DATA_DIR.iterdir()):
        print(f"Loading dataset from {LOCAL_DATA_DIR}...")
        train_ds = keras.preprocessing.image_dataset_from_directory(
            str(LOCAL_DATA_DIR),
            validation_split=0.2,
            subset="training",
            seed=42,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="int",
        )
        val_ds = keras.preprocessing.image_dataset_from_directory(
            str(LOCAL_DATA_DIR),
            validation_split=0.2,
            subset="validation",
            seed=42,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="int",
        )
        class_names = train_ds.class_names
        num_classes = len(class_names)
        print(f"Classes ({num_classes}): {class_names}")
    else:
        print(f"No dataset found at {LOCAL_DATA_DIR}")
        print(f"Download PlantVillage from Kaggle and extract to: {LOCAL_DATA_DIR}")
        return

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    # ── Phase 1: Feature extraction ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Phase 1: Feature extraction (frozen MobileNetV2)")
    print("=" * 60)

    model = build_model(num_classes)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.summary()

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_FEATURE_EXTRACTION,
        verbose=1,
    )

    val_acc = max(history.history["val_accuracy"])
    print(f"\nBest validation accuracy after feature extraction: {val_acc:.2%}")

    # ── Phase 2: Fine-tuning ────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Phase 2: Fine-tuning (unfreeze last 30 layers)")
    print("=" * 60)

    # Unfreeze the base model
    base = model.get_layer("mobilenetv2_1.00_224")
    base.trainable = True

    # Freeze early layers, only fine-tune the last 30
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=FINETUNE_LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_ft = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_FINETUNE,
        verbose=1,
    )

    val_acc_ft = max(history_ft.history["val_accuracy"])
    print(f"\nBest validation accuracy after fine-tuning: {val_acc_ft:.2%}")

    # ── Save ────────────────────────────────────────────────────────────────
    model_path = MODEL_DIR / "mobilenetv2_plantvillage.h5"
    model.save(str(model_path))
    print(f"\nModel saved: {model_path} ({os.path.getsize(model_path) / 1e6:.1f} MB)")

    class_path = MODEL_DIR / "class_names.txt"
    with open(class_path, "w") as f:
        f.write("\n".join(class_names))
    print(f"Class names saved: {class_path}")

    print("\n✅ Training complete!")
    print(f"   - Classes: {num_classes}")
    print(f"   - Feature extraction accuracy: {val_acc:.2%}")
    print(f"   - Fine-tuned accuracy: {val_acc_ft:.2%}")
    return model


if __name__ == "__main__":
    train()
