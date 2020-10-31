import argparse
import cv2
import imutils
import numpy as np 

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to the image file")
parser.add_argument("-m", "--method", required=True, help="sorting method")

args = parser.parse_args()

image = cv2.imread(args.image)
method = args.method
accumEdged = np.zeros(image.shape[:2], dtype="uint8")

def sort_contours(cnts, method="left-to-right"):
    # ascending or descending
    reverse = False
    # (x, y)-coordinates : i = 0: sort by x
    #                      i = 1: sort by y
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # cv2.boundingBoxes returns: (x, y), w, h
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    cnts, boundingBoxes = zip(*sorted(zip(cnts, boundingBoxes), 
                                key=lambda b: b[1][i], reverse=reverse))

    return cnts, boundingBoxes

def draw_contour(image, c, i):
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (255, 255, 255), 2)
    return image

for chan in cv2.split(image):
    chan = cv2.medianBlur(chan, 11)
    edged = cv2.Canny(chan, 50, 200)
    accumEdged = cv2.bitwise_or(accumEdged, edged)

cv2.imshow("Edge map", accumEdged)
cv2.waitKey(0)


# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# edge = cv2.Canny(gray, 50, 200)
# cv2.imshow("Edge map 2", edge)
# cv2.waitKey(0)

cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]
origine = image.copy()

for i, c in enumerate(cnts):
    origine = draw_contour(origine, c, i)
cv2.imshow("Sorted by size", origine)
cv2.waitKey(0)

cnts, boundingBoxes = sort_contours(cnts, method=method)

for i, c in enumerate(cnts):
    draw_contour(image, c, i)

cv2.imshow("Sorted by location", image)
cv2.waitKey(0)