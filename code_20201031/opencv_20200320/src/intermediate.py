import argparse
import imutils
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to input image")

args = parser.parse_args()

# Convert an image to grayscale
img = cv2.imread(args.image)
cv2.imshow("Image", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# Edge detection
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Thresholding
# the line code below:
#     - pixel < 225 -> set to 0
#     - pixel > 225 -> set to 255
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# Detecting contours
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = img.copy()
# Drawing contours
for c in cnts:
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
    cv2.imshow("Contours", output)
    cv2.waitKey(0)

text = f"I found {len(cnts)} objects"
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)
# cv2.imshow("Contours with Count", output)
cv2.imshow("Contours", output)
cv2.waitKey(0)

# Erosions and dilations
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

# Masking and bitwise operations
mask = thresh.copy()
output = cv2.bitwise_and(img, img, mask=mask)
cv2.imshow("Mask output", output)
cv2.waitKey(0)