import cv2 as cv  # '4.4.0'
import os
import json


OUTPUT_FOLDER = os.path.sys.path[00]
#OUTPUT_FOLDER = os.getcwd()
OUTPUT_FOLDER_IMAGES = os.path.join(OUTPUT_FOLDER, "images")
COVERS_FOLDER = os.path.join(OUTPUT_FOLDER_IMAGES, "covers")


def get_parameters(book: str):

    path_ = os.path.join(OUTPUT_FOLDER, "settings")
    path_ = os.path.join(path_, "specifications.json")
    with open(path_, 'r') as f:
        resp_dict = json.load(f)
        book_dict = resp_dict.get(book, None)
        if book_dict:
            return book_dict['thresh'], book_dict['octaves'], book_dict['resize'], book_dict['extension']
        else:
            print("\nDid not find parameters in specifications for book", book)
            return 0, 0, 0


def resize(image: object = None, scale_factor: int = 300):
    """
    resize image to increase performance
    return: resized image by factor scale_factor
    """

    h, w = image.shape[0], image.shape[1]
    if (w <= h and w < scale_factor) or (h <= w and h < scale_factor):
        return image

    scale = round(scale_factor/h,3)
    #if w < h:
    #    ow = scale_factor
    #    oh = int(scale_factor * h / w)
    #else:
    #    oh = scale_factor
    #    ow = int(scale_factor * w / h)
    #return cv.resize(image, (oh, ow), cv.INTER_LINEAR)
    return cv.resize(image, None, None, scale, scale, cv.INTER_LINEAR)# cv.INTER_NEAREST)# cv.INTER_LINEAR)

def rgb2gray(rgb):
    #if img.shape == 3
    fil = [0.299, 0.587, 0.144]
    #return np.dot(rgb, fil)