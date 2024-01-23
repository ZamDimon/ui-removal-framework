import logging
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageDraw
from pathlib import Path
import torch
import torchvision.transforms as T


class Cleaner:
    UINT8_VALUE_RANGE = 255

    def __init__(self, cleaner_model_path: Path, yolo_model_path: Path, logger: logging.Logger):
        self._logger = logger

        self._image_size = (600, 344)
        self._grid = 8

        self._device = torch.device('cpu')
        full_state_dict = torch.load(cleaner_model_path, map_location=torch.device('cpu'))

        generator_state_dict = full_state_dict['G']

        if 'stage1.conv1.conv.weight' in generator_state_dict.keys():
            from deep_fill.model.networks import Generator
        else:
            from deep_fill.model.networks_tf import Generator

        self._generator = Generator(cnum_in=5, cnum=48, return_flow=False).to(self._device)
        self._generator.load_state_dict(generator_state_dict, strict=True)

        self._yolo_model = YOLO(yolo_model_path)

    def clean_images(self, images: np.ndarray):
        """
        This func can be used to remove ui

        ### Args:
        - images: np.ndarray: Numpy array of images .

        ### Returns:
            Numpy array of images
        """

        result_images = np.zeros((2, 344, 600, 3), dtype=np.uint8)
        for index, image in enumerate(images):
            image = Image.fromarray(image)
            results = self._yolo_model(image)

            w, h = image.size
            mask = np.zeros((h, w, 3), dtype=np.uint8)
            mask = Image.fromarray(mask)
            draw = ImageDraw.Draw(mask, "RGBA")
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    draw.rectangle(((b[0], b[1]), (b[2], b[3])), fill=(255, 255, 255, 255))

            # load image and mask
            image = image.resize(self._image_size)
            mask = mask.resize(self._image_size)

            # prepare input
            image = T.ToTensor()(image)
            mask = T.ToTensor()(mask)

            _, h, w = image.shape

            image = image[:3, :h // self._grid * self._grid, :w // self._grid * self._grid].unsqueeze(0)
            mask = mask[0:1, :h // self._grid * self._grid, :w // self._grid * self._grid].unsqueeze(0)

            self._logger.debug(f"Shape of image: {image.shape}")

            image = (image * 2 - 1.).to(self._device)  # map image values to [-1, 1] range
            mask = (mask > 0.5).to(dtype=torch.float32,
                                   device=self._device)  # 1.: masked 0.: unmasked

            image_masked = image * (1. - mask)  # mask image

            ones_x = torch.ones_like(image_masked)[:, 0:1, :, :]
            x = torch.cat([image_masked, ones_x, ones_x * mask],
                          dim=1)  # concatenate channels

            with torch.inference_mode():
                _, x_stage2 = self._generator(x, mask)

            image_inpainted = image * (1. - mask) + x_stage2 * mask
            img_out = ((image_inpainted[0].permute(1, 2, 0) + 1) * (self.UINT8_VALUE_RANGE / 2))  # IDK what it is
            img_out = img_out.to(device='cpu', dtype=torch.uint8)
            result_images[index, :] = img_out.numpy()

        return result_images
