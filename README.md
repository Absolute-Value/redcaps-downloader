# RedCaps Downloader

This repository is copy of [redcaps-dataset/redcaps-downloader](https://github.com/redcaps-dataset/redcaps-downloader)

This repository provides the unofficial code for downloading and extending the [RedCaps dataset](https://openreview.net/forum?id=VjJxBi1p9zh).
Users can seamlessly download images of officially released annotations as well as download more image-text data from any subreddit over an arbitrary time-span.

## Basic usage: Download official RedCaps dataset images

```text
/data/datasets/redcaps/
├── annotations/
│   ├── abandoned_2017.json
│   ├── abandoned_2017.json
│   ├── ...
│   ├── itookapicture_2019.json
│   ├── itookapicture_2020.json
│   ├── <subreddit>_<year>.json
│   └── ...
│
└── images/
    ├── abandoned/
    │   ├── guli1.jpg
    |   └── ...
    │
    ├── itookapicture/
    │   ├── 1bd79.jpg
    |   └── ...
    │
    ├── <subreddit>/
    │   ├── <image_id>.jpg
    │   ├── ...
    └── ...
```

1. Download images by using this command.
    ```bash
    python downloader.py
    ```
    Reverse download by adding `--reverse`.
    Parallelize download in default. RedCaps images are sourced from Reddit,
    Imgur and Flickr, each have their own request limits. This code contains
    approximate sleep intervals to manage them. Use multiple machines (= different
    IP addresses) or a cluster to massively parallelize downloading.

## Citation

If you find this code useful, please consider citing:

```text
@inproceedings{desai2021redcaps,
    title={{RedCaps: Web-curated image-text data created by the people, for the people}},
    author={Karan Desai and Gaurav Kaul and Zubin Aysola and Justin Johnson},
    booktitle={NeurIPS Datasets and Benchmarks},
    year={2021}
}
```
