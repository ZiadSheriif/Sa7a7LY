# import libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from os import listdir
from os.path import isfile, join
from utils.commonfunctions import *
mpl.rcParams['image.cmap'] = 'gray'


def getLines(img, binaryImg, x):
    # global horizontalLinesImg, verticalLinesImg, kernel

    # Kernel Length
    kernelLength = np.array(img).shape[1] // x

    # Vertical Kernel (1 x kernelLength)
    verticalKernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernelLength))

    # Horizontal Kernel (kernelLength x 1)
    horizontalKernel = cv.getStructuringElement(
        cv.MORPH_RECT, (kernelLength, 1))

    # Apply erosion then dilation to detect vertical lines using the vertical kernel
    erodedImg = cv.erode(binaryImg, verticalKernel, iterations=3)
    verticalLinesImg = cv.dilate(erodedImg, verticalKernel, iterations=3)
    cv.imwrite("Outputs/vertical_lines.jpg", verticalLinesImg)

    # Apply erosion then dilation to detect horizontal lines using the horizontal kernel
    erodedImg = cv.erode(binaryImg, horizontalKernel, iterations=3)
    horizontalLinesImg = cv.dilate(erodedImg, horizontalKernel, iterations=3)
    cv.imwrite("Outputs/horizontal_lines.jpg", horizontalLinesImg)

    plt.subplot(1, 2, 1)
    plt.imshow(verticalLinesImg)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(horizontalLinesImg)
    plt.axis('off')
    return verticalLinesImg


def getIntersections(pixels):
    intersections = []
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            if pixels[i][j] != 0:
                intersections.append((i, j))
    return intersections


def hough_line(img):
    # print(img)
    lines = cv.HoughLinesP(img.astype(
        np.uint8), 0.5, np.pi/180, 100, minLineLength=0.25*min(img.shape[0], img.shape[1]), maxLineGap=10)
    print(lines)

    hough_lines_out = np.zeros(img.shape)
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line[0]
        cv.line(hough_lines_out, (x1, 0),
                (x2, img.shape[1]), (255, 255, 255), 2)
    return hough_lines_out


def run(img):
    imgTemp = cv.imread(img, 0)

    # thresholding
    (thresh, binaryImg) = cv.threshold(
        imgTemp, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binaryImg = 255 - binaryImg
    cv.imwrite("Outputs/Binary_img.jpg", binaryImg)
    plt.axis('off')
    plt.imshow(binaryImg)

    verticalLinesImg = getLines(imgTemp, binaryImg, x=7)
    verticalLinesImg = hough_line(verticalLinesImg)
    cv.imwrite("trial/vert.jpg", verticalLinesImg)
    return verticalLinesImg


def run_extract_grid():
    mypath = "grid"
    write_path = "Outputs/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    for file in onlyfiles:
        print(mypath+"/"+file)
        result_image = run(mypath+"/"+file)
        cv.imwrite(write_path+file, result_image)


run_extract_grid()
