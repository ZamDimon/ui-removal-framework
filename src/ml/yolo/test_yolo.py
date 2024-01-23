import os

import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO


model = YOLO('../datasets/helpers/runs/detect/uis5/weights/best.pt')

test_path = "../datasets/images"



for file in os.listdir(test_path):
    image = Image.open(f"{test_path}/{file}")
    results = model(image)

    w, h = image.size
    mask = np.zeros((h, w, 3), dtype=np.uint8)
    mask = Image.fromarray(mask)
    boxes = []
    draw = ImageDraw.Draw(mask, "RGBA")
    for result in results:
        boxes = result.boxes
        for box in boxes:
            b = box.xyxy[0]
            draw.rectangle(((b[0], b[1]), (b[2], b[3])), fill=(255, 255, 255, 255))

        print(boxes.xyxy.tolist())
        im_array = result.plot()  
        im = Image.fromarray(im_array[..., ::-1])

        im.save(f"{test_path}/new_{file}")

    mask.save(f"{test_path}/mask_{file}")



