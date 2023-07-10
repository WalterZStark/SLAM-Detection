# SLAM-Detection
# 
# Code to test the basics of SLAM and CV object detection


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

