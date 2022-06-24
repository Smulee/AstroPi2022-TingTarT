import cv2
from PIL import Image, ImageEnhance, ImageStat
import numpy as np
import keyboard


def empty():
    pass


factor = 1.863
number = 0
lower = np.array([0, 0, 0])
upper = np.array([179, 255, 255])
seed = (0, 0)
rep_value = (0, 0, 0, 0)

#Image Paths
opencv_imageISS = cv2.imread(r"[Insert ISS image]")
opencv_imageMODIUS = cv2.imread(r"[Insert Modis Image]")

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640,240)
cv2.createTrackbar("Hue Min", "TrackBars", 0,179,empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179,179,empty)
cv2.createTrackbar("Sat Min", "TrackBars", 110,255,empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255,empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255,empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255,empty)

while True:
    imgAdjust = cv2.resize(opencv_imageISS,(680,400))
    imgHSV = cv2.cvtColor(imgAdjust,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(imgAdjust, imgAdjust, mask=mask)

    cv2.imshow('original', imgAdjust)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', imgResult)
    cv2.waitKey(1)
    if keyboard.is_pressed("enter"):
        break

cv2.destroyAllWindows()
imgHSV = cv2.cvtColor(opencv_imageISS,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(imgHSV,lower,upper)
opencv_imageISS = cv2.bitwise_and(opencv_imageISS, opencv_imageISS, mask=mask)
opencv_imageISS = cv2.cvtColor(opencv_imageISS,cv2.COLOR_BGR2HSV)
opencv_imageISS = cv2.cvtColor(opencv_imageISS,cv2.COLOR_BGR2GRAY)

PIL_imageISS = cv2.cvtColor(opencv_imageISS, cv2.COLOR_BGR2RGB)
PIL_imageMODIUS = cv2.cvtColor(opencv_imageMODIUS, cv2.COLOR_BGR2RGB)

PIL_imageISS = Image.fromarray(PIL_imageISS)
PIL_imageMODIUS = Image.fromarray(PIL_imageMODIUS)

ni = np.array(PIL_imageMODIUS)
blues = ni[:,:,2]>10

imgMaskMOBIUS = Image.fromarray((blues*255).astype(np.uint8))
im = PIL_imageMODIUS.convert('L')
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(1)
stat = ImageStat.Stat(im, imgMaskMOBIUS)
brightLevelMOBIUS = stat.rms[0]

ni = np.array(PIL_imageISS)
blues = ni[:,:,2]>10
imgMaskISS = Image.fromarray((blues*255).astype(np.uint8))


im = PIL_imageISS.convert('L')
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(factor)
stat = ImageStat.Stat(im, imgMaskISS)
brightLevelISS = stat.rms[0]
print("MOBIUS: ",brightLevelMOBIUS, "ISS: ",brightLevelISS)

imgMaskISS.show()
PIL_imageISS.show()
im.show()
