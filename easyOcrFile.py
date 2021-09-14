import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import re

# IMAGE_PATH = r'img_7.jpg'

IMAGE_PATH = r'rotimage.jpg'



img = cv2.imread(IMAGE_PATH)


reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext(IMAGE_PATH)
textFromImage = [row[1] for row in result]
tempFromImage = [int(re.findall('\d\d', row[1])[0]) for row in result if re.search('\d\d+', row[1])]


print(textFromImage)
print(tempFromImage)

maxTemp, minTemp = -1000, 1000
if not (len(tempFromImage) < 2):
    for temp in tempFromImage:
        if temp > 10 and maxTemp < temp:
            maxTemp = temp
        if 10 < temp < minTemp:
            minTemp = temp

for res in result:
    top_left = tuple(res[0][0])
    bottom_right = tuple(res[0][2])
    text = res[1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
    img = cv2.putText(img, text, top_left, font, .5, (255, 255, 255), 2, cv2.LINE_AA)


top_left = tuple(result[0][0][0])
# bottom_right = tuple(result[0][0][2])
# text = result[0][1]
font = cv2.FONT_HERSHEY_SIMPLEX
# img = cv2.imread(IMAGE_PATH)
# img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
# img = cv2.putText(img, str(maxTemp) + ' & ' + str(minTemp), top_left, font, .5, (255, 255, 255), 2, cv2.LINE_AA)
print(str(maxTemp) + ' & ' + str(minTemp))

plt.imshow(img)
plt.show()

# cv2.imshow('image', img)

print('Hello, World')