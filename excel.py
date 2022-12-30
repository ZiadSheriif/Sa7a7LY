# import libraries
from recognition.knn import classify_unlabelled_directory, mapChars
import matplotlib as mpl
from ocr import ocr
from extract_cells import runExtractCells
from Symbols.symbols import runDetectCells
from recognition.codes import segmentCodes
import os

import xlwt
from xlwt import Workbook
# from utils.commonfunctions import *
mpl.rcParams['image.cmap'] = 'gray'

EnglishName, Code, StudentName = "Cells/EnglishName/", "Cells/Code/", "Cells/StudentName/"
CODE_WIDTH, ARABIC_WIDTH, ENGLISH_WIDTH, NUMBERS_WIDTH, SYMBOL1_WIDTH, SYMBOL2_WIDTH = 3000, 10000, 11000, 3000, 3000, 3000


def runExcel():
    # extract cells from table
    runExtractCells()
    #  test code
    codes = []
    for filename in os.scandir('./Cells/Code/'):
        res = segmentCodes(filename.path)
        print(res)
        codes.append(res)

    # codes = ocr(Code, 'eng')
    # test EnglishName
    englishNames = ocr(EnglishName, 'eng')
    # test Arabic Name
    arabicNames = ocr(StudentName, 'Arabic')
    # test digits Number
    numericalNumbers = classify_unlabelled_directory('./Cells/1/')
    numericalNumbers = mapChars(numericalNumbers)
    # detect symbols
    symbols = runDetectCells()

    style_center = xlwt.easyxf("align: vert centre, horiz centre")
    style_header = xlwt.easyxf("align: vert centre, horiz centre; font: bold true")
    style_red = xlwt.easyxf("pattern: pattern solid, fore_colour red")

    # create excel sheet
    wb = Workbook()
    AutoFiller = wb.add_sheet('AutoFiller')
    AutoFiller.write(0, 0, 'Code', style_header)
    AutoFiller.write(0, 1, 'StudentName', style_header)
    AutoFiller.write(0, 2, 'EnglishName', style_header)
    AutoFiller.write(0, 3, 1, style_header)
    AutoFiller.write(0, 4, 2, style_header)
    AutoFiller.write(0, 5, 3, style_header)

    AutoFiller.col(0).width = CODE_WIDTH
    AutoFiller.col(1).width = ARABIC_WIDTH
    AutoFiller.col(2).width = ENGLISH_WIDTH
    AutoFiller.col(3).width = NUMBERS_WIDTH
    AutoFiller.col(4).width = SYMBOL1_WIDTH
    AutoFiller.col(5).width = SYMBOL2_WIDTH

    for index in range(1, len(codes)):
        AutoFiller.write(index, 0, codes[index], style_center)

    for index in range(1, len(arabicNames)):
        AutoFiller.write(index, 1, arabicNames[index], style_center)

    for index in range(1, len(englishNames)):
        AutoFiller.write(index, 2, englishNames[index], style_center)

    for index in range(1, len(numericalNumbers)):
        AutoFiller.write(index, 3, int(numericalNumbers[index]), style_center)

    for index in range(1, len(symbols[0])):
        if (symbols[0][index] == "?"):
            AutoFiller.write(index, 4, " ", style_red)
        else:
            AutoFiller.write(index, 4, symbols[0][index], style_center)
    for index in range(1, len(symbols[1])):
        if (symbols[1][index] == "?"):
            AutoFiller.write(index, 5, " ", style_red)
        else:
            AutoFiller.write(index, 5, symbols[1][index], style_center)

    wb.save('autoFiller.xls')
