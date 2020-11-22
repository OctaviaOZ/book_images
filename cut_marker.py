import argparse
import os
from settings.parameters import OUTPUT_FOLDER, OUTPUT_FOLDER_IMAGES, get_parameters
import fitz
import numpy as np
from PIL import Image
import io

def findmarker(image: object, marker_name: str):

    def get_pix():
        base_image = doc.extractImage(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        if 'DeviceCMYK' in base_image['cs-name']:

            if 'Indexed' in base_image['cs-name']:
                metric = image.entropy()*2*(-1.0)
            else:
                metric = image.entropy()*(-1.0)
        else:
            print(name_image)
            metric = image.height * image.width

        return image, metric

    name_image = os.path.basename(image).split('.')[0]
    folder_name = OUTPUT_FOLDER_IMAGES+'\\'+marker_name+'\\'
    _, _, _, ext_of_files = get_parameters(folder_name)

    doc = fitz.open(image)

    pix_list = []
    pix_size = []

    for i in range(len(doc)):
        for img in doc.getPageImageList(i):

            if 'Separation' in img:
                continue

            xref = img[0]

            image, metric = get_pix()
            if image not in pix_list:
                pix_list.append(image)
                pix_size.append(metric)

    if not pix_size:
        print(f"n\Didn't find any picture at {image}")
        return 1

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    #if pixmap:
    #    idx = np.argmax(pix_size)
    #    pix = pix_list[idx]
    #    pix.writeImage("%s%s_%s.jpg" % (folder_name, marker_name, name_image))
     #   pix = None
    #else:
    idx = np.argmax(pix_size)
    image = pix_list[idx]
    image.save(open("%s%s_%s.%s" % (folder_name, marker_name, name_image, ext_of_files), "wb"))

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
