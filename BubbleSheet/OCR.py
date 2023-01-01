# import from skimage
from skimage.color import rgb2gray
from skimage.filters import sobel, sobel_h, sobel_v, prewitt, roberts, gaussian
from skimage.feature import canny
import skimage.io as io
import cv2 as cv
import pytesseract
import pickle
import knn
from scipy.spatial import distance as dist

# import from matplotlib
import matplotlib.pyplot as plt

# import from numpy
import numpy as np

# import utils
from utils.commonfunctions import *

#import pandas
import pandas as pd

class OCR:
    def __init__(self, debug):
        self.debug = debug
    def run(self, white_img_contours_IDBox, img_cpy):
        return self.get_student_id_name(white_img_contours_IDBox, img_cpy)

    def get_student_id_name(self, white_img_contours_IDBox, img_cpy):
        boxes_dimensions = self.Extract_Boxes(
            white_img_contours_IDBox, img_cpy)
        boxes_croped_images = []
        boxes_dimensions = reversed(
            sorted(boxes_dimensions, key=lambda dimension: boxes_dimensions[0]))
        for dimension in boxes_dimensions:
            if self.debug:
                print("dimension = ", dimension)
            (x, y, w, h) = dimension
            boxes_croped_images.append(img_cpy[y:y+h, x:x+w])
        ###########################################
        blurredImg = cv.medianBlur(boxes_croped_images[1], 3)
        kernel = np.ones((3, 3))
        dilatedImg = erode(blurredImg, kernel)
        if self.debug:
            show_images([boxes_croped_images[1], blurredImg, dilatedImg])
        ###########################################
        segmented_dimensions, filtered_img = self.segment_ID(
            255 - 255*blurredImg)
        ###########################################
        cropped_digits = []
        i = 0
        for dimension in segmented_dimensions:
            (x, y, w, h) = dimension
            cropped_digits.append(filtered_img[y-1:y+h+1, x-1:x+w+1])
            #cv.imwrite(str(i)+".jpg", filtered_img[y-1:y+h+1, x-1:x+w+1])
            i += 1
        if self.debug:
            show_images(cropped_digits)
        ###########################################
        model = self.load_pickle()
        for i in range(len(cropped_digits)):
            cropped_digits[i] = cv.resize(cropped_digits[i], (200, 100))
            cropped_digits[i] = cv.resize(
                cropped_digits[i], None, fx=3, fy=3, interpolation=cv.INTER_CUBIC)
        student_id = ""
        if len(cropped_digits) != 0:
            image_fv = knn.images_to_feature_vectors(cropped_digits)
            labels = knn.classify(model, image_fv, 3)
            student_id = knn.mapChars(listOfChars=labels)
        return student_id, boxes_croped_images[0]

    def Extract_Boxes(self, img, img_cpy):
        kernel = np.ones((15, 15))
        erodedImg = erode(img, kernel)

        contours, hierarchy = cv.findContours(
            (255 - erodedImg*255).astype("uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        white_img_large_contours = np.ones(img_cpy.shape)
        # computes the bounding box for the contour, and draws it on the frame,
        dimensions_contours = []
        sorted_contours = sorted(contours, key=cv.contourArea)
        for i in range(2):
            contour = sorted_contours[len(sorted_contours) - i - 1]
            (x, y, w, h) = cv.boundingRect(contour)
            dimensions_contours.append((x, y, w, h))
            cv.rectangle(white_img_large_contours,(x, y), (x+w, y+h), (0, 0, 0), 2)
        return dimensions_contours

    def segment_ID(self, img):
        img = cv.normalize(img, None, alpha=0, beta=255,norm_type=cv.NORM_MINMAX)
        res, img = cv.threshold(img, 64, 255, cv.THRESH_BINARY)
        # Fill everything that is the same color (black) as top-left corner with white
        cv.floodFill(img, None, (0, 0), 255)
        # Fill everything that is the same color (white) as top-left corner with black
        cv.floodFill(img, None, (0, 0), 0)
        contours, hierarchy = cv.findContours((img).astype(
            "uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=lambda ctr: cv.boundingRect(ctr)[0])
        white_img_large_contours = np.ones(img.shape)
        dimensions_contours = []
        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if(w*h > 20):
                dimensions_contours.append((x, y, w, h))
                cv.rectangle(white_img_large_contours,
                             (x, y), (x+w, y+h), (0, 0, 0), 2)
        return dimensions_contours, img

    def load_pickle(self) -> dict:
        a_file = open("./BubbleSheet/data.pkl", "rb")
        model = pickle.load(a_file)
        return model
