# Copyright (c) 2023 Keisuke Jikuya

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import csv

# imagesのフォルダ内のファイル数をすべて出力
REDCAPS_DIR = '/data/dataset/redcaps/'
images_dir = os.path.join(REDCAPS_DIR,'images/')
images = os.listdir(images_dir)

all_files_count = 0
all_files_dict = {}

for label in images:
    label_dir = os.path.join(REDCAPS_DIR,'images/', label)
    # label_dirの中身のファイル数をカウント
    files = os.listdir(label_dir)
    files_count = len(files)
    all_files_count += files_count
    print(f'{label}: {files_count}')
    all_files_dict[label] = files_count

print('all_files_count:', all_files_count)

print('creating all_files_dict.csv...')
# all_files_dictをcsvに出力
with open('all_files_dict.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['label', 'count'])
    for label, count in all_files_dict.items():
        writer.writerow([label, count])
    writer.writerow(['all_files_count', all_files_count])

print('all_files_dict.csv is created.')