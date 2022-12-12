import pytesseract
from PIL import Image
import os
from bidi.algorithm import get_display
import arabic_reshaper


def ocr(dir, langSelected):

    # if it doesn't work :
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR.\tesseract.exe'
    result=[]

    for filename in os.scandir(dir):
        try:
            res = pytesseract.image_to_string(
                Image.open(filename.path), lang=langSelected)

            # print(arabic)
            if(langSelected == 'ara'):
                arabicText = get_display(res)
                res = arabic_reshaper.reshape(arabicText)
            result.append(res)
            # print(res)
        except Exception:
            print("Error!")
    return result
    # print(pytesseract.image_to_string(filename.path))
    # ocrEnglish("Cells\EnglishName")
    # ocrEnglish("Cells\Code")
    # ocrEnglish("Cells\StudentName")
