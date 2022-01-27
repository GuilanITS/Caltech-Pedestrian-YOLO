import os
import time
from glob import glob
from logger import logger
from scipy.io import loadmat
from config import genLabelsDir, caltechLabelsDir, genImagesDir, imageFormat, frameSize


classes = ['person', 'people']  # Classes in Caltech Pedestrian dataset


def convertBoxFormat(box):
    (left, top, width, height) = box
    (imageWidth, imageHeight) = frameSize
    drawWidth = 1./imageWidth
    drawHeight = 1./imageHeight
    x = (left + width / 2.0) * drawWidth
    y = (top + height / 2.0) * drawHeight
    w = width * drawWidth
    h = height * drawHeight
    return (x, y, w, h)


def annotationGenerator():
    """
    Generates a set of annotation files from Caltech Pedestrian .vbb files
    Parameters
    ----------
    Reads genLabelsDir from config.py
    """
    logger('Annotation generator started!')
    # Initialization
    startTime = time.time()
    numberOfTruthBoxes = 0
    datasets = {
        'train': open(f'{genLabelsDir}/train.txt', 'w'),
        'test': open(f'{genLabelsDir}/test.txt', 'w')
    }
    # Checking the input directory if contains .vbb files
    vbbFiles = sorted(glob(f'{caltechLabelsDir}/*/*.vbb'))
    if not vbbFiles:
        logger(f'{caltechLabelsDir} contains no ".vbb" files!', logLevel='error')
        return
    # Creating the output folder if it doesn't exist
    if not os.path.exists(genLabelsDir):
        os.makedirs(genLabelsDir)
    # Processing .vbb files
    for vbbFile in vbbFiles:
        # Grabs the name of .vbb file, e.g. V000
        fileName = os.path.basename(vbbFile).split('.')[0]
        # Grabs the parent directory of .vbb file, e.g., set001
        parentDirtName = os.path.basename(os.path.dirname(vbbFile))
        setId = parentDirtName.replace('set', '')  # e.g., 001
        datasetId = 'train' if int(setId) < 6 else 'test'
        print(f'Processing {fileName} in set{setId}... ({datasetId} data)')
        parentFolderDir = genLabelsDir + '/' + \
            parentDirtName  # e.g. E:/genAnnots/set001
        if not os.path.exists(parentFolderDir):
            os.makedirs(parentFolderDir)
        # Processing .vbb file
        try:
            vbb = loadmat(vbbFile)
            frameLists = vbb['A'][0][0][1][0]
            frameLabel = [str(item[0]) for item in vbb['A'][0][0][4][0]]
            # Processing frames
            for frameId, frameValue in enumerate(frameLists):
                if len(frameValue) > 0:
                    # Processing frames with labels
                    labels = ''
                    for pedestrianId, pedestrianPos in zip(frameValue['id'][0], frameValue['pos'][0]):
                        pedestrianId = int(pedestrianId[0][0]) - 1
                        pedestrianPos = pedestrianPos[0].tolist()
                        # Class filter and height filter
                        if frameLabel[pedestrianId] in classes and pedestrianPos[3] > 30 and pedestrianPos[3] <= 80:
                            classIndex = classes.index(
                                frameLabel[pedestrianId])
                            yoloBoxFormat = convertBoxFormat(pedestrianPos)
                            labels += str(classIndex) + ' ' + \
                                ' '.join([str(item)
                                         for item in yoloBoxFormat]) + '\n'
                            numberOfTruthBoxes += 1
                    if not labels:
                        continue
                    # Filling dataset files
                    imageId = f'{fileName}_{frameId}.{imageFormat}'
                    datasets[datasetId].write(
                        f'{genImagesDir}/{parentDirtName}/{imageId}\n')
                    # Writing labels to file
                    filePath = parentFolderDir + '/' + \
                        fileName + '_frame' + str(frameId) + '.txt'
                    labelFile = open(filePath, 'w')
                    labelFile.write(labels)
                    labelFile.close()
        except Exception as error:
            errorText = str(error)
            logger(f'Error while processing ({errorText})', logLevel="error")
    # Close dataset files
    logger('Closing dataset files ...')
    for dataset in datasets.values():
        dataset.close()
    elapsedTime = '{:.2f}'.format(time.time() - startTime)
    logger(
        f'Generated annotations in {elapsedTime}s!')
