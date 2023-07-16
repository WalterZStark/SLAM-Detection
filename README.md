# SLAM-Detection
# 
# Code to test the basics of SLAM and CV object detection


7-16-2023
- Haven't updated the README in a couple days
- Fixed threading issues
- Also added Yolo segmentation in YOLO.py
- Renamed test-takeoff.py to test_takeoff.py due to issues calling it with the dash
- created main.py as the main file for running all drone code

![First Image](images/7_16_Bottom_Camera.png)
![Second Image](images/7_16_Front_Camera.png)




7-10-2023
- Downgraded OpenCv to 4.5.2.52 to fix "raise TelloException('Failed to grab video frames from video stream')"
- Made thread a daemon thread to be killed when program exits
- created retrieve_images.py to get images from both the laptop camera and drone camera

7-9-2023 - Second Push
- Updated DJI Tello Firmware to latest version (2.05.01.19) on app to get down view capabilities 
- Added down viewing capabilities


7-9-2023
- Make sure to turn on Airplane mode before flying
- Recieved Error: "djitellopy.tello.TelloException: Command 'left 100' was unsuccessful for 4 tries. Latest response:      'error No valid imu'"
    - Solved by holding down power button for 5 seconds and resetting wifi
- Implementing Camera Feed
    - Used inspiration from: https://github.com/damiafuentes/DJITelloPy/blob/master/examples/record-video.py
- Issues with Camera Feed being Blue
    - Solved with "im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)"

