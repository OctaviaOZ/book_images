#!/usr/bin/env python
# coding: utf-8

from settings.parameters import COVERS_FOLDER, OUTPUT_FOLDER_IMAGES, get_parameters, get_points
import argparse
import os
from numpy import argmax
from pickle import load
from timeit import default_timer as timer
from cv2 import imread, BRISK_create, FlannBasedMatcher


class Book:
    def __init__(self, image, isfolder, iscover):
        self.current_book = None
        self.image = image
        self.isfolder = isfolder
        self.iscover = iscover
        self.descriptions = None
        self.threshold = 0.7
        self.index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)

    @property
    def get_cur_book(self):

        if self.iscover:
            self.descriptions = self.getcover
            if self.descriptions:
                self.current_book = self.getmarker(self.image)
                if self.current_book:
                    with open(COVERS_FOLDER + "\\current_book.txt", 'w') as f:
                        f.write(str(self.current_book))

                    print('\nThe current book is', self.current_book)
                    return 0
                else:
                    print('\nDidn`t recognise the cover\n')
                    return 1
            else:
                print('\nDidn`t find the file with descriptions of covers in the folder', COVERS_FOLDER)
                return 1

        if os.path.exists(COVERS_FOLDER + "\\current_book.txt"):
            with open(COVERS_FOLDER + "\\current_book.txt", 'r') as f:
                self.current_book = str(f.readline())

        if not self.current_book:
            print('\nDidn`t find the current book, scan the cover of the chosen book with argument')
            return 1

        print('\nThe current book is', self.current_book)
        self.descriptions = self.getbook
        if self.descriptions:
            _ = self.getmarker(self.image)
            return 0
        else:
            print('\nDidn`t find the file with descriptions of boook`s pages in the folder', self.current_book)
            return 1

    @property
    def getbook(self):
        book_folder = self.current_book
        image_path = OUTPUT_FOLDER_IMAGES + "\\" + book_folder + "\\"
        if not os.path.exists(image_path):
            print("\n{0} not exists".format(image_path))
            return None
        # Getting back the objects:
        return f"{image_path}{self.current_book}.pickle"

    @property
    def getcover(self):
        if not os.path.exists(COVERS_FOLDER):
            print("\n{0}  not exists".format(COVERS_FOLDER))
            return None
        # Getting back the objects:
        return f"{COVERS_FOLDER}\\covers.pickle"

    def getmarker(self, image: object) -> str:
        """
        result of mathing of some pages
        :return: print result statment, name_book(page)
        """

        def findmacth(image_file):
            print('\nprocessing', str(image_file))
            start = timer()

            desc_1 = get_points(image_file, "", size, brisk)

            if desc_1 is not None:

                titles = []
                similarity = []
                titles_append = titles.append
                similarity_append = similarity.append

                for title, desc_2, len_desc_2 in root:

                    good_points = 0
                    matches = flann.knnMatch(desc_1, desc_2, k=2)

                    for m_n in matches:
                        if len(m_n) != 2:
                            continue
                        elif m_n[0].distance < self.threshold * m_n[1].distance:
                            good_points += 1

                    percentage_similarity = good_points / len_desc_2 * 100

                    if percentage_similarity > 2:
                        titles_append(title)
                        similarity_append(percentage_similarity)

                if similarity:
                    idx = argmax(similarity)
                    # for idx1, t in enumerate(titles):
                    print("Info: " + str(titles[idx]))
                    # print("percentage_similarity: {0}".format(str(similarity[idx])))

                    end = timer()
                    print('find_match_time: ', (end - start))

                    if not self.isfolder:
                        return str(titles[idx])
                else:
                    end = timer()
                    print("{0} no similarity".format(str(self.image)))
                    print('find_match_time: ', (end - start))
            else:
                print("\n{0} has not points".format(str(image)))

            if not self.isfolder:
                return None

        if not os.path.exists(self.descriptions):
            print("\nDid not find file {}".format(self.descriptions))
            return None

        with open(self.descriptions, 'rb') as handle:
            root = load(handle)

        flann = FlannBasedMatcher(self.index_params, {})

        if self.iscover:
            thresh, octaves, size, ext_of_files = get_parameters("covers")
        else:
            thresh, octaves, size, ext_of_files = get_parameters(self.current_book)

        if not thresh:
            return None

        brisk = BRISK_create(thresh, octaves)  # norm = cv.NORM_HAMMING (70,2) 30days

        if self.isfolder:

            files = os.listdir(self.image)
            for f in files:
                if f.endswith(ext_of_files):
                    findmacth(str(image) + "\\" + f)
            # cv_file.release()
        else:
            cur_book = findmacth(image)
            # cv_file.release()
            return cur_book

        return None


def main(image_name: str = None, isfolder: bool = False, iscover: bool = False):
    Book(image_name, isfolder, iscover).get_cur_book


if __name__ == '__main__':

    # PARAMETERS
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_name", type=str, required=True, help="process folder of images or single image")
    parser.add_argument("--cover", type=str, required=False, help="is image a cover? True or False")
    args = parser.parse_args()

    if args.folder_name:
        image_name = OUTPUT_FOLDER_IMAGES + "\\" + args.folder_name

        cover = False
        if args.cover:
            cover = bool(args.cover)

        main(image_name=image_name, isfolder=os.path.isdir(image_name), iscover=cover)
    else:
        print("\nDid not find image_name argument")
