import argparse
import os
from settings.parameters import OUTPUT_FOLDER, OUTPUT_FOLDER_IMAGES, get_parameters, get_points
import fitz
from PIL import Image
import io
from cv2 import BRISK_create
from numpy import argmax


def findmarker(image: object, marker_name: str):

    def get_pix():
        base_image = doc.extractImage(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))

        return image

    name_image = os.path.basename(image).split('.')[0]
    folder_name = OUTPUT_FOLDER_IMAGES+'\\'+marker_name+'\\'
    thresh, octaves, size, ext_of_files = get_parameters(marker_name)

    if not ext_of_files:
        return 1

    brisk = BRISK_create(thresh, octaves)

    doc = fitz.open(image)

    pix_list = []
    pix_size = []
    pix_list_append = pix_list.append
    pix_size_append = pix_size.append

    print("=" * 10)
    print(f"{name_image}")

    for i in range(len(doc)):
        for img in doc.getPageImageList(i):

            if 'Separation' in img:
                continue

            xref = img[0]


            image = get_pix()
            if image not in pix_list:
                pix_list_append(image)

    if not pix_list:
        print(f"\nDidn't find any picture at {name_image}")
        return 1

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for idx in range(len(pix_list)):
        image = pix_list[idx]

        image.save(open("%s%s_%s_%s.%s" % (folder_name, marker_name, name_image, idx, ext_of_files), "wb"))

        desc = \
        get_points(folder_name, "%s_%s_%s.%s" % (marker_name, name_image, idx, ext_of_files), size, brisk)

        if desc is not None:
            pix_size_append(len(desc))
        else:
            pix_size_append(0)

    idx = argmax(pix_size)

    if pix_size[idx] < 2000:
        idx = len(pix_size)
        print(f"Didn't find a picture at {name_image} with the appropriate quality!!! Need more pdf-s pages\n")

    for j in range(len(pix_size)):

        if j != idx:
            os.remove("%s%s_%s_%s.%s" % (folder_name, marker_name, name_image, j, ext_of_files))

        else:
            os.rename(\
            "%s%s_%s_%s.%s" % (folder_name, marker_name, name_image, idx, ext_of_files), \
            "%s%s_%s.%s" % (folder_name, marker_name, name_image, ext_of_files))

    return 0

def main(folder_name: str, marker_name: str):

    isfolder = os.path.isdir(image_name)

    if isfolder:

        files = os.listdir(folder_name)
        for f in files:
            if f.endswith('pdf'):
                findmarker(folder_name + "\\" + f, marker_name)

    else:
        findmarker(folder_name, marker_name)


if __name__ == '__main__':

    # PARAMETERS
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_name", type=str, required=True, help="process folder of images or single image")
    parser.add_argument("--marker_name", type=str, required=True, help="short name of book")
    args = parser.parse_args()

    if args.folder_name:

        if args.marker_name:

            image_name = OUTPUT_FOLDER + "\\" + args.folder_name

            main(folder_name=image_name, marker_name=args.marker_name)
        else:
            print("\nDid not find marker_name argument")
    else:
        print("\nDid not find image_name argument")
