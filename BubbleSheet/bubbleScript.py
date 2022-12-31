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

from os import listdir
from os.path import isfile, join

debug = True


def get_circles_id_name_contours(img_cpy, cannyEdges, img):
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
        if w/h >= 0.8 and w/h <=1.3 and (cannyEdges.shape[0] * cannyEdges.shape[1] * 0.01) > w*h:
            #print("here")
            cv.rectangle(white_img_contours, (x, y),
                         (round(x+1.1*w), round(y+1.7*h)), (0, 0, 0), -1)
    #         cv.fillPoly(white_img_contours, pts =[contour], color=(0,0,0))
        elif w/h > 4 and (cannyEdges.shape[0] * cannyEdges.shape[1] * 0.2) > w*h:
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


def get_student_id_name(white_img_contours_IDBox, img_cpy):
    boxes_dimensions = Extract_Boxes(white_img_contours_IDBox, img_cpy)

    boxes_croped_images = []
    # print(boxes_dimenstions)
    boxes_dimensions = reversed(
        sorted(boxes_dimensions, key=lambda dimension: boxes_dimensions[0]))
    for dimension in boxes_dimensions:
        # print(dimension)
        (x, y, w, h) = dimension
        boxes_croped_images.append(img_cpy[y:y+h, x:x+w])

    # show_images(boxes_croped_images)
    ###########################################
    blurredImg = cv.medianBlur(boxes_croped_images[1], 3)
    kernel = np.ones((3, 3))
    dilatedImg = erode(blurredImg, kernel)
    if debug:
        show_images([boxes_croped_images[1], blurredImg, dilatedImg])
    ###########################################
    segmented_dimensions, filtered_img = segement_ID(255 - 255*blurredImg)

    ###########################################
    cropped_digits = []
    i = 0
    for dimension in segmented_dimensions:
        (x, y, w, h) = dimension
        cropped_digits.append(filtered_img[y-1:y+h+1, x-1:x+w+1])
        #cv.imwrite(str(i)+".jpg", filtered_img[y-1:y+h+1, x-1:x+w+1])
        i += 1
    if debug:
        show_images(cropped_digits)

    ###########################################
    model = load_pickle()
    for i in range(len(cropped_digits)):
        cropped_digits[i] = cv.resize(cropped_digits[i], (200, 100))
        cropped_digits[i] = cv.resize(cropped_digits[i], None, fx=3, fy=3,
                                      interpolation=cv.INTER_CUBIC)
    student_id = ""
    if len(cropped_digits) != 0:
        image_fv = knn.images_to_feature_vectors(cropped_digits)
        labels = knn.classify(model, image_fv, 3)
        student_id = knn.mapChars(listOfChars=labels)
    return student_id, boxes_croped_images[0]


def apply_perspective_transform(cannyEdges, img, img_cpy):
    contours, hierarchy = cv.findContours(
        cannyEdges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=cv.contourArea)

    c = max(sorted_contours, key=cv.contourArea)
    maxCountourArea = cv.contourArea(c)

    image_area = img.shape[0] * img.shape[1]
    min_valid_contour_area = maxCountourArea
    final_contour = c
    for contour in sorted_contours:
        contour_area = cv.contourArea(contour)
        peri = cv.arcLength(contour, True)
        if contour_area > 0.4 * image_area and contour_area < min_valid_contour_area and len(cv.approxPolyDP(contour, 0.04 * peri, True)) == 4:
            min_valid_contour_area = contour_area
            final_contour = contour
    c = final_contour
    maxCountourArea = min_valid_contour_area
    transormedImg = img.copy()
    if(maxCountourArea > 0.4 * img.shape[0] * img.shape[1]):
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
            np.min([top_left[1], top_right[1], bottom_left[1], bottom_right[1]])
        width = np.max([top_left[0], top_right[0], bottom_left[0], bottom_right[0]]) - \
            np.min([top_left[0], top_right[0], bottom_left[0], bottom_right[0]])
        #print(width, height)
        oldPoints = np.float32(
            [top_left, bottom_left, top_right, bottom_right])
        newPoints = np.float32(
            [[0, 0], [width, 0], [0, height], [width, height]])
        transformationMatrix = cv.getPerspectiveTransform(oldPoints, newPoints)
        transormedImg = cv.warpPerspective(
            img, transformationMatrix, (width, height))
    if debug:
        show_images(images=[transormedImg])

    white_img_contours = np.ones(img_cpy.shape)

    for contour in sorted_contours:
        x, y, w, h = cv.boundingRect(contour)
        if w/h >= 0.7 and w/h <= 1.3 and cv.contourArea(contour) < 0.5 * img.shape[0]*img.shape[1]:
            cv.fillPoly(white_img_contours, pts=[contour], color=(0, 0, 0))
    return transormedImg


def get_contours_dimensions(erodedImg, img_cpy):
    contours, hierarchy = cv.findContours(
        (255 - erodedImg*255).astype("uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    white_img_large_contours = np.ones(img_cpy.shape)
    # computes the bounding box for the contour, and draws it on the frame,
    dimensions_contours = []

    c = max(contours, key=cv.contourArea)
    maxCountourArea = cv.contourArea(c)

    for contour in contours:
        if maxCountourArea * 0.2 > cv.contourArea(contour):
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


def crop_groups(dimensions_contours, img_cpy):
    croped_images = []
    for dimension in dimensions_contours:
        (x, y, w, h) = dimension
        croped_images.append(img_cpy[y:y+h, x:x+w])
    # show_images(croped_images)
    return croped_images


def find_contours_to_rect(img):
    contours, hierarchy = cv.findContours(
        (255-img).astype("uint8"), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cv.contourArea(max(contours, key=cv.contourArea)) > 0.5 * img.shape[0] * img.shape[1]:
        contours, hierarchy = cv.findContours(
            (255-img).astype("uint8"), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    white_img_large_contours = np.ones(img.shape)
    # computes the bounding box for the contour, and draws it on the frame,
    print(img.shape)
    sorted_contours = sorted(contours, key=lambda ctr: cv.boundingRect(ctr)[1])
    dimensions_contours = []
    for contour in sorted_contours:
        (x, y, w, h) = cv.boundingRect(contour)
        if w/h >= 0.8 and w/h <= 1.3 and w*h > img.shape[0]*img.shape[1]/220:
            approx = cv.approxPolyDP(
                contour, .03 * cv.arcLength(contour, True), True)
            # print(len(approx))
            if len(approx) >= 6:
                dimensions_contours.append((x, y, w, h))
                cv.rectangle(white_img_large_contours,
                             (x, y), (x+w, y+h), (0, 0, 0), 2)
    print("Here === >", len(dimensions_contours))
    return white_img_large_contours, dimensions_contours


def crop_answers(croped_images):
    contour_cropped_imgs = []
    dimensions_cropped_imgs = []

    for image in croped_images:
        result_img, result_dimenstion = find_contours_to_rect(image)
        contour_cropped_imgs.append([result_img])
        dimensions_cropped_imgs.append(result_dimenstion)
        if debug:
            show_images([result_img])

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
        # print(non_overlapped_cnts)

    # print(contours_count)
    return contour_cropped_imgs, dimensions_cropped_imgs, contours_count


def get_number_of_answers_per_question(contours_count):
    contours_count = np.array(contours_count)
    frequency = [0]*np.max(contours_count+1)
    for count in contours_count:
        frequency[count] = frequency[count] + 1
    answer_count = frequency.index(max(frequency))
    return answer_count


def groups_questions(dimensions_cropped_imgs, croped_images, answer_count):
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
                (x, y, w, h) = dimensions_cropped_img[question*answer_count+j]
                cropped_answers.append((x, croped_images[i][y:y+h, x:x+w]))
            sorted_cropped_answers = sorted(
                cropped_answers, key=lambda ans: ans[0])

            for cropped_answer in sorted_cropped_answers:
                # show_images([cropped_answer[1]])
                questions_answers.append(cropped_answer[1])
            groups_questions_answers[i].append(questions_answers)
    return groups_questions_answers


def get_student_answers(groups_questions_answers, answer_count):
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
            #print("answer(s) for question ", question_index, "is", ans)
            questions_final_answers.append(ans)
    return questions_final_answers


def write_excel(student_id, student_name, questions_final_answers):
    actual_answers = []
    with open("answers.txt") as file:
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
    with pd.ExcelWriter("answers.xlsx", mode="a", if_sheet_exists="overlay") as writer:
        df.to_excel(writer, startrow=writer.sheets['bubble sheet'].max_row,
                    sheet_name="bubble sheet", index=False, header=False)


# Extract Boxes of Name and ID

def ocr(img, langSelected="eng"):
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


def Extract_Boxes(img, img_cpy):
    kernel = np.ones((15, 15))
    #dilatedImg = dilate(img, kernel)
    kernel = np.ones((15, 15))
    erodedImg = erode(img, kernel)

    contours, hierarchy = cv.findContours((255 - erodedImg*255).astype("uint8"),
                                          cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    white_img_large_contours = np.ones(img_cpy.shape)
    # computes the bounding box for the contour, and draws it on the frame,
    dimensions_contours = []
    sorted_contours = sorted(contours, key=cv.contourArea)
    for i in range(2):
        contour = sorted_contours[len(sorted_contours) - i - 1]
        (x, y, w, h) = cv.boundingRect(contour)
        dimensions_contours.append((x, y, w, h))
        cv.rectangle(white_img_large_contours,
                     (x, y), (x+w, y+h), (0, 0, 0), 2)
#     print(dimensions_contours)
    #show_images([erodedImg, white_img_large_contours])
    return dimensions_contours


def segement_ID(img):
    #     cnts = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #     cnts = cnts[0]
    # #     cnts = cnts[0] if imutils.is_cv() else cnts[1]
    #     cv.drawContours(img, cnts, -1, 0, 5) # 15 is the right thickness for this image, but might not be for other ones...
    # show_images([img])
    img = cv.normalize(img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    res, img = cv.threshold(img, 64, 255, cv.THRESH_BINARY)
    # Fill everything that is the same colour (black) as top-left corner with white
    # show_images([img])
    cv.floodFill(img, None, (0, 0), 255)
    # show_images([img])
    # Fill everything that is the same colour (white) as top-left corner with black
    cv.floodFill(img, None, (0, 0), 0)
    # show_images([img])
    contours, hierarchy = cv.findContours((img).astype("uint8"),
                                          cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda ctr: cv.boundingRect(ctr)[0])
    white_img_large_contours = np.ones(img.shape)
    dimensions_contours = []
    for contour in contours:
        #         print(contour)
        (x, y, w, h) = cv.boundingRect(contour)
        if(w*h > 20):
            dimensions_contours.append((x, y, w, h))
            cv.rectangle(white_img_large_contours,
                         (x, y), (x+w, y+h), (0, 0, 0), 2)
    #dimensions_contours = sorted(dimensions_contours, key=lambda dimension: dimension[0])

    # print(dimensions_contours)
    #show_images([img, white_img_large_contours])
    return dimensions_contours, img


def load_pickle() -> dict:
    a_file = open("./data.pkl", "rb")
    model = pickle.load(a_file)
    return model


def bubble_sheet(image_path):
    # read image
    img = cv.imread(image_path, 0)
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
    transormedImg = apply_perspective_transform(cannyEdges, img, img_cpy)
    ############################################
    # use canny to detect edges
    cannyEdges = cannyEdge(transormedImg)
    # show_images([cannyEdges])
    ############################################
    img_cpy = transormedImg.copy()
    img_cpy = cv.adaptiveThreshold(
        img_cpy, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 59, 3)
    # Get circles ,student id and name contours
    white_img_contours, white_img_contours_IDBox = get_circles_id_name_contours(
        img_cpy, cannyEdges, img)
    ###########################################
    student_id, student_name = get_student_id_name(
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
    dimensions_contours = get_contours_dimensions(erodedImg, img_cpy)
    ###########################################
    # Crop questions groups
    croped_images = crop_groups(dimensions_contours, img_cpy)
    ###########################################
    # Crop answers from each group of questions
    contour_cropped_imgs, dimensions_cropped_imgs, contours_count = crop_answers(
        croped_images)
    ###########################################
    # Get number of answers per question
    answer_count = get_number_of_answers_per_question(contours_count)
    ###########################################
    # Groups questions in groups with there answers
    groups_questions_answers = groups_questions(
        dimensions_cropped_imgs, croped_images, answer_count)
    ###########################################
    # count = 0
    # print("groups_questions_answers", len(groups_questions_answers))
    # for group in groups_questions_answers:
    #     print("group", len(group))
    #     for question in group:
    #         show_images(question)
    ###########################################
    # Group questions in groups and find answers
    questions_final_answers = get_student_answers(
        groups_questions_answers, answer_count)
    ###########################################
    # Write results to excel sheet
    write_excel(student_id, ocr(student_name), questions_final_answers)
    ###########################################
    ###########################################


def run_bubble_sheet():
    mypath = "dataset/Bubble_Data/mo3ed2"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range(len(onlyfiles)):
        # break
        file = onlyfiles[i]
        print("Processed "+file+"...")
        result_image = bubble_sheet(mypath+"/"+file)
        print(file+" Processed successfully")
    # result_image = bubble_sheet(mypath+"/"+"Five0.png")

# extract_grid("datasets/dataset4_module1/5.jpg")


run_bubble_sheet()
