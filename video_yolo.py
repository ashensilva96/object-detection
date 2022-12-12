import torch
import os
from PIL import Image
import cv2

VIDEO_CAP = cv2.VideoCapture('./videos/paris_test_s.mp4')

frame_width = int(VIDEO_CAP.get(3))
frame_height = int(VIDEO_CAP.get(4))
   
size = (frame_width, frame_height)

result = cv2.VideoWriter('car_detect.mp4', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

while(True):
    ret, frame = VIDEO_CAP.read()
    if ret == True: 
  
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s') #load yolov5s model
        model.classes = 2                                       #select car class
        results = model(frame)                              #feed converted image to the model
        results.render()
        #results.save()

        result.write(results)
  
    # Break the loop
    else:
        break
  
VIDEO_CAP.release()
result.release()

print("The video was successfully saved")

