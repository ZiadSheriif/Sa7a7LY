# import libraries
import cv2 as cv
import numpy as np
import matplotlib as mpl
import os
from os import listdir
from os.path import isfile, join

from skimage.feature import hog
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle

mpl.rcParams['image.cmap'] = 'gray'

Symbol_2, Symbol_3 = "./Cells/2", "./Cells/3"
checkMarksPath, boxesPath, otherPath, questionMarksPath = "./data/marks", "./data/boxes", "./data/other", "./data/questionMarks"

def detectHorizontalLines(symbol):
    width = symbol.shape[1] // 5
    horizontalSE = cv.getStructuringElement(cv.MORPH_RECT, (width, 1))
    morphResult = cv.morphologyEx(symbol, cv.MORPH_OPEN, horizontalSE)
    contours, hierarchy = cv.findContours(morphResult, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    horizontalLinesCnt = len(contours)
    return horizontalLinesCnt

def detectVerticalLines(symbol):
    height = symbol.shape[0] // 5
    verticalSE = cv.getStructuringElement(cv.MORPH_RECT, (1, height))
    morphResult = cv.morphologyEx(symbol, cv.MORPH_OPEN, verticalSE)
    contours, hierarchy = cv.findContours(morphResult, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    verticalLinesCnt = len(contours)
    return verticalLinesCnt

def getLinesCount(img):
    _, thresh = cv.threshold(img, 225, 255, cv.THRESH_BINARY_INV)
    kernal = np.ones((2, 2), np.uint8)
    dilatedImg = cv.dilate(thresh, kernal, iterations=1)
    contours, hierarchy = cv.findContours(dilatedImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    count = len(contours)
    return count - 1

def detectEmptyCells(symbol):
    numOfWhitePixels = np.sum(symbol == 255)
    return (numOfWhitePixels == 0)

############################# HOG ############################

def prepareData(dataPath, files, label):
    x = []
    for fileName in files:
        img = cv.imread(dataPath + "/" + fileName, 0)
        x.append(img)
    y = [label] * len(x)
    return x, y

def train(x_train, y_train):
    list_hog_fd = []
    for img in x_train:
        fd = hog(resize(img, (128*4, 64*4)), orientations=9, pixels_per_cell=(14, 14),
                 cells_per_block=(1, 1), visualize=False)
        list_hog_fd.append(fd)

    x_train = np.array(list_hog_fd)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)

    # save the model to disk
    filename = 'model.sav'
    pickle.dump(knn, open(filename, 'wb'))

def knnScore(x_test, y_test):
    filename = 'model.sav'
    # load the model from disk
    knn = pickle.load(open(filename, 'rb'))
    list_hog_fd = []
    for img in x_test:
        fd = hog(resize(img, (128*4, 64*4)), orientations=9, pixels_per_cell=(14, 14),
                 cells_per_block=(1, 1), visualize=False)
        list_hog_fd.append(fd)

    x_test = np.array(list_hog_fd)

    score = knn.score(x_test, y_test)
    percentage = np.round(score * 100, 2)

    return percentage

def knnPredict(img):
    filename = 'model.sav'
    # load the model from disk
    knn = pickle.load(open(filename, 'rb'))
    fd = hog(resize(img, (128*4, 64*4)), orientations=9, pixels_per_cell=(14, 14),
             cells_per_block=(1, 1), visualize=False)
    expected = knn.predict(fd.reshape(1, -1))
    return expected[0]

def getData():
    checkMarksLabel, boxesLabel, questionMarksLabel, otherLabel = "C", "B", "Q", "O"

    checkMarksFiles = [f for f in listdir(checkMarksPath) if isfile(join(checkMarksPath, f))]
    boxesFiles = [f for f in listdir(boxesPath) if isfile(join(boxesPath, f))]
    questionMarksFiles = [f for f in listdir(questionMarksPath) if isfile(join(questionMarksPath, f))]
    otherFiles = [f for f in listdir(otherPath) if isfile(join(otherPath, f))]

    x_checkMarks, y_checkMarks = prepareData(checkMarksPath, checkMarksFiles, checkMarksLabel)
    x_boxes, y_boxes = prepareData(boxesPath, boxesFiles, boxesLabel)
    x_questionMarks, y_questionMarks = prepareData(questionMarksPath, questionMarksFiles, questionMarksLabel)
    x_other, y_other = prepareData(otherPath, otherFiles, otherLabel)

    x = x_checkMarks + x_boxes + x_questionMarks + x_other
    y = y_checkMarks + y_boxes + y_questionMarks + y_other

    return x, y

def runHog():
    x, y = getData()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.33, random_state=42)

    train(x_train, y_train)
    score = knnScore(x_test, y_test)

    print(score, '%')

def mapPrediction(symbol):
    if (symbol == "C"):
        return 5
    elif (symbol == "Q"):
        return "?"
    elif (symbol == "B"):
        return 0

def runDetectCells():
    files = []
    results = [[], []]

    files.append([f for f in listdir(Symbol_2) if isfile(join(Symbol_2, f))])
    files.append([f for f in listdir(Symbol_3) if isfile(join(Symbol_3, f))])
    for i in range(len(files)):
        for filename in files[i]:
            img = []
            if (i == 0):
                img = cv.imread(Symbol_2 + "/" + filename, 0)
            else:
                img = cv.imread(Symbol_3 + "/" + filename, 0)
            if (detectEmptyCells(img)):
                results[i].append(" ")
            else:
                prediction = knnPredict(img)
                if (prediction == "O"):
                    count = getLinesCount(img)
                    numOfHorizontalLines = detectHorizontalLines(img)
                    numOfVerticalLines = detectVerticalLines(img)
                    if (numOfVerticalLines > numOfHorizontalLines):
                        results[i].append(count)
                    else:
                        results[i].append(5 - count)
                else:
                    results[i].append(mapPrediction(prediction))
    return results