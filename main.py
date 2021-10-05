import cv2
import numpy as np
import glob

from cv2 import imshow
from PIL import Image, ImageFilter

import re
import skimage.io as sk
from skimage import img_as_float, img_as_ubyte
from numpy import clip, dstack, asarray
from matplotlib.colors import rgb2hex

# img = cv2.imread(r'cutImage\thermoImg.jpg')

def recolor(img, IMAGE_PATH):
    colorsImg = Image.open(IMAGE_PATH)
    data = np.array(img)
    colorsData = np.array(colorsImg)

    print(colorsData[0][0])

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    r2, g2, b2 = int(colorsData[0][0][0]), int(colorsData[0][0][1]), int(colorsData[0][0][2])

    for row in colorsData:
        r1, g1, b1 = int(row[0][0]), int(row[0][1]), int(row[0][2])
        mask = (abs(red - r1) < 20) & (abs(green - g1) < 20) & (abs(blue - b1) < 20)
        data[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(data)

# def recolorHSV(img, IMAGE_PATH):
#     colorImage =


def recolorExe(IMAGE_PATH):
    img = Image.open(IMAGE_PATH)
    img = img.filter(ImageFilter.GaussianBlur(5))
    files = glob.glob('bar_fragments/*')

    for i in range(0, len(files)):
        img = recolor(img, 'bar_fragments/fragment_'+str(i)+'.jpg')
        img.save('finalImages/newimg_'+str(i)+'.jpg')
    img.save('finalImages/finalImage_.jpg')

# imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# cv2.imwrite(r'newimg_1.jpg', img)