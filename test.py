import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import re
import os

from os import listdir
from os.path import isfile, join

def readTempFromImage (IMAGE_PATH):
    reader = easyocr.Reader(['en'], gpu=False)
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

def WriteMinMax (img):
    height, width, sheet = img.shape
    img_topLeft = img[0:35, 35:80]
    img_botLeft = img[height - 35:height, 35:80]

    img_topLeft = cleanImage(img_topLeft)
    img_botLeft = cleanImage(img_botLeft)

    cv2.imwrite(r'cutImage/topLeft.jpg', img_topLeft)
    cv2.imwrite(r'cutImage/botLeft.jpg', img_botLeft)

def getMinMax (IMAGE_PATH, IMAGE_MAX, IMAGE_MIN):
    print(IMAGE_PATH.split('\\')[len(IMAGE_PATH.split('\\')) - 1])
    # logstr.append(IMAGE_PATH.split('\\')[2] + " - ")
    img = cv2.imread(IMAGE_PATH)
    height, width, sheet = img.shape
    if height < width:
        assert isinstance(img, object)
        img = np.rot90(img)

    WriteMinMax(img)

    minT, maxT = None, None

    minT = readTempFromImage(IMAGE_MIN)
    maxT = readTempFromImage(IMAGE_MAX)

    if minT is None or maxT is None:
        img = np.rot90(img)
        img = np.rot90(img)
        WriteMinMax(img)
        minT = readTempFromImage(IMAGE_MIN)
        maxT = readTempFromImage(IMAGE_MAX)

    cv2.imwrite(IMAGE_PATH, img)
    print(minT, maxT)
    # logstr.append('min: ' + str(minT) + ', ')
    # logstr.append('max: ' + str(maxT) + '\n')

IMAGE_PATH = r'D:\Seek Thermal\img_162.jpg'
IMAGE_MAX = r'cutImage/topLeft.jpg'
IMAGE_MIN = r'cutImage/botLeft.jpg'

mypath = r'D:\Seek Thermal'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

iter = 0
my_file_handle = open(r'D:\pytest\logs', mode="a+", encoding="utf-8")
logstr = []

getMinMax(IMAGE_PATH, IMAGE_MAX, IMAGE_MIN)
# for file in onlyfiles:
#     print(IMAGE_PATH.split('\\')[len(IMAGE_PATH.split('\\')) - 1])
#     logstr.append(IMAGE_PATH.split('\\')[2] + " - ")
#     img = cv2.imread(IMAGE_PATH)
#     height, width, sheet = img.shape
#     if height < width:
#         assert isinstance(img, object)
#         img = np.rot90(img)
#
#     WriteMinMax(img)
#
#     minT, maxT = None, None
#
#     minT = readTempFromImage(IMAGE_MIN)
#     maxT = readTempFromImage(IMAGE_MAX)
#
#     if minT is None or maxT is None:
#         img = np.rot90(img)
#         img = np.rot90(img)
#         WriteMinMax(img)
#         minT = readTempFromImage(IMAGE_MIN)
#         maxT = readTempFromImage(IMAGE_MAX)
#
#     cv2.imwrite(IMAGE_PATH, img)
#     print(minT, maxT)
#     logstr.append('min: ' + str(minT) + ', ')
#     logstr.append('max: ' + str(maxT) + '\n')


