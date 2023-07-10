#Test-takeoff.py
# Written by Walter Stark



import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

# Connect to Tello
tello.connect()


keepRecording = True
# Start Stream
tello.streamon()

print(tello.get_battery())
# Turn on down vision
tello.send_command_with_return("downvision 1")
downvision = True


# Create a function to output images
def imgOut():
 
    
    # Check to see if recording has finished
    while keepRecording:
        # Try Catch added in case no frame when looking downward
        #try:
            if(downvision):
                singular_frame = tello.get_frame_read().frame
                cropped_img = singular_frame[0:240, 0:320]
                cv2.imshow('img', cropped_img)
                cv2.waitKey(1)
            else: 
                singular_frame = tello.get_frame_read().frame
                img = cv2.resize(singular_frame, (360, 240))
                im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cv2.imshow('img', im_rgb)
                cv2.waitKey(1)
        #except:
            #print("no frame")

    

# Create a thread to run image viewing in the background
recorder = Thread(target=imgOut)
recorder.start()

#tello.takeoff()
time.sleep(10)
#tello.move_up(100)
#tello.rotate_counter_clockwise(360)
#tello.land()

keepRecording = False
recorder.join()

