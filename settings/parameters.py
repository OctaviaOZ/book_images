import os
import json
from cv2 import imread, cvtColor, resize, COLOR_BGR2GRAY
from numpy import float32


OUTPUT_FOLDER = os.path.sys.path[00]
OUTPUT_FOLDER_IMAGES = os.path.join(OUTPUT_FOLDER, "images")
COVERS_FOLDER = os.path.join(OUTPUT_FOLDER_IMAGES, "covers")


def get_parameters(book: str):

    path_ = os.path.join(OUTPUT_FOLDER, "settings")
    path_ = os.path.join(path_, "specifications.json")
    with open(path_, 'r') as f:

        resp_dict = json.load(f)
        book_dict = resp_dict.get(book, None)
        if book_dict:

            return book_dict['thresh'], book_dict['octaves'], book_dict['resize'], \
                                        book_dict['extension']

        else:

            print("\nDid not find parameters in specifications for book", book)
            return 0, 0, 0


def resize_(image: object = None, scale_factor: int = 300):
    """
    resize image to increase performance
    return: resized image by factor scale_factor
    """
    h, w = image.shape[0], image.shape[1]

    if (w <= h and w < scale_factor) or (h <= w and h < scale_factor):
        return image

    scale = round(scale_factor/h,3)
    return resize(image, None, None, scale, scale) # default INTER_LINEAR


def get_points(image_path, f, size, brisk):

    # 1: cv2.IMREAD_COLOR
    # 0: cv2.IMREAD_GRAYSCALE
    image = imread(image_path + f, 1)

    if image is None:
        print('\n' + image_path + f + " didn't find")
        return None

    image = resize_(image, size)
    image = cvtColor(image, COLOR_BGR2GRAY) #6

    image[0] = image[0] / 255.
    image[1] = image[1] / 255.

    _, desc = brisk.detectAndCompute(image, None)

    return desc