from imutils import build_montages
from imutils import paths
import cv2
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--images', required=True, help='path to directory of images')
parser.add_argument('-s', '--sample', type=int, default=21, help='# of images to sample')
args = parser.parse_args()

imagePaths = list(paths.list_images(args.images))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args.sample]

images = []
for imagePath in imagePaths:
    img = cv2.imread(imagePath)
    images.append(img)

montages = build_montages(images, (128, 196), (7, 3))
for montage in montages:
    cv2.imshow("Montage", montage)
    cv2.waitKey(0)