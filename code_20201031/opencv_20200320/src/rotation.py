import cv2
import numpy as np 
import argparse
import imutils

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="path to the image file")

args = parser.parse_args()

img = cv2.imread(args.image)

h, w, d = img.shape
center = w // 2, h // 2
for angle in range(0, 360, 15):
    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
    # The image is “cut off” when it’s rotated
    cv2.imshow('Rotated (Problem)', rotated)
    cv2.waitKey(0)

for angle in range(0, 360, 15):
    rotated = imutils.rotate_bound(img, angle)
    cv2.imshow('Rotated (Correct)', rotated)
    cv2.waitKey(0)
