# python 3.7.8
import argparse
import os
from parameters import BRISK, OUTPUT_FOLDER_IMAGES, resize
import cv2 as cv  # '4.4.0'
import numpy as np
import pickle

IMAGE_PATH = ''

def main(folder_name: str):
    """Processes folder of images and produce descriptor's file.

    :param folder_name: (str):
            Processes images (*.png).

    :saves
        detect the feature points and make the descriptors of images
        pkl-file with list of [name folder(file), descriptors]

    """

    #cv_file = cv.FileStorage(image_path + folder_name + '.xml', cv.FILE_STORAGE_WRITE)
    #cv_file.startWriteStruct('Mapping', cv.FileNode_MAP)

    all_images_to_compare = []
    for _, _, files in os.walk(IMAGE_PATH):

        for f in files:
            if f.endswith('.png'):

                image = cv.imread(IMAGE_PATH + f, cv.IMREAD_COLOR)
                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

                image[0] = image[0] / 255.
                image[1] = image[1] / 255.

                #star = cv.xfeatures2d.StarDetector_create()
                # Initiate BRIEF extractor
                #brief = cv.xfeatures2d.BriefDescriptorExtractor_create()
                # find the keypoints with STAR
                #kp = star.detect(image, None)
                # compute the descriptors with BRIEF
                #_, desc = brief.compute(image, kp)

                _, desc = BRISK.detectAndCompute(image, None)
                #cv_file.write(os.path.splitext(f)[0], desc)
                if desc is not None:
                    all_images_to_compare.append((os.path.splitext(f)[0], desc, len(desc)))
                else:
                    print("impossible to find point", IMAGE_PATH + f)

    #cv_file.endWriteStruct()
    #cv_file.release()
    with open(IMAGE_PATH + folder_name + '.pickle', 'wb') as handle:
        pickle.dump(np.array(all_images_to_compare, dtype=object), handle, protocol=pickle.HIGHEST_PROTOCOL)

    #with open(IMAGE_PATH + folder_name + '.npy', 'wb') as handle_file:
    #    np.save(handle_file, np.array(all_images_to_compare, dtype=object), allow_pickle=True)

    print("\nDescriptor's file is saved as", "{0}{1}.pickle".format(IMAGE_PATH, folder_name))


if __name__ == '__main__':

    # PARAMETERS
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_name", type=str, help="process folder of images", required=True)
    args = parser.parse_args()

    if args.folder_name:
        folder_path = args.folder_name

        IMAGE_PATH = OUTPUT_FOLDER_IMAGES + "\\" + folder_path + "\\"

        if os.path.exists(IMAGE_PATH):
            main(folder_name=folder_path)
        else:
            print(f"\n{IMAGE_PATH} not exists")
    else:
        print("\nDid not find --folder_name argument")