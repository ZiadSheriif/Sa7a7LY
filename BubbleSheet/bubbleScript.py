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

import os
import shutil
from os import listdir
from os.path import isfile, join

import OCR

debug = False
# debug = True


class Bubble:
    def __init__(self, input_path, output_path, model_answer):
        self.input_path = input_path
        self.output_path = output_path
        self.model_answer = model_answer

    def run(self):
        # Define variables
        my_ocr = OCR.OCR(debug)

        # read image
        img = cv.imread(self.input_path, 0)
        ############################################
        # Apply canny edge detection
        cannyEdges = cannyEdge(img)
        # show_images([cannyEdges])
        ############################################
        # Apply adaptive threshold
        img_cpy = img.copy()
        img_cpy = cv.adaptiveThreshold(
            img_cpy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 59, 3)
        ############################################
        # Apply perspective transform
        transformedImg = self.apply_perspective_transform(
            cannyEdges, img, img_cpy)
        ############################################
        # use canny to detect edges
        cannyEdges = cannyEdge(transformedImg)
        # show_images([cannyEdges])
        ############################################
        img_cpy = transformedImg.copy()
        img_cpy = cv.adaptiveThreshold(
            img_cpy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 59, 3)
        # Get circles ,student id and name contours
        white_img_contours, white_img_contours_IDBox = self.get_circles_id_name_contours(
            img_cpy, cannyEdges, img)
        ###########################################
        # Get student id and name
        student_id, student_name = my_ocr.run(
            white_img_contours_IDBox, img_cpy)
        ###########################################
        kernel = np.ones((20, 20))
        erodedImg2 = erode(white_img_contours, kernel)

        kernel = np.ones((20, 20))
        dilatedImg = dilate(erodedImg2, kernel)

        kernel = np.ones((25, 25))
        erodedImg = erode(dilatedImg, kernel)
        #show_images([white_img_contours, dilatedImg, erodedImg, erodedImg2])
        ###########################################
        # Get all contours of the image
        dimensions_contours = self.get_contours_dimensions(erodedImg, img_cpy)
        ###########################################
        # Crop questions groups
        cropped_images = self.crop_groups(dimensions_contours, img_cpy)
        ###########################################
        # Crop answers from each group of questions
        contour_cropped_imgs, dimensions_cropped_imgs, contours_count = self.crop_answers(
            cropped_images)
        ###########################################
        # Get number of answers per question
        answer_count = self.get_number_of_answers_per_question(contours_count)
        ###########################################
        # Groups questions in groups with there answers
        groups_questions_answers = self.groups_questions(
            dimensions_cropped_imgs, cropped_images, answer_count)
        ###########################################
        # Group questions in groups and find answers
        questions_final_answers = self.get_student_answers(
            groups_questions_answers, answer_count)
        ###########################################
        # Write results to excel sheet
        self.write_excel(student_id, self.ocr(student_name),
                         questions_final_answers)
        ###########################################

    def get_circles_id_name_contours(self, img_cpy, cannyEdges, img):
        contours, hierarchy = cv.findContours(
            cannyEdges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        white_img_contours = np.ones(img_cpy.shape)
        white_img_contours_IDBox = np.ones(img_cpy.shape)
        TwoBox = []
        all_id_boxs = []
        sorted_contours = sorted(contours, key=cv.contourArea)
        count_boxes = 0

        max_contour = max(contours, key=cv.contourArea)
        max_contour_area = cv.contourArea(max_contour)
        #print("max_contour_area = ", max_contour_area)
        for contour in sorted_contours:
            x, y, w, h = cv.boundingRect(contour)
            if w/h >= 0.8 and w/h <= 1.3 and (cannyEdges.shape[0] * cannyEdges.shape[1] * 0.01) > w*h:
                # print("here")
                cv.rectangle(white_img_contours, (x, y),
                             (round(x+1.1*w), round(y+1.7*h)), (0, 0, 0), -1)
        #         cv.fillPoly(white_img_contours, pts =[contour], color=(0,0,0))
            elif w/h > 3 and (cannyEdges.shape[0] * cannyEdges.shape[1] * 0.2) > w*h:
                cv.fillPoly(white_img_contours_IDBox, pts=[
                            contour], color=(0, 0, 0))
                all_id_boxs.append((x, y, w, h))
                if(count_boxes < 2):
                    TwoBox.append((x, y, w, h))
                count_boxes += 1
        TwoBox = all_id_boxs[0:2]
        #print(len(TwoBox), len(all_id_boxs))
        # cv.fillPoly(white_img_contours_IDBox, pts =[TwoBox[0]], color=(0,0,0))
        # cv.fillPoly(white_img_contours_IDBox, pts =[TwoBox[1]], color=(0,0,0))
        if debug:
            show_images([white_img_contours, cannyEdges,
                        img, white_img_contours_IDBox])
        return white_img_contours, white_img_contours_IDBox

    def apply_perspective_transform(self, cannyEdges, img, img_cpy):
        contours, hierarchy = cv.findContours(
            cannyEdges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        sorted_contours = sorted(contours, key=cv.contourArea)

        c = max(sorted_contours, key=cv.contourArea)
        maxContourArea = cv.contourArea(c)

        image_area = img.shape[0] * img.shape[1]
        min_valid_contour_area = maxContourArea
        final_contour = c
        for contour in sorted_contours:
            contour_area = cv.contourArea(contour)
            peri = cv.arcLength(contour, True)
            if contour_area > 0.4 * image_area and contour_area < min_valid_contour_area and len(cv.approxPolyDP(contour, 0.04 * peri, True)) == 4:
                min_valid_contour_area = contour_area
                final_contour = contour
        c = final_contour
        maxContourArea = min_valid_contour_area
        transformedImg = img.copy()
        if(maxContourArea > 0.4 * img.shape[0] * img.shape[1]):
            # print("here")
            # limit contour to quadrilateral
            peri = cv.arcLength(c, True)
            corners = cv.approxPolyDP(c, 0.04 * peri, True)

            # draw quadrilateral on input image from detected corners
            result = img.copy()
            cv.polylines(result, [corners], True, (0, 0, 255), 2, cv.LINE_AA)

            #show_images([img, result])

            # print(corners)

            x_list = [corners[0][0][0], corners[1][0]
                      [0], corners[2][0][0], corners[3][0][0]]
            y_list = [corners[0][0][1], corners[1][0]
                      [1], corners[2][0][1], corners[3][0][1]]
            x_list = np.sort(x_list)
            y_list = np.sort(y_list)

            # print(corners)

            temp_corners = np.squeeze(corners)

            #print("temp_corners", temp_corners)

            temp_corners = sorted(temp_corners, key=lambda x: x[0])

            top_left = []
            top_right = []
            bottom_left = []
            bottom_right = []
            if temp_corners[0][1] < temp_corners[1][1]:
                top_left = temp_corners[0]
                top_right = temp_corners[1]
            else:
                top_left = temp_corners[1]
                top_right = temp_corners[0]

            if temp_corners[2][1] < temp_corners[3][1]:
                bottom_left = temp_corners[2]
                bottom_right = temp_corners[3]
            else:
                bottom_left = temp_corners[3]
                bottom_right = temp_corners[2]

            height = np.max([top_left[1], top_right[1], bottom_left[1], bottom_right[1]]) - \
                np.min([top_left[1], top_right[1],
                       bottom_left[1], bottom_right[1]])
            width = np.max([top_left[0], top_right[0], bottom_left[0], bottom_right[0]]) - \
                np.min([top_left[0], top_right[0],
                       bottom_left[0], bottom_right[0]])
            #print(width, height)
            oldPoints = np.float32(
                [top_left, bottom_left, top_right, bottom_right])
            newPoints = np.float32(
                [[0, 0], [width, 0], [0, height], [width, height]])
            transformationMatrix = cv.getPerspectiveTransform(
                oldPoints, newPoints)
            transformedImg = cv.warpPerspective(
                img, transformationMatrix, (width, height))
        if debug:
            show_images(images=[transformedImg])

        white_img_contours = np.ones(img_cpy.shape)

        for contour in sorted_contours:
            x, y, w, h = cv.boundingRect(contour)
            if w/h >= 0.7 and w/h <= 1.3 and cv.contourArea(contour) < 0.5 * img.shape[0]*img.shape[1]:
                cv.fillPoly(white_img_contours, pts=[contour], color=(0, 0, 0))
        return transformedImg

    def get_contours_dimensions(self, erodedImg, img_cpy):
        contours, hierarchy = cv.findContours(
            (255 - erodedImg*255).astype("uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        white_img_large_contours = np.ones(img_cpy.shape)
        # computes the bounding box for the contour, and draws it on the frame,
        dimensions_contours = []

        c = max(contours, key=cv.contourArea)
        maxContourArea = cv.contourArea(c)

        for contour in contours:
            if maxContourArea * 0.2 > cv.contourArea(contour):
                continue
            (x, y, w, h) = cv.boundingRect(contour)
            dimensions_contours.append((x, y, w, h))
            cv.rectangle(white_img_large_contours,
                         (x, y), (x+w, y+h), (0, 0, 0), 2)
        dimensions_contours = sorted(
            dimensions_contours, key=lambda dimension: dimension[0])

        # print(dimensions_contours)
        # show_images([white_img_large_contours])
        return dimensions_contours

    def crop_groups(self, dimensions_contours, img_cpy):
        cropped_images = []
        for dimension in dimensions_contours:
            (x, y, w, h) = dimension
            cropped_images.append(img_cpy[y:y+h, x:x+w])
        # show_images(cropped_images)
        return cropped_images

    def find_contours_to_rect(self, img):
        contours, hierarchy = cv.findContours(
            (255-img).astype("uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        if cv.contourArea(max(contours, key=cv.contourArea)) > 0.5 * img.shape[0] * img.shape[1]:
            contours, hierarchy = cv.findContours(
                (255-img).astype("uint8"), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        white_img_large_contours = np.ones(img.shape)
        # computes the bounding box for the contour, and draws it on the frame,
        if debug:
            print(img.shape)
        sorted_contours = sorted(
            contours, key=lambda ctr: cv.boundingRect(ctr)[1])
        dimensions_contours = []
        for contour in sorted_contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if w/h >= 0.8 and w/h <= 1.3 and w*h > img.shape[0]*img.shape[1]/220:
                approx = cv.approxPolyDP(
                    contour, .03 * cv.arcLength(contour, True), True)
                if len(approx) >= 5:
                    dimensions_contours.append((x, y, w, h))
                    cv.rectangle(white_img_large_contours,
                                 (x, y), (x+w, y+h), (0, 0, 0), 2)
        return white_img_large_contours, dimensions_contours

    def crop_answers(self, cropped_images):
        contour_cropped_imgs = []
        dimensions_cropped_imgs = []

        for image in cropped_images:
            result_img, result_dimension = self.find_contours_to_rect(image)
            contour_cropped_imgs.append([result_img])
            dimensions_cropped_imgs.append(result_dimension)
            if debug:
                show_images([result_img, image])

        contours_count = []
        non_overlapped_cnts = []
        for dimensions_cropped_img in dimensions_cropped_imgs[0]:
            isOverlapped = False
            for contour in non_overlapped_cnts:
                (x, y, w, h) = dimensions_cropped_img
                (x1, y1, w1, h1) = contour
                if (x >= x1 and x <= x1+w1) or (x+w >= x1 and x+w <= x1+w1):
                    isOverlapped = True
                    break
            if isOverlapped:
                contours_count.append(len(non_overlapped_cnts))
                non_overlapped_cnts = []
                non_overlapped_cnts.append(dimensions_cropped_img)
            else:
                non_overlapped_cnts.append(dimensions_cropped_img)

        return contour_cropped_imgs, dimensions_cropped_imgs, contours_count

    def get_number_of_answers_per_question(self, contours_count):
        contours_count = np.array(contours_count)
        frequency = [0]*np.max(contours_count+1)
        for count in contours_count:
            frequency[count] = frequency[count] + 1
        answer_count = frequency.index(max(frequency))
        return answer_count

    def groups_questions(self, dimensions_cropped_imgs, cropped_images, answer_count):
        groups_questions_answers = []
        for i in range(len(dimensions_cropped_imgs)):
            dimensions_cropped_img = dimensions_cropped_imgs[i]
            question_count = len(dimensions_cropped_img)//answer_count
            questions_answers = []
            #print(answer_count, question_count)
            groups_questions_answers.append([])
            for question in range(question_count):
                questions_answers = []
                cropped_answers = []
                for j in range(answer_count):
                    (x, y, w,
                     h) = dimensions_cropped_img[question*answer_count+j]
                    cropped_answers.append(
                        (x, cropped_images[i][y:y+h, x:x+w]))
                sorted_cropped_answers = sorted(
                    cropped_answers, key=lambda ans: ans[0])

                for cropped_answer in sorted_cropped_answers:
                    # show_images([cropped_answer[1]])
                    questions_answers.append(cropped_answer[1])
                groups_questions_answers[i].append(questions_answers)
        return groups_questions_answers

    def get_student_answers(self, groups_questions_answers, answer_count):
        question_index = 0
        questions_final_answers = []
        for group in groups_questions_answers:
            for question in group:
                question_index = question_index+1
                ans = []
                for i in range(answer_count):
                    choice = question[i]
                    if np.sum(choice) < 0.6*(255*choice.shape[0]*choice.shape[1]):
                        ans.append(chr(ord('A')+i))
                if debug:
                    print("answer(s) for question ", question_index, "is", ans)
                questions_final_answers.append(ans)
        return questions_final_answers

    def write_excel(self, student_id, student_name, questions_final_answers):
        if debug:
            print("name = ", student_name)
        actual_answers = []
        with open(self.model_answer) as file:
            lines = file.readlines()
            for line in lines:
                actual_answers.append(line.split())

        # Convert answers to integers
        data = {"code": [student_id], "name": [student_name]}
        for i in range(len(questions_final_answers)):
            questions_final_answers[i].sort()
            actual_answers[i].sort()
            data["Q"+str(i+1)] = [1 if questions_final_answers[i]
                                  == actual_answers[i] else 0]

        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.output_path, mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, startrow=writer.sheets['bubble sheet'].max_row,
                        sheet_name="bubble sheet", index=False, header=False)

    def ocr(self, img, langSelected="eng"):
        # if it doesn't work :
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        result = []
        res = ''
        try:
            res = pytesseract.image_to_string(img, lang=langSelected)

            # print(arabic)
            if(langSelected == 'ara'):
                arabicText = get_display(res)
                res = arabic_reshaper.reshape(arabicText)
            res = res.strip()
            res = res.replace(" ", "")
        except Exception:
            print("Error!")
        return res


if __name__ == "__main__":
    mypath = "./BubbleSheet/dataset/Bubble_Data/Input"
    onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range(len(onlyFiles)):
        file = onlyFiles[i]
        print("Processed "+file+"...")
        bubble = Bubble(mypath+"/"+file,
                        "./BubbleSheet/answers.xlsx", "./BubbleSheet/five.txt")
        bubble.run()
        shutil.rmtree("./BubbleSheet/dataset/Input/")
        os.makedirs("./BubbleSheet/dataset/Input/")
        print(file+" Processed successfully")
