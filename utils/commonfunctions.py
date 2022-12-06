

import skimage.io as io
import matplotlib.pyplot as plt
import numpy as np
from skimage.exposure import histogram
from matplotlib.pyplot import bar
from skimage.color import rgb2gray, rgb2hsv

# Convolution:
from scipy.signal import convolve2d
from scipy import fftpack
import math

from skimage.util import random_noise
from skimage.filters import median
from skimage.feature import canny

import cv2 as cv
# Edges
from skimage.filters import sobel_h, sobel, sobel_v, roberts, prewitt

# Show the figures / plots inside the notebook


def show_images(images, titles=None):
    # This function is used to show image(s) with titles by sending an array of images and an array of associated titles.
    # images[0] will be drawn with the title titles[0] if exists
    # You aren't required to understand this function, use it as-is.
    n_ims = len(images)
    if titles is None:
        titles = ['(%d)' % i for i in range(1, n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image, title in zip(images, titles):
        a = fig.add_subplot(1, n_ims, n)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()


def showHist(img):
    # An "interface" to matplotlib.axes.Axes.hist() method
    plt.figure()
    imgHist = histogram(img, nbins=256)

    bar(imgHist[1].astype(np.uint8), imgHist[0], width=0.8, align='center')



def gaussianFilter(img):
    #     newImg = gaussian(img, sigma=1,mode='nearest', cval=0, preserve_range=False, truncate=4.0)
    newImg = cv.GaussianBlur(img,(5,5),0)
    return newImg

def cannyEdge(img,sigma=1,thres1=100,thres2=200):
    #     edges = abs(canny(img,sigma = sigma))
    #     img = (img*255).astype(np.uint8)
    edges = cv.Canny(img,thres1,thres2,L2gradient = True)
    return edges

def adaptiveThresholding(img):
    #     img = (img*255).astype(np.uint8)
    filteredImg = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    return filteredImg


def closing(img, kernel):
    closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    return closing


def opening(img, kernel):
    closing = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    return closing

def dilate(img, kernel):
    closing = cv.dilate(img, kernel, iterations=1)
    return closing

def erode(img, kernel):
    closing = cv.erode(img, kernel, iterations=1)
    return closing
