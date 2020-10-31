import cv2
import imutils
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required=True, help='path to image file')

args = parser.parse_args()

img = cv2.imread(args.image)

# define the list of boundaries
# tuple with two values: a list of lower limits and a list of upper limits
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]

for lower, upper in boundaries:
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # cv2.inRange: find the colors within the specified boundaries 
	# and apply the mask
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    
    #cv2.imshow("Mask", mask)
    cv2.imshow("images", np.hstack([img, output]))
    cv2.waitKey(0)

