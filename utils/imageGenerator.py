import os
import time
import cv2 as cv
from glob import glob
from logger import logger
from config import caltechDataDir, imageFormat, genImagesDir


def saveImage(frame, dname, fn, i):
    cv.imwrite('{}/{}_{}_{}.png'.format(
        genImagesDir, os.path.basename(dname),
        os.path.basename(fn).split('.')[0], i), frame)


def imageGenerator():
    """
    Generates a set of images from Caltech Pedestrian .seq files
    Parameters
    ----------
    Reads caltechDataDir, imageFormat, and genImagesDir from config.py
    """
    logger('Image generator started!')
    # Checking the input directory if contains .seq files
    seqFiles = sorted(glob(f'{caltechDataDir}/*/*.seq'))
    if not seqFiles:
        logger(f'{caltechDataDir} contains no ".seq" files!', logLevel='error')
        return
    # Creating the output folder if it doesn't exist
    if not os.path.exists(genImagesDir):
        os.makedirs(genImagesDir)
    # Processing .seq files
    print(seqFiles)
    for seqFile in seqFiles:
        counter = 0
        startTime = time.time()
        # Grabs the name of .seq file, e.g. V000
        fileName = os.path.basename(seqFile).split('.')[0]
        # Grabs the parent directory of .seq file, e.g. set001
        parentDirtName = os.path.basename(os.path.dirname(seqFile))
        try:
            capture = cv.VideoCapture(seqFile)
            while True:
                # Read all frames from the sequence file
                existed, frame = capture.read()
                if not existed:
                    break
                # Saving image
                saveImage(frame, parentDirtName)
                # Create a log every 25 passed
                if (counter % 100 == 0):
                    print(f'Processing file #{counter} in {fileName}')
                counter += 1
            elapsedTime = '{:.2f}'.format(time.time() - startTime)
            logger(
                f'Generated {counter-1} images from {fileName} in {elapsedTime}s!')
        except Exception as error:
            errorText = str(error)
            logger(f'Error while processing ({errorText})', logLevel="error")


# def save_img(dname, fn, i, frame):
#     cv.imwrite('{}/{}_{}_{}.png'.format(
#         outputDirectory, os.path.basename(dname),
#         os.path.basename(fn).split('.')[0], i), frame)


# def convert(dir, squared: bool = False):
#     for dname in sorted(glob.glob(dir)):
#         for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
#             cap = cv.VideoCapture(fn)
#             i = 0
#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 if (squared):
#                     square()
#                 save_img(dname, fn, i, frame)
#                 i += 1
#             print(fn)


# convert(inputDirectory)


# https://github.com/simonzachau/caltech-pedestrian-dataset-to-yolo-format-converter/blob/master/generate-images.py

# https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/tests/test_plot_annotations.py
