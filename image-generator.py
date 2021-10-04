import os
import glob
import cv2 as cv


inputDirectory = 'E:\Datasets\Dataset 19 - Caltech\set00'
outputDirectory = 'E:\Datasets\Dataset 19 - Caltech\set00_images'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)


def save_img(dname, fn, i, frame):
    cv.imwrite('{}/{}_{}_{}.png'.format(
        outputDirectory, os.path.basename(dname),
        os.path.basename(fn).split('.')[0], i), frame)


def convert(dir):
    for dname in sorted(glob.glob(dir)):
        for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
            cap = cv.VideoCapture(fn)
            i = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                save_img(dname, fn, i, frame)
                i += 1
            print(fn)


convert(inputDirectory)


# https://github.com/simonzachau/caltech-pedestrian-dataset-to-yolo-format-converter/blob/master/generate-images.py
