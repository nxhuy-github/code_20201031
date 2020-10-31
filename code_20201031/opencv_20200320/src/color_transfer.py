import numpy as np 
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True, help='path to image source file')
parser.add_argument('-t', '--target', required=True, help='path to image target file')

args = parser.parse_args()

def image_stats(image):
    l, a, b = cv2.split(image)
    return l.mean(), l.std(), a.mean(), a.std(), b.mean(), b.std()

def color_transfer(source, target):
    # Convert BGR to LAB
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # Get Mean, Standard Deviation of Source and Target
    lSrcMean, lSrcStd, aSrcMean, aSrcStd, bSrcMean, bSrcStd = image_stats(source)
    lTarMean, lTarStd, aTarMean, aTarStd, bTarMean, bTarStd = image_stats(target)

    # Subtract mean from target
    l, a, b = cv2.split(target)
    l -= lTarMean
    a -= aTarMean
    b -= bTarMean

    # Scale by Standard Diviation
    l = (lTarStd / lSrcStd) * l
    a = (aTarStd / aSrcStd) * a
    b = (bTarStd / bSrcStd) * b

    # Add the source mean
    l += lSrcMean
    a += aSrcMean
    b += bSrcMean

    # Clip the pixels that fall outside the range [0, 255]
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # Merge to create image and convert back to BGR
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
    return transfer

source = cv2.imread(args.source)
target = cv2.imread(args.target)
if source is not None and target is not None:
    transfer = color_transfer(source, target)
    cv2.imshow("Source", source)
    cv2.imshow("Target", target)
    cv2.imshow("Transfer", transfer)
    cv2.waitKey(0)