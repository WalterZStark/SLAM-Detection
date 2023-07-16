#Test_takeoff.py
# Written by Walter Stark
# NO LONGER USED - Most code moved to main.py


import cv2
import time
from retrieve_images import retrieve
from threading import Thread
from djitellopy import Tello

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
        # Try Catch added in case no frame when looking downward
       # try:
            img = retrieve(useDrone, frontvision,tello,vid)
            #print(img)
            cv2.imshow('img', img)
            cv2.waitKey(1)
            if(frontvision):
                
                '''
                singular_frame = tello.get_frame_read(False,1).frame
                cropped_img = singular_frame[0:240, 0:320]
                cv2.imshow('img', cropped_img)
                cv2.waitKey(1)
                '''
            else: 
                
                '''
                singular_frame = tello.get_frame_read().frame
                img = cv2.resize(singular_frame, (360, 240))
                im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                surf = cv2.xfeatures2d.SURF_create(50000)
               # kp, des = surf.detectAndCompute(im_grey,None)
                #img2 = cv2.drawKeypoints(im_grey,kp,None,(255,0,0),4)
                cv2.imshow('img', im_gray)
                cv2.waitKey(1)
                '''
        #except:
            #print("no frame")

    

# Create a thread to run image viewing in the background
recorder = Thread(target=imgOut, daemon=True) # daemon to ensure threads are killed
recorder.start()

#tello.takeoff()
time.sleep(5)

try:
    while True:
        #Image processing can happen here haha
        print("True")
        True
except KeyboardInterrupt:
    print("End Program")
    pass


#recorder.join()

