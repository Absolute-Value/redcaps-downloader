import os
import json
import shutil
import argparse
from tqdm import tqdm
import multiprocessing as mp
from typing import List, Tuple

def main(args):
    workers = os.cpu_count()

    os.makedirs(args.to_ann_dir, exist_ok=True)
    removed_annotations = sorted(os.listdir(args.from_ann_dir))
    removed_annotations = [x for x in removed_annotations if '2020' in x]
    len_removed_annotations = len(removed_annotations)

    with mp.Pool(processes=workers) as p:
        worker_args: List[Tuple] = []
        for annotations in removed_annotations:
            if '2020' in annotations:
                worker_args.append((args.from_ann_dir, args.to_ann_dir, annotations))

        with tqdm(total=len(worker_args), desc='copying annotaions') as pbar:
            for _status in p.imap(_ann_download_worker, worker_args):
                pbar.update()

    print(f"Annotaions Downloaded.")
    
    for i, annotations_file_name in enumerate(removed_annotations):
        annotations_file_path = os.path.join(args.to_ann_dir, annotations_file_name)
        annotations = json.load(open(annotations_file_path))

        with mp.Pool(processes=workers) as p:
            worker_args2: List[Tuple] = []
            for ann in annotations["annotations"]:
                os.makedirs(os.path.join(args.to_img_dir, ann["subreddit"]), exist_ok=True)
                from_image_path = os.path.join(
                    args.from_img_dir, ann["subreddit"], f"{ann['image_id']}.jpg"
                )
                to_image_path = os.path.join(
                    args.to_img_dir, ann["subreddit"], f"{ann['image_id']}.jpg"
                )
                worker_args2.append((from_image_path, to_image_path))

            with tqdm(total=len(worker_args2), desc=f"{annotations_file_name} [{i+1}/{len_removed_annotations}]") as pbar:
                for _status in p.imap(_img_download_worker, worker_args2):
                    pbar.update()

def _ann_download_worker(args):
    from_ann_dir, to_ann_dir, annotations = args
    from_ann_path = os.path.join(from_ann_dir, annotations)
    to_ann_path = os.path.join(to_ann_dir, annotations)
    if not os.path.exists(to_ann_path):
        shutil.copy(from_ann_path, to_ann_dir)

def _img_download_worker(args):
    from_image_path, to_image_path = args
    if not os.path.exists(to_image_path):
        shutil.copy(from_image_path, to_image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--reverse', action='store_true')
    parser.add_argument('--from_ann_dir', type=str, default='/data/dataset/redcaps/removed_annotations/')
    parser.add_argument('--from_img_dir', type=str, default='/data/dataset/redcaps/images/')
    parser.add_argument('--to_ann_dir', type=str, default='/user/data/redcaps/removed_annotations/')
    parser.add_argument('--to_img_dir', type=str, default='/user/data/redcaps/images/')
    args = parser.parse_args()
    main(args)