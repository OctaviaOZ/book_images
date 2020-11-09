import argparse
import os
from settings.parameters import OUTPUT_FOLDER, OUTPUT_FOLDER_IMAGES
import fitz
import numpy as np

def findmarker(image: object, marker_name: str):

    name_image = os.path.basename(image).split('.')[0]
    #split_name = os.path.split(image)
    #name_image = split_name[1].split('.')[0]
    folder_name = OUTPUT_FOLDER_IMAGES+'\\'+marker_name+'\\'

    doc = fitz.open(image)

    pix_list = []
    pix_size = []

    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            pix_list.append(pix)
            pix_size.append(pix.size)
            pix = None

    if not pix_size:
        print(f"n\Didn't find any picture at {image}")
        return 1

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    idx = np.argmax(pix_size)
    pix = pix_list[idx]

    if pix.n < 5:  # can be saved as PNG
        pix.writeImage("%s%s_%s.jpg" % (folder_name, marker_name, name_image))
    else:  # must convert the CMYK first
        pix0 = fitz.Pixmap(fitz.csRGB, pix)
        pix0.writeImage("%s%s_%s.png" % (folder_name, marker_name, name_image))
        pix0 = None  # free Pixmap resources
    pix = None
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
