from PIL import Image

import cv2

from . separator import Separator
from . sorting import BubbleSemiSort
from . exceptions import UnknownAlgorithmException

import time
import numpy
import os


def build_frame(divider: Separator):
    buffer_image = Image.new('RGB', ( divider.image_width, divider.image_height ), (255, 255, 255))

    for segment_y in range(divider.rows):
        current_width = 0
        current_height = segment_y*divider.segment_height
        for segment_x in range(divider.columns):
            segment = divider.get_segment(segment_x, segment_y)
            buffer_image.paste(segment['region'], (current_width, current_height))
            current_width += segment['pos_size'][2] - segment['pos_size'][0]

    return buffer_image


def build_gif_animation(image_path: str, settings: dict, anim_name: str, output: str):
    start_time = time.time()
    sep = Separator(image_path, settings)

    result_anim_name = anim_name + '.gif'

    algorithm = None
    if settings['algorithm'] == "Bubble":
        algorithm = BubbleSemiSort()
    else:
        raise UnknownAlgorithmException("Unknown or undefined type of algorithm was specified")

    steps = []
    for row in sep.row_arrays:
        steps.append(algorithm.get_all_iterations(row))

    frames = []

    for phase in range(len(steps[0])):
        for row in range(len(sep.row_arrays)):
            sep.row_arrays[row] = steps[row][phase]
        frame = build_frame(sep)
        frames.append(frame)

    frames[-1].save(os.path.join(output, result_anim_name), save_all=True,
                    append_images=frames[0:-1], optimize=False, duration=500, loop=1)

    print('It tooks ' + str(time.time() - start_time))

    return result_anim_name


def build_animation(image_path: str, settings: dict, video_name: str, extention: str, output: str):
    start_time = time.time()
    sep = Separator(image_path, settings)

    result_video = video_name + '.' + extention

    out = cv2.VideoWriter(os.path.join(output, result_video), cv2.VideoWriter_fourcc(*'DIVX'),
                          30, (sep.image_width, sep.image_height))

    algorithm = None
    if settings['algorithm'] == "Bubble":
        algorithm = BubbleSemiSort()
    else:
        raise UnknownAlgorithmException("Unknown or undefined type of algorithm was specified") 
    
    steps = []
    
    for row in sep.row_arrays:
        steps.append(algorithm.get_all_iterations(row))

    def add_frame(frame, repeat=1):
        for x in range(repeat):
            opencv_image = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)
            out.write(opencv_image)
    
    frame = build_frame(sep)
    add_frame(frame, repeat=5)

    for phase in range(len(steps[0])):
        for row in range(len(sep.row_arrays)):
            sep.row_arrays[row] = steps[row][phase]
        frame = build_frame(sep)
        add_frame(frame, repeat = 1 if phase != len(steps[0])-1 else 5)

    out.release()

    print('It tooks ' + str(time.time() - start_time))

    return result_video
