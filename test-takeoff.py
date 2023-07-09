#Test-takeoff.py




'''
from djitellopy import Tello

tello = Tello()



tello.connect()
tello.takeoff()
tello.get_current_state()
tello.move_left(100)
tello.rotate_counter_clockwise(90)
tello.move_forward(100)


# Command to get downvision camera
tello.send_command_with_return("downvision 1")


tello.land()
'''


import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
print(tello.get_battery())



#rame_read = tello.get_frame_read()



# Imae output
def imgOut():
    # Create a function to output images
    #height, width, _ = frame_read.frame.shape
    #video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        singular_frame = tello.get_frame_read().frame
        img = cv2.resize(singular_frame, (360, 240))
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('img', im_rgb)
        cv2.waitKey(1)

    


recorder = Thread(target=imgOut)
recorder.start()

#tello.takeoff()
time.sleep(10)
#tello.move_up(100)
#tello.rotate_counter_clockwise(360)
#tello.land()

keepRecording = False
recorder.join()

