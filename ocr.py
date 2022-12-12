import pytesseract
from PIL import Image
import os


def ocrEnglish(dir):

    # temp directory till put in env. variables
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR.\tesseract.exe'
    for filename in os.scandir(dir):
        try:
            # print(pytesseract.image_to_string(Image.open('Cells\EnglishName\d.jpg')))
            print(pytesseract.image_to_string(filename.path))
        except Exception:
            print("Error!")


# ocrEnglish("Cells\EnglishName")
# ocrEnglish("Cells\Code")
# ocrEnglish("Cells\StudentName")