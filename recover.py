from PIL import Image
from tqdm import tqdm
import io
import os
import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str, default='gardening_2019')
args = parser.parse_args()

image_dir = '/data/dataset/redcaps/images/'
annotations_dir = '/data/dataset/redcaps/removed_annotations/'
for annotations_file_name in os.listdir(annotations_dir):
    if args.target in annotations_file_name and 'vegetablegardening' not in annotations_file_name:
        annotations_filepath = os.path.join(annotations_dir, annotations_file_name)
        annotations = json.load(open(annotations_filepath))
        loop = tqdm(annotations["annotations"], desc=annotations_file_name)
        for ann in loop:
            image_path = os.path.join(image_dir, 'gardening', ann['image_id'] + '.jpg')
            try:
                Image.open(image_path).convert("RGB")
            except:
                print('anomaly', ann)
                url = ann['url']
                response = requests.get(url)
                pil_image = Image.open(io.BytesIO(response.content)).convert("RGB")

                if 512 > 0:
                    image_width, image_height = pil_image.size

                    scale = 512 / float(max(image_width, image_height))

                if scale != 1.0:
                    new_width, new_height = tuple(
                        int(round(d * scale)) for d in (image_width, image_height)
                    )
                    pil_image = pil_image.resize((new_width, new_height))
                pil_image.save(image_path)