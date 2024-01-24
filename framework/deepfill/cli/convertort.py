from pathlib import Path

from segment_anything import sam_model_registry,   SamAutomaticMaskGenerator, SamPredictor
from ultralytics import YOLO

import cv2
import numpy as np
from rasterio import features


device = "cuda"
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
class Converter:

    def __init__(self):
        self._sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self._sam.to(device=device)
        self._predictor = SamPredictor(self._sam)

    def show_mask(mask, ax, random_color=False):
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        ax.imshow(mask_image)


    def convert(self,  image_path: Path , model,images_dir_path):

        labels = []
        print(image_path)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = model.predict(image, conf=0.25)
        width, height, _ = image.shape

        boxes = []
        for result in results:
            boxes = result.boxes
        try:
            bbox = boxes.xyxy.tolist()[0]
        except:
            print(f"skip: file {image_path}")
            return [], False

        self._predictor.set_image(image)

        bbox_numpy = np.array(bbox)
        masks, _, _ = self._predictor.predict(
            point_coords=None,
            point_labels=labels,
            box=bbox_numpy,
            multimask_output=True,
        )

        fname = str(image_path).split('/')[-1:][0]

        print(f"{images_dir_path}/mask_{fname}")
        cv2.imwrite(f"{images_dir_path}/mask_{fname}.jpg", np.array(masks[0],  np.uint8))
        return masks[0], True


    def create_label(self,img, label_path):

        img = np.array(img, np.uint8)
        # There may be a better way to do it, but this is what I have found so far
        cords = list(features.shapes(img, mask=(img >0)))[0][0]['coordinates'][0]
        label_line = '0 ' + ' '.join([f'{int(cord[0])/img.shape[0]} {int(cord[1])/img.shape[1]}' for cord in cords])

        label_path.parent.mkdir( parents=True, exist_ok=True )
        with label_path.open('w') as f:
            f.write(label_line)



if __name__ == "__main__":

    converter = Converter()

    model = YOLO("best.pt")

    for images_dir_path in [Path(f'datasets/{x}/images') for x in ['train', 'val', 'test']]:
        for img_path in images_dir_path.iterdir():
            label_path = img_path.parent.parent / 'labels' / f'{img_path.stem}.txt'

            mask, is_valid = converter.convert(str(img_path),model, images_dir_path)
            if not is_valid:
                continue
            converter.create_label(mask, label_path)