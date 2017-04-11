import cv2
import numpy as np
import os, sys
import RPi.GPIO as gpio 

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
try:
 gpio.setup(26, gpio.IN, gpio.PUD_UP) # y positionr 
except:
 print('Failed GPIO initialization')

try:
 cap = cv2.VideoCapture(0)
except:
 try:
  cap = cv2.VideoCapture(1)
 except:
  try:
   cap = cv2.VideoCapture(2)
  except:
   print('no camera')
   sys.exit()

def vision():
 c = 0
 while(1):
  ret, frame = cap.read()
  cv2.imshow('_', frame)
  if gpio.input(26) == 0:
   cv2.imwrite( str(c) + '.png', frame )
   c += 1
  cv2.waitKey(10)

def exit():
 cap.release()
 cv2.destroyAllWindows()
 sys.exit()

