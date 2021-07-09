#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2 as cv
from PIL import Image, ImageSequence
import numpy as np
import ffmpy3 as ff

if __name__ == "__main__":
    # 获取gif带有alpha通道每一帧
    gif = cv.VideoCapture("./res/0.gif")
    gifs = []
    mask = Image.new("RGBA", gif.size, (255, 255, 255, 0))
    for frame in ImageSequence.Iterator(gif):
        f = frame.convert("RGBA")
        gifs.append(np.array(Image.alpha_composite(mask, f)))

    video = cv.VideoCapture("./res/test.mp4")
    if video.isOpened():
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = int(video.get(cv.CAP_PROP_FPS))
        channel = 3

        writer = cv.VideoWriter("./out.mp4", cv.VideoWriter_fourcc(*"h264"),
                                fps, (width, height), True)

        ret, frame = video.read()
        while ret:
            # TODO 给视频每一帧底部加上gifs的每一帧

            writer.write(frame)
            ret, frame = video.read()
        else:
            video.release()
