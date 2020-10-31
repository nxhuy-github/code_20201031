import cv2
import imutils
import numpy as np

image = cv2.imread('data/extreme_points_input.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
#cv2.imshow('Thresh', thresh)
#cv2.waitKey(0)
thresh = cv2.erode(thresh, None, iterations=2)
#cv2.imshow('Thresh eroded', thresh)
#cv2.waitKey(0)
thresh = cv2.dilate(thresh, None, iterations=2)
#cv2.imshow('Thresh eroded + dilated', thresh)
#cv2.waitKey(0)

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Get contour with max area
c = max(cnts, key=cv2.contourArea)
print(f"Contour shape {c.shape}")

# Calculate extreme points
# cv2.findContours  is simply a NumPy array of (x, y)-coordinates. 
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# Drawing
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
cv2.imshow("Image", image)
cv2.waitKey(0)
