# Copyright (c) 2023 Keisuke Jikuya

# Copyright (c) Karan Desai (https://kdexd.xyz), The University of Michigan.

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import multiprocessing as mp
import os
import argparse
from typing import Any, Dict, List, Tuple
from tqdm import tqdm

from redcaps import _image_worker, ImageDownloader

def main(args):
    os.makedirs(args.img_dir, exist_ok=True)

    removed_ann_dir = args.ann_dir.replace('annotations', 'removed_annotations')
    os.makedirs(removed_ann_dir, exist_ok=True)

    image_downloader = ImageDownloader()
    workers = os.cpu_count()

    for annotations_file_name in sorted(os.listdir(args.ann_dir), reverse=args.reverse):
        annotations_filepath = os.path.join(args.ann_dir, annotations_file_name)
        removed_annotations_filepath = os.path.join(removed_ann_dir, annotations_file_name)
        # ファイルが存在していたらスキップ
        if os.path.exists(removed_annotations_filepath):
            continue
        annotations = json.load(open(annotations_filepath))

        # Parallelize image downloads.
        with mp.Pool(processes=workers) as p:

            worker_args: List[Tuple] = []
            for ann in annotations["annotations"]:
                image_savepath = os.path.join(
                    args.img_dir, ann["subreddit"], f"{ann['image_id']}.jpg"
                )
                worker_args.append((ann["url"], image_savepath, image_downloader))

            # Collect download status of images in these annotations (True/False).
            download_status: List[bool] = []

            with tqdm(total=len(worker_args), desc=f"Downloading {annotations_file_name}") as pbar:
                for _status in p.imap(_image_worker, worker_args):
                    download_status.append(_status)
                    pbar.update()

        # How many images were downloaded?
        num_downloaded = sum(download_status)
        print(
            f"Downloaded {num_downloaded}/{len(worker_args)} images "
            f"from {annotations_filepath}!"
        )
        # Optionally remove annotations for which images were unavailable.
        annotations["annotations"] = [
            ann
            for ann, downloaded in zip(annotations["annotations"], download_status)
            if downloaded
        ]

        print(f"Saving updated annotations...")
        json.dump(annotations, open(removed_annotations_filepath, "w"))
        print(f"Saved updated annotations at {removed_annotations_filepath}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--reverse', action='store_true')
    parser.add_argument('--img_dir', type=str, default='/data/dataset/redcaps/images/')
    parser.add_argument('--ann_dir', type=str, default='/data/dataset/redcaps/annotations/')
    args = parser.parse_args()
    main(args)