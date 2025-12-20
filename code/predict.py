import argparse
from tensorflow.keras.models import load_model
from utils import preprocess_image
from decay import compute_all_decay
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("fruit")
args = parser.parse_args()

model = load_model("../model.h5")

# Predict Initial Freshness
img = preprocess_image(args.image)
initial = model.predict(img)[0][0]
initial = max(0, min(round(initial, 2), 100))

# Apply decay
decay = compute_all_decay(initial, args.fruit.lower(), date.today())

print("\n--- FRESHNESS REPORT ---")
print(f"Fruit: {args.fruit}")
print(f"\nInitial Freshness: {initial}%")

print(f"\nCurrent Freshness (Ideal): {decay['ideal_final']}%")
print(f"Current Freshness (Room): {decay['room_final']}%")
print(f"Current Freshness (High Humidity): {decay['humid_final']}%")

print("\nIDEAL STORAGE CONDITIONS:")
print(f"   Estimated Edible Days Left: {decay['ideal_days_left']} days")

print("\nNORMAL ROOM CONDITIONS:")
print(f"   Estimated Edible Days Left: {decay['room_days_left']} days")

print("\nHIGH HUMIDITY CONDITIONS:")
print(f"   Estimated Edible Days Left: {decay['humid_days_left']} days")

status = (
    "FRESH" if decay["room_final"] > 70 else
    "CONSUME SOON" if decay["room_final"] > 40 else
    "SPOILED"
)

print(f"\nFinal Status: {status}")
