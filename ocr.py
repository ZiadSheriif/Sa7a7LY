import pytesseract
from bidi.algorithm import get_display
import arabic_reshaper


def ocr(images, langSelected):
    result = []

    for img in images:
        try:
            res = pytesseract.image_to_string(img, lang=langSelected)
            if(langSelected == 'ara'):
                arabicText = get_display(res)
                res = arabic_reshaper.reshape(arabicText)
            result.append(res)
        except Exception:
            print("Error!")
    return result
