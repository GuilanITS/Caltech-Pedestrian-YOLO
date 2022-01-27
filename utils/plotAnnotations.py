import os
import re
import time
import glob
import cv2 as cv
import pandas as pd
from logger import logger
from config import genLabelsDir, genImagesDir, genPlotsDir, frameSize


def annotationPlotter():
    """
    Plots the annotations of the generated images.
    """
    logger('Annotation plotter started!')
    # Initialization
    startTime = time.time()
    framesDataFrame = pd.DataFrame(
        columns=['Set', 'VideoId', 'FrameId', 'Labels'])
    # Check if the paths are not empty
    if not os.path.exists(genImagesDir) or not os.listdir(genImagesDir):
        logger('The path to the images is empty or does not exist!', logLevel="error")
        return
    if not os.path.exists(genLabelsDir) or not os.listdir(genLabelsDir):
        logger('The path to the annotations is empty or does not exist!',
               logLevel="error")
        return
    # Creating the output folder if it doesn't exist
    if not os.path.exists(genPlotsDir):
        os.makedirs(genPlotsDir)
    # Get the list of sets and images to create framesDataFrame
    for counter, image in enumerate(sorted(glob.glob(f'{genImagesDir}/*/*.png'))):
        setName = re.search('(set[0-9]+)', image).groups()[0]
        videoId = re.search('(V[0-9]+)', image).groups()[0]
        frameId = re.search('_([0-9]+)\.png', image).groups()[0]
        # Process labels
        labels = []
        txtFilePath = f'{genLabelsDir}/{setName}/{videoId}_frame{frameId}.txt'
        if os.path.exists(txtFilePath):
            txtFile = open(txtFilePath, 'r')
            lines = txtFile.readlines()
            for line in lines:
                # Remove \n from the end of the line
                line = line.rstrip()
                # Fetches the labels stored in lines
                splittedLine = line.split(' ')
                classId = splittedLine[0]
                coordinates = splittedLine[1:]
                labels.append({'classId': classId, 'coordinates': coordinates})
            txtFile.close()
        # Add to dataframe
        framesDataFrame = framesDataFrame.append(
            {'Set': setName, 'VideoId': videoId, 'FrameId': frameId, 'Labels': labels}, ignore_index=True)
        # Adding a log
        if (counter % 500) == 0:
            print(f'Processed {setName} {videoId} frame#{frameId}...')
    # Processing dataframe
    # 1) Sorting
    framesDataFrame['FrameId'] = framesDataFrame['FrameId'].astype(int)
    framesDataFrame = framesDataFrame.sort_values(
        by=['Set', 'VideoId', 'FrameId'])
    framesDataFrame['FrameId'] = framesDataFrame['FrameId'].astype(str)
    # 2) Groupping into a dictionary
    framesDict = framesDataFrame.groupby(['Set', 'VideoId'])[
        'FrameId'].apply(list)
    # Iterating over the dataframe
    for counter, (setName, videoId) in enumerate(framesDict.index):
        print(f'Processing {setName} {videoId}...')
        videoWrither = cv.VideoWriter(
            f'{genPlotsDir}/{setName}_{videoId}.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
        for frameId in framesDict.loc[(setName, videoId)]:
            framePath = f'{genImagesDir}/{setName}/{videoId}_{frameId}.png'
            frame = cv.imread(framePath)
            # Get the labels
            labels = framesDataFrame.query(
                f'Set == "{setName}" and VideoId == "{videoId}" and FrameId == "{frameId}"')['Labels'].values[0]
            # Add annotations if there are any
            for label in labels:
                x, y, w, h = label['coordinates']
                x, y, w, h = round(float(x)), round(
                    float(y)), round(float(w)), round(float(h))
                # Set different colors for different classes
                color = (0, 255, 0) if label['classId'] == '0' else (255, 0, 0)
                # Draw the rectangle and the text
                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(frame, label['classId'], (x, y),
                           cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            videoWrither.write(frame)
        videoWrither.release()
    # Finalization
    elapsedTime = '{:.2f}'.format(time.time() - startTime)
    logger(f'Annotations plotted in {elapsedTime}s!')
