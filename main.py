import pytesseract
import cv2
import re

imagePath = r'img_thermal_1591962901684.jpg'
img = cv2.imread(imagePath)

img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
se=cv2.getStructuringElement(cv2.MORPH_RECT , (5,5))
bg=cv2.morphologyEx(img, cv2.MORPH_DILATE, se)

out_gray=cv2.divide(img, bg, scale=255)
out_binary=cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU )[1]

## Преобразование гуссиана
# image = cv2.imread(r'img_thermal_1591962901684.jpg', cv2.IMREAD_GRAYSCALE)
# image = cv2.GaussianBlur(image, (5,5), 1)
# image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,2)

## Удаляем все не черные пиксели
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image[image != 255] = 0 # change everything to white where pixel is not black
# threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# cv2.imshow('threshold_img', image)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(image)
matches = re.match('26', text)

print(text)
# print(matches.group(0))
cv2.imwrite('my_img2.jpeg', image)

cv2.waitKey(0)

cv2.destroyAllWindows()