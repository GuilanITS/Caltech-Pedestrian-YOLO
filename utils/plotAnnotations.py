import os
import re
import time
import json
import glob
import cv2 as cv
from logger import logger
from collections import defaultdict
from config import genLabelsDir, genImagesDir, genPlotsDir


def annotationPlotter():
    """
    """
    logger('Annotation plotter started!')
    # Initialization
    startTime = time.time()
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
    # Finalization
    elapsedTime = '{:.2f}'.format(time.time() - startTime)
    logger(f'Annotations plotted in {elapsedTime}s!')

# genImagesDir = 'E:/Datasets/Dataset 19 - Caltech/set00_images'
# annotations = json.load(open('data/annotations.json'))

# out_dir = 'data/plots'
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)

# img_fns = defaultdict(dict)

# for fn in sorted(glob.glob(f'{genImagesDir}/*.png')):
#     set_name = re.search('(set[0-9]+)', fn).groups()[0]
#     img_fns[set_name] = defaultdict(dict)

# for fn in sorted(glob.glob(f'{genImagesDir}/*.png')):
#     set_name = re.search('(set[0-9]+)', fn).groups()[0]
#     video_name = re.search('(V[0-9]+)', fn).groups()[0]
#     img_fns[set_name][video_name] = []

# for fn in sorted(glob.glob(f'{genImagesDir}/*.png')):
#     set_name = re.search('(set[0-9]+)', fn).groups()[0]
#     video_name = re.search('(V[0-9]+)', fn).groups()[0]
#     n_frame = re.search('_([0-9]+)\.png', fn).groups()[0]
#     img_fns[set_name][video_name].append((int(n_frame), fn))

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
