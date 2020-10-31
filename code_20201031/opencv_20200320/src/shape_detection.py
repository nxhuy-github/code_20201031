import cv2
import argparse
import imutils
import numpy as np 

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to the image file")

args = parser.parse_args()

image = cv2.imread(args.image)
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
mask  = cv2.inRange(image, lower, upper)

cv2.imshow("Mask", mask)
cv2.waitKey(0)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(f"I found {len(cnts)} black shapes")

for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# ------------- ALTERNATIVE WAY ??? ----------------------
image = cv2.imread(args.image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.imshow("Thresh", thresh)
# cv2.waitKey(0)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(f"Alternative Way: I found {len(cnts)} black shapes")
for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Alternative Way", image)
    cv2.waitKey(0)