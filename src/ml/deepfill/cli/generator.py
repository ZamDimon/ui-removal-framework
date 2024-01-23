import os
from datetime import datetime
from pathlib import Path

from PIL import Image,ImageDraw
import random
from os import listdir
from os.path import isfile, join


class DatasetGenerator:
    def __init__(self,  ui_list: list[str], ui_count: int):
        self._ui_list = ui_list
        self._ui_count = ui_count

    def generate(self, image, filename, dataset_path):

        image = Image.open(image)
        w, h = image.size
        labels = ""
        ui_count = random.randint(1, self._ui_count)

        for n in range(ui_count):
            ui = Image.open(random.choice(self._ui_list))
            ui_w,  ui_h = ui.size

            x = random.randint(0, w)
            y = random.randint(0, h)

            labels += f"0 {((ui_w/2 + x))/w} {((ui_h/2+y))/h} {ui_w/w} {ui_h/h}\n"
            ui = ui.convert("RGBA")
            image.paste(ui, (x, y), ui)
        with open(f"{dataset_path}/{os.path.splitext(os.path.basename(filename))[0]}.txt", 'w') as f:
            f.write(labels)

        image.save(f"{dataset_path}/{filename}")


if __name__ == "__main__":

    ui_path = "../datasets/ui/"
    ui_items = [join(ui_path, f) for f in listdir(ui_path)]

    image_path = "../datasets/images/"

    images_items = [f for f in listdir(image_path)]

    generator = DatasetGenerator(ui_items, 6)
    dataset_path = "../datasets/prepared"
    for path in images_items:
        generator.generate(join(image_path, path), path,dataset_path)
