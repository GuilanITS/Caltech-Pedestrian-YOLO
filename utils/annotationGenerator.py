import os
import time
from glob import glob
from logger import logger
from scipy.io import loadmat
from config import genLabelsDir, caltechLabelsDir, genImagesDir, imageFormat


classes = ['person', 'people']  # Classes in Caltech Pedestrian dataset
frameSize = (640, 480)  # Resolution of files in Caltech Pedestrian dataset


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
        parentFolderDir = genLabelsDir + '/' + parentDirtName  # e.g. genAnnots/set001
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
                        fileName + '_' + str(frameId) + '.txt'
                    labelFile = open(f'{genLabelsDir}/' + filePath, 'w')
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
        f'Generated annotations for {vbbFile} in {elapsedTime}s!')

# # traverse sets
# for caltech_set in sorted(glob.glob(f'{caltechLabelsDir}/set*')):
#     set_nr = os.path.basename(caltech_set).replace('set', '')
#     dataset = 'train' if int(set_nr) < 6 else 'test'
#     set_id = dataset + set_nr
#     # traverse videos
#     for caltech_annotation in sorted(glob.glob(caltech_set + '/*.vbb')):
#         vbb = loadmat(caltech_annotation)
#         obj_lists = vbb['A'][0][0][1][0]
#         obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
#         video_id = os.path.splitext(os.path.basename(caltech_annotation))[0]

#         # traverse frames
#         for frame_id, obj in enumerate(obj_lists):
#             if len(obj) > 0:

#                 # traverse labels
#                 labels = ''
#                 for pedestrian_id, pedestrian_pos in zip(obj['id'][0], obj['pos'][0]):
#                     pedestrian_id = int(pedestrian_id[0][0]) - 1
#                     pedestrian_pos = pedestrian_pos[0].tolist()
#                     # class filter and height filter: here example for medium distance
#                     if obj_lbl[pedestrian_id] in classes and pedestrian_pos[3] > 30 and pedestrian_pos[3] <= 80:
#                         class_index = classes.index(obj_lbl[pedestrian_id])
#                         yolo_box_format = convertBoxFormat(pedestrian_pos)
#                         labels += str(class_index) + ' ' + \
#                             ' '.join([str(n) for n in yolo_box_format]) + '\n'
#                         number_of_truth_boxes += 1

#                 # if no suitable labels left after filtering, continue
#                 if not labels:
#                     continue

#                 image_id = set_id + '_' + video_id + '_' + str(frame_id)
#                 datasets[dataset].write(genImagesDir + '/' + image_id + ('_squared' if squared else '') + '.png\n')
#                 label_file = open(f'{genLabelsDir}/' + image_id + ('_squared' if squared else '') + '.txt', 'w')
#                 label_file.write(labels)
#                 label_file.close()

#                 print('finished ' + image_id)

# for dataset in datasets.values():
#     dataset.close()

# print(number_of_truth_boxes)
