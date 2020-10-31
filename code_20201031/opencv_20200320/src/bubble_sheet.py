import cv2
import imutils
import argparse
import numpy as np 
from imutils.perspective import four_point_transform
from imutils import contours

# define the answer key which maps the question number
# to the correct answer
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to image file")

args = parser.parse_args()

image = cv2.imread(args.image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

cv2.imshow("Edged", edged)
cv2.waitKey(0)

cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

if len(cnts) > 0:
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

        if len(approx) == 4:
            docCnt = approx
            break

# apply a four point perspective transform to both the
# original image and grayscale image to obtain a top-down
# birds eye view of the paper
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

cv2.imshow("Paper", paper)
cv2.imshow("Warped", warped)
cv2.waitKey(0)

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(f"I found {len(cnts)} contours")
# List of contours that correspond to the questions/bubbles on the exam
questionCnts = []

# Find all regions as bubbles
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    ar = w / float(h)
    # in order to label the contour as a question, region
	# should be sufficiently wide, sufficiently tall, and
	# have an aspect ratio approximately equal to 1
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        questionCnts.append(c)

print(f"I found {len(questionCnts)} bubbles in total")
# This line below ensure that 
# rows of questions that are closer to the top of the exam 
# will appear first in the sorted list.
questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
correct = 0

# loop through each question in which has 5 answers
for q, i in enumerate(np.arange(0, len(questionCnts), 5)):
    # This line below ensure that 
    # the contour of A will appear before the contour of B and so on.
    cnts = contours.sort_contours(questionCnts[i: i+5])[0] # default "left-to-right"
    bubbled = None

    # Determine which bubble is filled in
    # using our thresh  image and 
    # counting the number of non-zero pixels (i.e., foreground pixels) 
    # in each bubble region. 
    # The most non-zero pixels region is the bubbled region !!!
    for (j, c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)

        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)
        total = cv2.countNonZero(mask)
        
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)

    color = (0, 0, 255)
    k = ANSWER_KEY[q]

    if k == bubbled[1]:
        color = (0, 255, 0)
        correct += 1

    cv2.drawContours(paper, [cnts[k]], -1, color, 3)

score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)