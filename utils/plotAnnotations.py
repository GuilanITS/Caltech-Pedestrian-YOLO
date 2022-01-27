import os
import re
import time
import glob
import pandas as pd
from logger import logger
from config import genLabelsDir, genImagesDir, genPlotsDir


def annotationPlotter():
    """
    Plots the annotations of the generated images.
    """
    logger('Annotation plotter started!')
    # Initialization
    startTime = time.time()
    framesDataFrame = pd.DataFrame(columns=['Set', 'VideoId', 'FrameId'])
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
    # Get the list of sets and images
    for counter, image in enumerate(sorted(glob.glob(f'{genImagesDir}/*/*.png'))):
        setName = re.search('(set[0-9]+)', image).groups()[0]
        videoId = re.search('(V[0-9]+)', image).groups()[0]
        frameId = re.search('_([0-9]+)\.png', image).groups()[0]
        # Add to dataframe
        framesDataFrame = framesDataFrame.append(
            {'Set': setName, 'VideoId': videoId, 'FrameId': frameId}, ignore_index=True)
        # Adding a log
        if (counter % 500) == 0:
            print(f'Processed {setName} {videoId} frame#{frameId}...')
    # Processing dataframe
    # 1) Sorting
    framesDataFrame['FrameId'] = framesDataFrame['FrameId'].astype(int)
    framesDataFrame = framesDataFrame.sort_values(
        by=['Set', 'VideoId', 'FrameId'])
    framesDataFrame['FrameId'] = framesDataFrame['FrameId'].astype(str)
    # 2) Groupping
    framesDataFrame = framesDataFrame.groupby(['Set', 'VideoId'])[
        'FrameId'].apply(list)
    print(framesDataFrame)
    # Finalization
    elapsedTime = '{:.2f}'.format(time.time() - startTime)
    logger(f'Annotations plotted in {elapsedTime}s!')

# n_objects = 0
# for set_name in sorted(img_fns.keys()):
#     for video_name in sorted(img_fns[set_name].keys()):
#         wri = cv.VideoWriter(
#             'data/plots/{}_{}.avi'.format(set_name, video_name),
#             cv.VideoWriter_fourcc(*'XVID'), 30, (640, 480))
#         for frame_i, fn in sorted(img_fns[set_name][video_name]):
#             img = cv.imread(fn)
#             if str(frame_i) in annotations[set_name][video_name]['frames']:
#                 data = annotations[set_name][
#                     video_name]['frames'][str(frame_i)]
#                 for datum in data:
#                     x, y, w, h = [int(v) for v in datum['pos']]
#                     cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
#                     n_objects += 1
#                 wri.write(img)
#         wri.release()
#         print(set_name, video_name)
# print(n_objects)

# https://github.com/mitmul/caltech-pedestrian-dataset-converter/blob/master/tests/test_plot_annotations.py
