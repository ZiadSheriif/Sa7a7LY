# import from skimage
from skimage.color import rgb2gray
from skimage.filters import sobel, sobel_h, sobel_v, prewitt, roberts, gaussian
from skimage.feature import canny
import skimage.io as io
import cv2 as cv

from scipy.spatial import distance as dist

# import from matplotlib
import matplotlib.pyplot as plt

# import from numpy
import numpy as np

# import utils
from utils.commonfunctions import *

from os import listdir
from os.path import isfile,join

def closing(img):
    dilate_kernel = np.ones((5,5))
    erosion_kernel = np.ones((3,3))
    dilated_img = dilate(img,dilate_kernel)
    closed_img = erode(dilated_img,erosion_kernel)
    return closed_img

def get_table_contour(closed_img,img):
    contours, hierarchy = cv.findContours(closed_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # get the biggest contour
    c = max(contours, key = cv.contourArea)

    # contour of table
    contours_list = list(contours)
    
    image_area = img.shape[0] * img.shape[1]
    
    # Area of final contour
    min_valid_contour_area = cv.contourArea(c)
    # final contour
    final_contour = c
    
    for contour in contours:
        contour_area = cv.contourArea(contour)
        if contour_area > 0.25 * image_area and contour_area < min_valid_contour_area:
            min_valid_contour_area = contour_area
            final_contour = contour
    c = final_contour
    return final_contour

def hough_line(biggest_contour,img):
    dilate_kernel = np.ones((25,25))
    dilated_biggest_contour = dilate(biggest_contour,dilate_kernel)

    lines =cv.HoughLinesP(dilated_biggest_contour.astype(np.uint8),0.5,np.pi/180,100,minLineLength=0.25*min(img.shape[0],img.shape[1]),maxLineGap=10)

    hough_lines_out = np.zeros(dilated_biggest_contour.shape)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv.line(hough_lines_out,(x1,y1),(x2,y2),(255,255,255),2)
    dilate_kernel = np.ones((15,15))
    hough_lines_out = dilate(hough_lines_out,dilate_kernel)
    return hough_lines_out

def get_biggest_contour(hough_lines_out):
    contours, hierarchy = cv.findContours(hough_lines_out.astype(np.uint8), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv.contourArea)
    return c
    
def limit_contour_to_quadrilateral(contour,img):
    # limit contour to quadrilateral
    peri = cv.arcLength(contour, True)
    corners = cv.approxPolyDP(contour, 0.04 * peri, True)

    # draw quadrilateral on input image from detected corners
    result = img.copy()
    cv.polylines(result, [corners], True, (0,0,255), 2, cv.LINE_AA)
    
    return result,corners

def get_four_corners(corners):
    x_list = [corners[0][0][0],corners[1][0][0],corners[2][0][0],corners[3][0][0]]
    y_list = [corners[0][0][1],corners[1][0][1],corners[2][0][1],corners[3][0][1]]
    x_list = np.sort(x_list)
    y_list = np.sort(y_list)

    # print(corners)
    temp_corners = np.squeeze(corners)

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
    return top_left,top_right,bottom_left,bottom_right

def prespective_transform(top_left,top_right,bottom_left,bottom_right,img):
    height = np.max([top_left[1],top_right[1],bottom_left[1],bottom_right[1]]) - np.min([top_left[1],top_right[1],bottom_left[1],bottom_right[1]]) 
    width = np.max([top_left[0],top_right[0],bottom_left[0],bottom_right[0]]) - np.min([top_left[0],top_right[0],bottom_left[0],bottom_right[0]])

    oldPoints = np.float32([top_left,bottom_left,top_right,bottom_right])
    newPoints = np.float32([[0,0],[width,0],[0,height],[width,height]])
    transformationMatrix = cv.getPerspectiveTransform(oldPoints,newPoints)
    transormedImg = cv.warpPerspective(img,transformationMatrix,(width,height))
    return transormedImg
    
def extract_grid(file):
    #Read image
    img = cv.imread(file,0)
    grey_scale = img
    
    #Edge detection
    cannyEdges = cannyEdge(grey_scale)
    
    # Apply closing
    closed_img = closing(cannyEdges)
    
    # get contour of table
    table_contour = get_table_contour(closed_img,img)
    
    # draw contour
    black_img = np.zeros(img.shape)
    biggest_contour = cv.drawContours(black_img,[table_contour],0,(255,255,255),2)
    
    # apply hough transform
    hough_lines_out = hough_line(biggest_contour,img)
    
    # get biggest contour
    final_contour = get_biggest_contour(hough_lines_out)
    
    # limit contour to quadrilateral
    image_with_contour, corners = limit_contour_to_quadrilateral(final_contour,img)
    
    # get four corners
    top_left,top_right,bottom_left,bottom_right = get_four_corners(corners)
    
    # prespective transform
    transformed_image = prespective_transform(top_left,top_right,bottom_left,bottom_right,img)
    
#     print(transformed_image)
#     show_images(images = [transformed_image])
    
    return transformed_image

    

def run_extract_grid():
    mypath = "datasets/dataset"
    write_path = "grid/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    for i in range(len(onlyfiles)):
        file = onlyfiles[i]
        print(mypath+"/"+file)
        result_image = extract_grid(mypath+"/"+file)
        cv.imwrite(write_path+file,result_image)
    
# extract_grid("datasets/dataset4_module1/5.jpg")
    
run_extract_grid()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    