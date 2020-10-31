import cv2
import imutils
import time
import numpy as np 
from imutils.video import VideoStream
from collections import deque
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", help="path to the video file")
parser.add_argument("-b", "--buffer", type=int, default=64, help="buffer size")

args = parser.parse_args()

if args.video is None:
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture()

time.sleep(2.0)

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# list of tracked points
# deque allows us to draw the “contrail” of the ball, detailing its past locations
pts = deque(maxlen=args.buffer)
counter = 0
(dX, dY) = (0, 0)
direction = ""

while True:
    frame = vs.read()
    frame = frame if args.video is None else frame[1]

    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
    
    pts.appendleft(center)

    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

        if counter >= 10 and i == 1 and pts[-10] is not None:
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            dirX, dirY = "", ""

            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"
            if dirX != "" and dirY != "":
                direction = f"{dirX}-{dirY}"

            else:
                direction = dirX if dirX != "" else dirY
        
        thickness = int(np.sqrt(args.buffer / float(i+1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)

    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Frame", frame)
    counter += 1

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.stop() if args.video is None else vs.release()
cv2.destroyAllWindows()

