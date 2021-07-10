#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cv2 as cv
from PIL import Image, ImageSequence
import numpy as np

if __name__ == "__main__":
	gif = Image.open("./res/1.gif")
	gif_w = gif.width
	gif_h = gif.height
	
	# 获取gif带有alpha通道每一帧
	gif.resize((int(gif.height * 0.7), int(gif.width * 0.7)), Image.ANTIALIAS)
	gifs = []
	mask = Image.new("RGBA", gif.size, (255, 255, 255, 0))
	for frame in ImageSequence.Iterator(gif):
		f = frame.convert("RGBA")  # 加上alpha通道
		f = np.array(Image.alpha_composite(mask, f))  # 转为opencv格式图片
		f = cv.cvtColor(f, cv.COLOR_RGBA2BGRA)  # 改变颜色格式
		gifs.append(f)
	
	video = cv.VideoCapture("./res/test.mp4")
	if video.isOpened():
		width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
		height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
		fps = int(video.get(cv.CAP_PROP_FPS))
		fs = int(video.get(cv.CAP_PROP_FRAME_COUNT))
		channel = 3
		
		writer = cv.VideoWriter("./out.avi", cv.VideoWriter_fourcc(*"DIVX"), fps, (width, height), True)
		ret, frame = video.read()
		cursor = 0
		
		video_show_region_width = 0
		video_show_region_x = 0
		gif_show_x = gif_w
		gif_show_width = gif_w
		step = 2
		while ret:
			# TODO 调整step，使得gif走到最后的时候视频结束
			# TODO 虽然gif的每一帧都是有透明通道，但是放上去后依然没有透明，因此需要进一步修改
			# FIXME step为3时报错，判断条件比较狭窄，寻求更好的算法中……
			frame = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
			
			if video_show_region_x + gif_w >= width:  # gif右边缘到达视频右边缘
				# 先减了显示区域再执行赋值操作，不然会出错
				video_show_region_width -= step
				gif_show_width -= step
				
				frame[height - gif_h:, video_show_region_x:video_show_region_x + gif_show_width:, :] \
					= (gifs[cursor])[:, 0:gif_show_width:, :]
				
				video_show_region_x += step
			elif video_show_region_width <= gif_w:  # gif左边缘还未到达或刚到达视频左边缘
				frame[height - gif_h:, 0:video_show_region_width, :] \
					= (gifs[cursor])[:, gif_show_x:gif_show_x + video_show_region_width, :]
				
				video_show_region_width += step
				gif_show_x -= step
			elif video_show_region_width > gif_w:  # gif已全部进入视频区域
				frame[height - gif_h:, video_show_region_x:video_show_region_x + gif_w, :] = gifs[cursor]
				video_show_region_x += step
			
			cursor = (cursor + 1) % len(gifs)
			writer.write(frame)
			# cv.imshow("d", frame)
			cv.waitKey(int(fps))
			# break
			ret, frame = video.read()
		else:
			video.release()
