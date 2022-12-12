import pytesseract
from PIL import Image
import os
from bidi.algorithm import get_display
import arabic_reshaper
import sys


def ocr(dir, lang):

    # temp directory till put in env. variables
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR.\tesseract.exe'
    for filename in os.scandir(dir):
        try:
            res = pytesseract.image_to_string(
                Image.open(filename.path), lang=lang)
            if(lang == 'ara'):
                res = res[::-1]
            print(res)
        except Exception:
            print("Error!")

    # print(pytesseract.image_to_string(filename.path))
    # ocrEnglish("Cells\EnglishName")
    # ocrEnglish("Cells\Code")
    # ocrEnglish("Cells\StudentName")
