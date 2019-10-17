import picamera
import picamera.array
import numpy as np
import cv2
import os
from time import sleep
import time
# Color definitions
red = np.uint8([[[255, 0, 0]]])
green = np.uint8([[[0, 255, 0]]])
blue = np.uint8([[[0, 0, 255]]])
yellow = np.uint8([[[255, 255, 0]]])

red = cv2.cvtColor(red, cv2.COLOR_RGB2HSV)
green = cv2.cvtColor(green, cv2.COLOR_RGB2HSV)
blue = cv2.cvtColor(blue, cv2.COLOR_RGB2HSV)
yellow = cv2.cvtColor(yellow, cv2.COLOR_RGB2HSV)

low_red = red[0][0][0] - 15, 100, 100
high_red = red[0][0][0] + 15, 255, 255
low_green = green[0][0][0] - 35, 100, 100
high_green = green[0][0][0] + 20, 255, 255
low_blue = blue[0][0][0] - 40, 100, 100
high_blue = blue[0][0][0] + 20, 255, 255
low_yellow = yellow[0][0][0] - 10, 180, 180
high_yellow = yellow[0][0][0] + 10, 255, 255

num = np.array([0, 0, 0, 0, 300])
undefined = 300
color = ["red", "blue", "green", "yellow","undefined"]

nsplits = 24
if 'N_SPLITS' in os.environ:
    nsplits = int(os.environ['N_SPLITS'])

split_height = int(240/nsplits)

if ((float(240)/nsplits) - split_height)*100 != 0:
    uneven = True
else:
    uneven = False
print("%d horizontal splits" % (nsplits))

with picamera.PiCamera() as camera:
  camera.resolution = (320, 240)
  while True:
      start = time.time()
      with picamera.array.PiRGBArray(camera) as output:
          camera.capture(output, 'rgb')
          output = output.array
          output = cv2.cvtColor(output,cv2.COLOR_RGB2HSV) #hsv color space
          # You can now treat output as a normal numpy array
          # Do your magic here

          red_mask = cv2.inRange(output, low_red, high_red)
          blue_mask = cv2.inRange(output, low_blue, high_blue)
          green_mask = cv2.inRange(output, low_green, high_green)
          yellow_mask = cv2.inRange(output, low_yellow, high_yellow)
          print("The capture's most occuring colors in the splits are:")

          for i in range(0,nsplits-uneven):
              num[0] = np.sum(red_mask[:,i*split_height+1:(i+1)*split_height])
              num[1] = np.sum(blue_mask[:,i*split_height+1:(i+1)*split_height])
              num[2] = np.sum(green_mask[:,i*split_height+1:(i+1)*split_height])
              num[3] = np.sum(yellow_mask[:,i*split_height+1:(i+1)*split_height])
              #print(num[0],num[1],num[2],num[3])
              pos = num.argmax()
              print(color[pos])

              if (i == nsplits-1-uneven) and (uneven == True):
                  num[0] = np.sum(red_mask[:,(i+1)*split_height+1: ])
                  num[1] = np.sum(blue_mask[:,(i+1)*split_height+1: ])
                  num[2] = np.sum(green_mask[:,(i+1)*split_height+1: ])
                  num[3] = np.sum(yellow_mask[:,(i+1)*split_height+1: ])
                  #print(num[0],num[1],num[2],num[3])
                  pos = num.argmax()
                  print(color[pos])
          elapsed_time = time.time()-start
          sleep(1-elapsed_time)
          #print(elapsed_time)
