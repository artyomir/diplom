import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import re
import os
import glob

from os import listdir
from os.path import isfile, join

def readTempFromImage (IMAGE_PATH):
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(IMAGE_PATH)
    tempFromImage = [int(re.findall('\d\d', row[1])[0]) for row in result if re.search('\d\d+', row[1])]
    if len(tempFromImage) == 1:
        return tempFromImage[0]
    else:
        return None

def cleanImage (img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(img, bg, scale=255)
    # return cv2.threshold(se, 0, 255, cv2.THRESH_OTSU)[1]
    return img

def FindMinMaxTemp (img):
    height, width, sheet = img.shape
    img_topLeft = img[0:35, 35:80]
    img_botLeft = img[height - 35:height, 35:80].cleanImage(img_topLeft)

    img_topLeft = cleanImage(img_topLeft)
    img_botLeft = cleanImage(img_botLeft)

    cv2.imwrite(r'cutImage/topLeft.jpg', img_topLeft)
    cv2.imwrite(r'cutImage/botLeft.jpg', img_botLeft)

    minT = readTempFromImage(r'cutImage/topLeft.jpg')
    maxT = readTempFromImage(r'cutImage/botLeft.jpg')

    return minT, maxT

def MinMaxTempExe (IMAGE_PATH):
    print(IMAGE_PATH.split('\\')[len(IMAGE_PATH.split('\\')) - 1])
    # logstr.append(IMAGE_PATH.split('\\')[2] + " - ")
    img = cv2.imread(IMAGE_PATH)

    minT, maxT = FindMinMaxTemp(img)

    for i in range(0, 3):
        if minT is None or maxT is None:
            img = np.rot90(img)
            minT, maxT = FindMinMaxTemp(img) # #              #dsfsdfasdasdin this casein this case

    cv2.imwrite(IMAGE_PATH, img)
    print(minT, maxT)
    # logstr.append('min: ' + str(minT) + ', ')
    # logstr.append('max: ' + str(maxT) + '\n')

def fragmentsTempBar(fragmentsAmount):
    if fragmentsAmount < 1:
        return
    img = cv2.imread(r'cutImage/tempBar.jpg')
    height, width, sheet = img.shape
    fragmentHeight = height / fragmentsAmount
    for i in range(0, fragmentsAmount):
        print(i)
        start = int(fragmentHeight * i)
        end = int(fragmentHeight + fragmentHeight * i)
        centery = int(fragmentHeight/2)
        centerx = int(width / 2)
        barFragment = img[start: end, 0:10]
        deltaHeight = 0
        # if i != 0:
        #     remPixImg = cv2.imread(r'bar_fragments/fragment_' + str(i - 1) + '.jpg')
        #     remPixImgheight, remPixImgwidth, sheet = remPixImg.shape
        #     p = remPixImg[remPixImgheight - 1, 0]
        #     while True:
        #         if np.all(barFragment[deltaHeight, 0] != p):
        #             break
        #         deltaHeight = deltaHeight + 1
        #     barFragment = barFragment[deltaHeight: end, 0:10]

        height, width, sheet = barFragment.shape

        print('added')

        cv2.imwrite('bar_fragments/fragment_' + str(i) + '.jpg', barFragment)




def CutTermogramm (IMAGE_PATH):
    files = glob.glob('bar_fragments/*')
    for f in files:
        os.remove(f)

    img = cv2.imread(IMAGE_PATH)
    height, width, sheet = img.shape
    tempBar = img[0:height, 0:30]
    thermoImg = img[0:height, 120:width]

    # ksize = (30, 30)
    # thermoImg = cv2.blur(thermoImg, ksize)

    cv2.imwrite(r'cutImage/tempBar.jpg', tempBar)
    cv2.imwrite(r'cutImage/thermoImg.jpg', thermoImg)

    return tempBar, thermoImg

def reColorImage (IMAGE_PATH):
    img = cv2.imread(IMAGE_PATH)
    height, width, sheet = img.shape
    print(height, 'X', width)
    for i in range(int(height/2), height):
        print('find row #', i)
        for j in range(0, width):
            print('find pixel #', i, j)
            pixel = findPixel(img[i][j])
            if pixel is not None:
                img[i][j] = pixel
        if i > 700:
            break
    cv2.imwrite('cutImage/finalTempImage.jpg', img)

def findPixel (pixel):
    for imgNum in range(0, 10):
        img = cv2.imread('bar_fragments/fragment_' + str(imgNum)+'.jpg')
        height, width, sheet = img.shape
        for i in range(0, height):
            if np.all(pixel == img[i][0]):
                centery = height / 2
                centerx = width / 2
                return img[int(centery), int(centerx)]
    return None



files = glob.glob('bar_fragments/*')
for f in files:
    os.remove(f)
IMAGE_PATH = r'D:\Seek Thermal\img_100.jpg'

CutTermogramm(IMAGE_PATH)
fragmentsTempBar(10)

