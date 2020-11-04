import cv2 as cv  # '4.4.0'
import os


BRISK = cv.BRISK_create(70, 2)  # norm = cv.NORM_HAMMING

OUTPUT_FOLDER = os.path.sys.path[00]
COVERS_FOLDER = OUTPUT_FOLDER+'\\images\\covers'
OUTPUT_FOLDER_IMAGES = OUTPUT_FOLDER+'\\images'

def resize(image: object = None, scale_factor: int = 500):
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
    return cv.resize(image, None, None, scale, scale, cv.INTER_LINEAR)
