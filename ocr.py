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
        conf = '--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789'
    else:
        conf = ""

    for filename in os.scandir(dir):

        ocrOutput = pytesseract.image_to_string(
            Image.open(filename.path), lang=langSelected, config=conf)

        if(langSelected == 'ara'):
            arabicText = get_display(ocrOutput)
            ocrOutput = arabic_reshaper.reshape(arabicText)
        if(len(ocrOutput) != 0 and type != None):
            result.append(ocrOutput[0])
        elif (type != None):
            result.append(0)
        else:
            result.append(ocrOutput)

    return result
