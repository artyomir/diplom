import cv2
import pytesseract

image = cv2.imread(r'binary.png')
ret,thresh = cv2.threshold(image,55,255,cv2.THRESH_BINARY)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)))
cv2.imshow('result_1.jpg', opening)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(opening)
print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()

