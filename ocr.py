from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import cv2 
import cv2 as cv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import argparse
import csv

# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# # TESSDATA = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

######################## OCR PDF ##########################
# from pdf2image import convert_from_path, convert_from_bytes
# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract
# from pytesseract import Output
# images = convert_from_path('Facture.pdf')
# print ("Nombre de pages: " + str(len(images)))
# for i in range (len(images)):
#     print ("Page N�" + str(i+1) + "\n")
#     print(pytesseract.image_to_string(images[i]))
######################## OCR PDF ##########################

IMAGE_PATH = 'fdp.jpg'
image = cv2.imread(IMAGE_PATH)

#converting image into gray scale image
custom_config = r'--oem 3 --psm 6'

# now feeding image to tesseract
details = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config, lang='fra')

# print(details.keys())
total_boxes = len(details['text'])

for sequence_number in range(total_boxes):
	if int(float(details['conf'][sequence_number])) > 30:
		(x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
		threshold_img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


# cv2.imshow('img',threshold_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
plt.figure(figsize=(10,10))
plt.imshow(threshold_img)
plt.show()

parse_text = []
word_list = []
last_word = ''

for word in details['text']:
    if word!='':
        word_list.append(word)
        last_word = word
        
    if (last_word!='' and word == '') or (word==details['text'][-1]):
        parse_text.append(word_list)
        word_list = []

with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)