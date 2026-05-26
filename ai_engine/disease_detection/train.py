"""Disease Detection training — MobileNetV2 with augmentation + fine-tuning."""

import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

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


def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)
    image = tf.image.random_brightness(image, 0.15)
    image = tf.image.random_contrast(image, 0.9, 1.1)
    return image, label


def preprocess(image, label):
    """MobileNetV2 preprocessing: scale [0,255] -> [-1,1]"""
    return (image / 127.5) - 1.0, label


def build_model(num_classes: int) -> tf.keras.Model:
    base = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    inputs = keras.Input(shape=(*IMG_SIZE, 3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return keras.Model(inputs, outputs)


def train():
    print("TensorFlow:", tf.__version__)
    print("GPU available:", tf.config.list_physical_devices("GPU"))

    if not (LOCAL_DATA_DIR.exists() and any(LOCAL_DATA_DIR.iterdir())):
        print(f"No dataset found at {LOCAL_DATA_DIR}")
        return

    print(f"Loading dataset from {LOCAL_DATA_DIR}...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        str(LOCAL_DATA_DIR),
        validation_split=0.2, subset="training", seed=42,
        image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="int",
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        str(LOCAL_DATA_DIR),
        validation_split=0.2, subset="validation", seed=42,
        image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="int",
    )
    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f"Classes ({num_classes}): {class_names}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.map(augment, num_parallel_calls=AUTOTUNE).map(preprocess, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
    val_ds = val_ds.map(preprocess, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)

    # ── Phase 1 ──────────────────────────────────────────────────────────────
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

    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_FEATURE_EXTRACTION, verbose=1)
    val_acc = max(history.history["val_accuracy"])
    print(f"\nBest validation accuracy after feature extraction: {val_acc:.2%}")

    # ── Phase 2 ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Phase 2: Fine-tuning (unfreeze last 30 layers)")
    print("=" * 60)

    base = model.get_layer("mobilenetv2_1.00_224")
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=FINETUNE_LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_ft = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_FINETUNE, verbose=1)
    val_acc_ft = max(history_ft.history["val_accuracy"])
    print(f"\nBest validation accuracy after fine-tuning: {val_acc_ft:.2%}")

    # ── Save ─────────────────────────────────────────────────────────────────
    # Save in modern .keras format (portable across TF versions)
    keras_path = MODEL_DIR / "mobilenetv2_plantvillage.keras"
    model.save(str(keras_path))
    print(f"\nModel saved (.keras): {keras_path} ({os.path.getsize(keras_path) / 1e6:.1f} MB)")

    # Also save just weights as backup
    weights_path = MODEL_DIR / "mobilenetv2_plantvillage.weights.h5"
    model.save_weights(str(weights_path))
    print(f"Weights saved: {weights_path}")

    class_path = MODEL_DIR / "class_names.txt"
    class_path.write_text("\n".join(class_names))
    print(f"Class names saved: {class_path}")

    print(f"\n✅ Training complete! Classes: {num_classes} | FE acc: {val_acc:.2%} | FT acc: {val_acc_ft:.2%}")
    return model


if __name__ == "__main__":
    train()
