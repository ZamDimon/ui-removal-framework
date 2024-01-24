import argparse
import os

import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw
import torch
import torchvision.transforms as T


parser = argparse.ArgumentParser(description='Test inpainting')

parser.add_argument("--checkpoint", type=str,
                    default="pretrained/states_tf_places2.pth", help="path to the checkpoint file")
parser.add_argument("--yolo_path", type=str,
                    default="yolo path...", help="path to the yolo model")
parser.add_argument("--folder_path", type=str,
                    default="folder path...", help="path to folder with images")

def main():
    args = parser.parse_args()

    device = torch.device('cpu')
    full_state_dict = torch.load(args.checkpoint, map_location=torch.device('cpu'))

    generator_state_dict = full_state_dict['G']

    if 'stage1.conv1.conv.weight' in generator_state_dict.keys():
        import sys
        sys.path.append('../')
        from model.networks import Generator
    else:
        import sys
        sys.path.append('../')
        from model.networks_tf import Generator

    # set up network
    generator = Generator(cnum_in=5, cnum=48, return_flow=False).to(device)

    generator.load_state_dict(generator_state_dict, strict=True)

    yolo = YOLO(args.yolo_path)
    folder_path = args.folder_path

    for file in os.listdir(folder_path):
        image = os.path.join(folder_path,  file)
        results = yolo.predict(image)
        image = Image.open(image)

        w, h = image.size
        mask = np.zeros((h, w, 3), dtype=np.uint8)
        mask = Image.fromarray(mask)
        draw = ImageDraw.Draw(mask, "RGBA")
        for result in results:
            boxes = result.boxes
            for box in boxes:
                b = box.xyxy[0]
                draw.rectangle(((b[0], b[1]), (b[2], b[3])), fill=(255, 255, 255, 255))

        image = image.resize((600, 344))
        mask = mask.resize((600, 344))

        # prepare input
        image = T.ToTensor()(image)
        mask = T.ToTensor()(mask)

        _, h, w = image.shape
        grid = 8


        image = image[:3, :h//grid*grid, :w//grid*grid].unsqueeze(0)
        mask = mask[0:1, :h//grid*grid, :w//grid*grid].unsqueeze(0)

        print(f"Shape of image: {image.shape}")

        image = (image*2 - 1.).to(device)  # map image values to [-1, 1] range
        mask = (mask > 0.5).to(dtype=torch.float32,
                               device=device)  # 1.: masked 0.: unmasked

        image_masked = image * (1.-mask)  # mask image

        ones_x = torch.ones_like(image_masked)[:, 0:1, :, :]
        x = torch.cat([image_masked, ones_x, ones_x*mask],
                      dim=1)  # concatenate channels

        with torch.inference_mode():
            _, x_stage2 = generator(x, mask)

        # complete image
        image_inpainted = image * (1.-mask) + x_stage2 * mask

        # save inpainted image
        img_out = ((image_inpainted[0].permute(1, 2, 0) + 1)*127.5)
        img_out = img_out.to(device='cpu', dtype=torch.uint8)
        img_out = Image.fromarray(img_out.cpu().numpy())
        img_out.save(f"../cleaned/{file}")


        # # subplot(r,c) provide the no. of rows and columns
        # f, axarr = plt.subplots(2, 1)
        #
        # # use the created array to output your multiple images. In this case I have stacked 4 images vertically
        #
        # axarr[0].imshow(Image.open(os.path.join(folder_path,  file)))
        #
        # axarr[1].imshow(Image.open(f"../cleaned/{file}"))
        # plt.show()



if __name__ == "__main__":
    main()
