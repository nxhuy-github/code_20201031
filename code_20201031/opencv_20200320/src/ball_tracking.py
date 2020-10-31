import cv2
import argparse
import imutils
from collections import deque
from imutils.video import VideoStream
import numpy as np 
import time

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", help="path to the (optional) video file")
parser.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")

args = parser.parse_args()

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# list of tracked points
# deque allows us to draw the “contrail” of the ball, detailing its past locations
pts = deque(maxlen=args.buffer)

if not args.video:
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args.video)

time.sleep(2.0)

# Main process
while True:
    frame = vs.read()

    frame = frame if args.video is None else frame[1]
    
    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Try to detect the green ball in the image
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 2, (0, 0, 255), -1)

    # Once a bounded length deque is full, when new items are added, 
    # a corresponding number of items are discarded from the opposite end
    pts.appendleft(center)

    # Keep track the “contrail” of the ball
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        
        thickness = int(np.sqrt(args.buffer / float(i+1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Press Q to quit
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.stop() if args.video is None else vs.release()
cv2.destroyAllWindows()


