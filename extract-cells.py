# import libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['image.cmap'] = 'gray'

# read image
img = cv.imread('./Assets/Input.jpg', 0)

# thresholding 
(thresh, binaryImg) = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
binaryImg = 255 - binaryImg 
cv.imwrite("Outputs/Binary_img.jpg", binaryImg)
plt.axis('off')
plt.imshow(binaryImg)



def getLines(x):
    global horizontalLinesImg, verticalLinesImg, kernel
    
    # Kernel Length
    kernelLength = np.array(img).shape[1] // x

    # Vertical Kernel (1 x kernelLength)
    verticalKernel = cv.getStructuringElement(cv.MORPH_RECT, (1, kernelLength))
    
    # Horizontal Kernel (kernelLength x 1)
    horizontalKernel = cv.getStructuringElement(cv.MORPH_RECT, (kernelLength, 1))
    
    # Apply erosion then dilation to detect vertical lines using the vertical kernel
    erodedImg = cv.erode(binaryImg, verticalKernel, iterations = 3)
    verticalLinesImg = cv.dilate(erodedImg, verticalKernel, iterations = 3)
    cv.imwrite("Outputs/vertical_lines.jpg", verticalLinesImg)
    
    # Apply erosion then dilation to detect horizontal lines using the horizontal kernel
    erodedImg = cv.erode(binaryImg, horizontalKernel, iterations = 3)
    horizontalLinesImg = cv.dilate(erodedImg, horizontalKernel, iterations = 3)
    cv.imwrite("Outputs/horizontal_lines.jpg", horizontalLinesImg)
    
    plt.subplot(1, 2, 1)
    plt.imshow(verticalLinesImg)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(horizontalLinesImg)
    plt.axis('off')

def getIntersections(pixels):
    intersections = []
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            if pixels[i][j] != 0:
               intersections.append((i, j))
    return intersections
    
getLines(x = 7)

# Get vertices by ANDing the vertical and horizontal lines
res = cv.bitwise_and(verticalLinesImg, horizontalLinesImg)
cv.imwrite("Outputs/intersections.jpg", res)
plt.imshow(res)
plt.axis('off')

# Print positions of each intersection
print(getIntersections(res))


