import pytesseract
from PIL import Image
import os
from bidi.algorithm import get_display
import arabic_reshaper


def ocr(dir, langSelected, type=None):

    # if it doesn't work :
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR.\tesseract.exe'
    result = []
    if type != None:
        conf = 'digits'
    else:
        conf = ""

    for filename in os.scandir(dir):
        try:
            res = pytesseract.image_to_string(
                Image.open(filename.path), lang=langSelected, config=conf)

            if(langSelected == 'ara'):
                arabicText = get_display(res)
                res = arabic_reshaper.reshape(arabicText)
            result.append(res)
        except Exception:
            print("Error!")
    return result
