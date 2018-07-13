# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import sys

#redirect stderr to nowhere to stay invisible ;)
f = open('nul', 'w')
sys.stderr = f

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="log.avi",
                help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=60,
                help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
                help="codec of output video")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera
# sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None

# loop over frames from the video stream
while True:
    # grab the frame from the video stream and resize it to have a
    # maximum width of 300 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=300)

    # check if the writer is None
    if writer is None:
        # store the image dimensions, initialzie the video writer,
        # and construct the zeros array
        (h, w) = frame.shape[:2]
        writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
                                 (w, h), True)
        zeros = np.zeros((h, w), dtype="uint8")

    # store frame
    output = np.zeros((h, w, 3), dtype="uint8")
    output[0:h, 0:w] = frame
    writer.write(output)
    key = cv2.waitKey(1) & 0xFF

cv2.destroyAllWindows()
vs.stop()
writer.release()