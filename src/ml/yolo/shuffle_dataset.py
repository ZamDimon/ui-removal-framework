import os
import random
import shutil

dataset_dir = "../datasets/prepared"
train_dir = "../datasets/helpers/data/data/train"
val_dir = "../datasets/helpers/data/data/val"

shutil.rmtree(train_dir, ignore_errors=True)
shutil.rmtree(val_dir, ignore_errors=True)
os.makedirs(train_dir)
os.makedirs(val_dir)

images = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if os.path.join(dataset_dir, f).endswith(".jpg")]
val_indexes = random.sample(range(0, len(images) - 1), round(len(images) * 0.2))
for i, img in enumerate(images):
    filename, ext = img.split(".")

    if i in val_indexes:
        shutil.copy2(img, val_dir)
        shutil.copy2(f"{filename}.txt", val_dir)
        print(f"{img} copied to {val_dir}")
    else:
        shutil.copy2(img, train_dir)
        shutil.copy2(f"{filename}.txt", train_dir)
        print(f"{img} copied to {train_dir}")
