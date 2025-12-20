import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Load labels
df = pd.read_csv("../labels.csv")

# Add full image path
df["full_path"] = df["image"].apply(lambda x: os.path.join("../dataset", x))

# Data augmentation (TRAIN ONLY)
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.7, 1.3],
    zoom_range=0.2,
    shear_range=0.1,
    horizontal_flip=True,
    fill_mode="nearest"
)

# Generator
train_generator = datagen.flow_from_dataframe(
    dataframe=df,
    x_col="full_path",
    y_col="freshness",
    target_size=(224, 224),
    batch_size=4,          # 🔴 VERY IMPORTANT (LOW MEMORY)
    class_mode="raw"
)

# Model
base = MobileNetV2(weights="imagenet", include_top=False)
base.trainable = False

x = GlobalAveragePooling2D()(base.output)
x = Dense(128, activation="relu")(x)
output = Dense(1)(x)

model = Model(inputs=base.input, outputs=output)
model.compile(optimizer="adam", loss="mse")

# Train
model.fit(
    train_generator,
    epochs=15
)

model.save("../model.h5")
print("✅ Model trained and saved as model.h5")
