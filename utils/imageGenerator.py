import os
import time
import cv2 as cv
from glob import glob
from logger import logger
from config import caltechDataDir, imageFormat, genImagesDir


def saveImage(frame, folderName, fileName, counter):
    destFolder = genImagesDir + '/' + folderName
    try:
        cv.imwrite(os.path.join(
            destFolder, f'{fileName}_{counter}.{imageFormat}'), frame)
    except cv.error as openCVError:
        errorText = str(openCVError)
        logger(f'Error while creating image ({errorText})', logLevel="error")


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
    for seqFile in seqFiles:
        counter = 0
        startTime = time.time()
        # Grabs the name of .seq file, e.g. V000
        fileName = os.path.basename(seqFile).split('.')[0]
        # Grabs the parent directory of .seq file, e.g. set001
        parentDirtName = os.path.basename(os.path.dirname(seqFile))
        parentFolderDir = genImagesDir + '/' + parentDirtName  # e.g. genImages/set001
        if not os.path.exists(parentFolderDir):
            os.makedirs(parentFolderDir)
        try:
            capture = cv.VideoCapture(seqFile)
            while True:
                # Read all frames from the sequence file
                existed, frame = capture.read()
                if not existed:
                    break
                # Saving image
                saveImage(frame, parentDirtName, fileName, counter)
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
