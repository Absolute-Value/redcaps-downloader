# Copyright (c) 2023 Keisuke Jikuya

# Copyright (c) Karan Desai (https://kdexd.xyz), The University of Michigan.

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import time

def _image_worker(args):
    r"""Helper method for parallelizing image downloads."""
    image_url, image_savepath, image_downloader = args

    download_status = image_downloader.download(image_url, save_to=image_savepath)

    # Sleep for 2 seconds for Imgur, and 0.1 seconds for Reddit and Flickr.
    # This takes care of all request rate limits.
    if "imgur" in image_url:
        time.sleep(2.0)
    else:
        time.sleep(0.1)

    return download_status
