# python 3.7.8
import argparse
import os
from settings.parameters import OUTPUT_FOLDER_IMAGES, get_parameters, get_points
from numpy import array
import pickle
from cv2 import BRISK_create

IMAGE_PATH = ''

def main(folder_name: str):
    """Processes folder of images and produce descriptor's file.

    :param folder_name: (str):
            Processes images (*.png).

    :saves
        detect the feature points and make the descriptors of images
        pkl-file with list of [name folder(file), descriptors]

    """

    thresh, octaves, size, ext_of_files = get_parameters(folder_name)

    if not ext_of_files:
        return 1

    brisk = BRISK_create(thresh, octaves)

    all_images_to_compare = []
    all_images_to_compare_append = all_images_to_compare.append
    files = os.listdir(IMAGE_PATH)
    for f in files:
            if f.endswith(ext_of_files):

                desc = get_points(IMAGE_PATH, f, size, brisk)
                if desc is not None:
                    all_images_to_compare_append((os.path.splitext(f)[0], desc, len(desc)))
                else:
                    print("impossible to find point", IMAGE_PATH + f)

    with open(IMAGE_PATH + folder_name + '.pickle', 'wb') as handle:
        pickle.dump(array(all_images_to_compare, dtype=object), handle, protocol=pickle.HIGHEST_PROTOCOL)

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