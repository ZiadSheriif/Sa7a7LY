# import libraries
from recognition.knn import classify_unlabelled_directory, mapChars
import matplotlib as mpl
from ocr import ocr
from extract_cells import runExtractCells
from Symbols.symbols import runDetectCells
from extract_grid_script import run_extract_grid
from recognition.codes import segmentCodes
import os

import xlwt
from xlwt import Workbook
# from utils.commonfunctions import *
mpl.rcParams['image.cmap'] = 'gray'

EnglishNameDir, CodeDir, StudentNameDir, numericalNumbersDir = "Cells/EnglishName/", "Cells/Code/", "Cells/StudentName/", "Cells/1/"
CODE_WIDTH, ARABIC_WIDTH, ENGLISH_WIDTH, NUMBERS_WIDTH, SYMBOL_WIDTH = 4000, 10000, 11000, 3000, 3000


def runExcel(codesChoice, digitsChoice):
    # Extract grid from table
    run_extract_grid()
    # Extract cells from grid
    columnsCount = runExtractCells()
    # Codes
    codes = []
    if (codesChoice == 1):
        codes = ocr(CodeDir, 'eng')
    else:
        for filename in os.scandir('./Cells/Code/'):
            res = segmentCodes(filename.path)
            codes.append(res)
    # Arabic Names
    arabicNames = ocr(StudentNameDir, 'Arabic')
    # English Names
    englishNames = ocr(EnglishNameDir, 'eng')
    # Digits
    numericalNumbers = []
    if (digitsChoice == 1):
        numericalNumbers = ocr(numericalNumbersDir, 'hand3', "**")
    else:
        numericalNumbers = classify_unlabelled_directory(numericalNumbersDir)
        numericalNumbers = mapChars(numericalNumbers)
    # Symbols
    symbols = runDetectCells(columnsCount - 4)

    style_center = xlwt.easyxf("align: vert centre, horiz centre")
    style_header = xlwt.easyxf(
        "align: vert centre, horiz centre; font: bold true; pattern: pattern solid, fore_colour gray25")
    style_red = xlwt.easyxf("pattern: pattern solid, fore_colour red")

    # Create Excel Sheet
    wb = Workbook()
    AutoFiller = wb.add_sheet('AutoFiller')
    AutoFiller.write(0, 0, 'Code', style_header)
    AutoFiller.write(0, 1, 'Student Name', style_header)
    AutoFiller.write(0, 2, 'English Name', style_header)
    AutoFiller.write(0, 3, 1, style_header)
    for i in range(columnsCount - 4):
        AutoFiller.write(0, 4 + i, i + 2, style_header)

    AutoFiller.col(0).width = CODE_WIDTH
    AutoFiller.col(1).width = ARABIC_WIDTH
    AutoFiller.col(2).width = ENGLISH_WIDTH
    AutoFiller.col(3).width = NUMBERS_WIDTH
    for i in range(columnsCount - 4):
        AutoFiller.col(i + 4).width = SYMBOL_WIDTH

    for index in range(1, len(codes)):
        AutoFiller.write(index, 0, int(codes[index]) if codes[index].isnumeric() else codes[index], style_center)

    for index in range(1, len(arabicNames)):
        AutoFiller.write(index, 1, arabicNames[index], style_center)

    for index in range(1, len(englishNames)):
        AutoFiller.write(index, 2, englishNames[index], style_center)

    for index in range(1, len(numericalNumbers)):
        AutoFiller.write(index, 3, int(numericalNumbers[index]) if numericalNumbers[index].isnumeric() else numericalNumbers[index], style_center)

    for i in range(len(symbols)):
        for index in range(1, len(symbols[i])):
            if (symbols[i][index] == "?"):
                AutoFiller.write(index, i + 4, " ", style_red)
            else:
                AutoFiller.write(index, i + 4, symbols[i][index], style_center)

    wb.save('autoFiller.xls')
