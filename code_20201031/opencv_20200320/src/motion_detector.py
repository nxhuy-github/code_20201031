from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video", help="path to the video file")
parser.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

args = parser.parse_args()

if args.video is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args.video)

# Assumption: The first frame of our video file will contain no motion 
# and just background — therefore, we can model the background of our video stream 
# using only the first frame of the video.
firstFrame = None

# Main process
while True:
    frame = vs.read()
    frame = frame if args.video is None else frame[1]
    text = "Unoccupied"

    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    # Color has no bearing on the motion detection algorithm.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between 
    # the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < args.min_area:
            continue

        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.putText(frame, f"Room Status; {text}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # Press Q to quit
    if key == ord("q"):
        break

vs.stop() if args.video is None else vs.release()
cv2.destroyAllWindows()

