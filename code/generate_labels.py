import os
import csv
import random

root = "../dataset"

output_rows = []

for split in ["Train", "Test"]:
    split_path = os.path.join(root, split)

    for folder in os.listdir(split_path):
        class_path = os.path.join(split_path, folder)
        if not os.path.isdir(class_path):
            continue

        if folder.startswith("fresh"):
            freshness = random.uniform(85, 100)
        elif folder.startswith("rotten"):
            freshness = random.uniform(0, 40)
        else:
            continue

        for img in os.listdir(class_path):
            img_path = os.path.join(split, folder, img)
            output_rows.append([img_path, folder, round(freshness, 2)])

with open("../labels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["image", "category", "freshness"])
    writer.writerows(output_rows)

print("labels.csv created successfully!")
