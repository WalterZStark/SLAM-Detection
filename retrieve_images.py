# retrieve_images.py
# Written by Walter Stark

import cv2

# Variable for sending a command to the drone to switch the camera view
front = True

# Function to retrieve feed from laptop camera feed or drone feed
# drone: True specifies that the drone will be used while False implies the laptop feed will be used
# front_camera: True specifies that the drones front camera will be used, False implies bottom camera will be used
def retrieve(drone,front_camera,tello,vid):
    global front
    img_out = None
    # Check if drone or laptop feed is being used
    if(drone):
        # Check if front camera used
        if(front_camera):
            # Send command to turn on front camera
            if(not front):
                tello.send_command_with_return("downvision 0")
                front = True
            singular_frame = tello.get_frame_read().frame
            img = cv2.resize(singular_frame, (360, 240))
            img_out = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            # Send command to turn on down camera
            if(front):
                tello.send_command_with_return("downvision 1")
                front = False
            singular_frame = tello.get_frame_read().frame
            img_out = singular_frame[0:240, 0:320]
        
    else:
        ret, img_out = vid.read()

    # Return the output image
    return img_out
           



