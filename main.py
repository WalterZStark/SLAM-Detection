# Main file for running all libraries
# Written by Walter Stark


# Import Statements
import cv2
import time
import os
import sys
from pathlib import Path

# Inser path for SLAM scripts
sys.path.insert(0, os.getcwd() + '\SLAM')
print(os.getcwd() + '\SLAM')



from retrieve_YOLO import outputSegment # using custom YOLO.py
from retrieve_images import retrieve
from data_downloader import downloadTest
from threading import Thread
from djitellopy import Tello

# Downlaod SLAM Test Files
url = "https://vision.in.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_long_office_household.tgz"
fileName = 'fr3_office.tgz'

downloadTest(url,fileName)
print("Passed Download Test")



# Init tello
tello = Tello()




keepRecording = True


useDrone = False


# Check if planning on using drone or laptop
if useDrone:
    # Connect to Tello
    tello.connect()
    # Start Stream
    tello.streamon()

    print(tello.get_battery())
    # Turn on down vision
    # By default send command to turn on front Camera
    tello.send_command_with_return("downvision 0")



frontvision = True

vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Create a function to output images
def imgOut():
 
    
    # Check to see if recording has finished
    while keepRecording:
        img = retrieve(useDrone, frontvision,tello,vid)
        imgOut = outputSegment(img)
        cv2.imshow('img', imgOut)
        cv2.waitKey(1)

    

# Create a thread to run image viewing in the background
recorder = Thread(target=imgOut, daemon=True) # daemon to ensure threads are killed
recorder.start()

#tello.takeoff()
#time.sleep(5)

try:
    while True:
        #Image processing can happen here haha
        print("")
        True
except KeyboardInterrupt:
    print("End Program")
    pass


#recorder.join()

