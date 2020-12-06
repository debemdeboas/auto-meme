from PIL import Image
from typing import Any

import os
import shutil



def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.

    No modifications were made to the original function.
    Credit: https://stackoverflow.com/a/52969463/9918829
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')


def prepare_image(img_path: str) -> str:
    img = Image.open(img_path, 'r')
    if img.width > img.height:
        fixed = img.width
    else:
        fixed = img.height
    output_path = img_path[:-4] + '_resized' + img_path[-4:]
    resize(img, fixed, fixed).save(output_path)
    os.remove(img_path)
    return output_path


def save_image(req: Any) -> str:
    filename = './images/' + str(hash(req))[1:] + '.jpg'
    with open(filename, 'wb') as f:
        shutil.copyfileobj(req, f)
    return filename