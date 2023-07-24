# Map Initialization
# Written by Walter Stark
# Sources: https://ch.mathworks.com/help/vision/ug/monocular-visual-simultaneous-localization-and-mapping.html

# Notes for future implementation:
# Need to check whether images are distorted 
# Make functions such that they don't require this database
# TODO: implement bag of features 



from skimage.io import imread_collection
import cv2
import os
import sys
import datetime
import numpy as np
from matplotlib import pyplot as plt


# Function for determining camera properties
def determineCameraProperties ():
    print("Camera Properties Not Found")


def main():
    # Create collection of images
    col_dir = os.path.dirname(os.getcwd()) + '/SLAM_Data/rgbd_dataset_freiburg3_long_office_household/rgb/*.png'
    print(col_dir)
    col = imread_collection(col_dir)
    
    # Find image intrinsics 
    focalLength = [535.4, 539.2]
    principalPoint = [320.1, 247.6]
    

    # Properties of ORB
    scaleFactor = 1.2
    numLevels   = 8
    numPoints   = 1000
    
    # Initialize Map
    mapInit(scaleFactor, numLevels, numPoints, col, focalLength, principalPoint)
    
    

# Map initialization
def mapInit(scaleFactor, numLevels, numPoints, col, focalLength, principalPoint):
    
    currentFrameNum = 0
    # Find the first image
    img1 = col[currentFrameNum]
    imageSize = [img1.shape[1],img1.shape[0]]
    # Extract Features
    [preDes, preKp] = helperDetectAndExtractFeatures(img1, scaleFactor, numLevels, numPoints); 

    currentFrameNum = currentFrameNum + 1
    currentImage = img1

    initialized = False

    # Initialization loop
    while not initialized and currentFrameNum < len(col):
        print("Arrived")
        currentImage = col[currentFrameNum]
        [currentDes, currentKp] = helperDetectAndExtractFeatures(currentImage, scaleFactor, numLevels, numPoints); 
        currentFrameNum = currentFrameNum + 1

        # Create BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match desc
        matches = bf.match(preDes,currentDes)

        good_matches = [m for m in matches if m.distance < 10 * min(matches, key=lambda x: x.distance).distance]
        print(len(good_matches))
        # Sort Descriptors on order of distance
        #matches = sorted(matches, key = lambda x:x.distance)
        
        # Check to see whether to continue to next frame
        minMatches = 100
        if len(matches) < minMatches:
            continue



        print(len(matches))
        # Init Point Matches Matrix
        p1 =[]
        p2 = []
        # Find Key Point Matches
        
        for match in good_matches:
            p1.append(preKp[match.queryIdx].pt)
            p2.append(currentKp[match.trainIdx].pt)
        

        print("Check point 1")
        # TODO: Potentially need to add in homography
        # Find Fundamental Matrix
        p1 = np.float32(p1)
        #print(len(p1))
        p2 = np.float32(p2)
        #F, mask = cv2.findFundamentalMat(p1,p2,cv2.FM_LMEDS)
        # We select only inlier points
        #pInlier1 = p1[mask.ravel()==1]
        #pInlier2 = p2[mask.ravel()==1]

        # Camera matrix of camera properties
        fx = focalLength[0]
        fy = focalLength[1]
        cx = principalPoint[0]
        cy = principalPoint[1]
        cameraMatrix = np.asarray([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
        
        
        # Normalize for Esential Matrix calaculation
        #pts_1_norm = cv2.undistortPoints(np.expand_dims(p1, axis=1), cameraMatrix=cameraMatrix, distCoeffs=None)
        #pts_2_norm = cv2.undistortPoints(np.expand_dims(p2, axis=1), cameraMatrix=cameraMatrix, distCoeffs=None)

        

        
        
        [E, mask] = cv2.findEssentialMat(p1, p2, cameraMatrix,  cv2.RANSAC)
        # Determine position (R is rotation matrix, t is translation)
        [points, R, t,  mask] = cv2.recoverPose(E, p1, p2)
        
        
        # Find 3D Points
        M_2 = np.hstack((R, t))
        M_1 = np.hstack((np.eye(3, 3), np.zeros((3, 1)))) 
        P_1 = np.dot(cameraMatrix,  M_1)
        P_2 = np.dot(cameraMatrix,  M_2)
       
        #print(np.expand_dims(pInlier1, axis=1))
        
        point_4d_hom = cv2.triangulatePoints(P_1, P_2, p1.T, p2.T)
        
        # Convert homogeneous coordinates to 3D Cartesian coordinates
        triangulated_points_cartesian = cv2.convertPointsFromHomogeneous(point_4d_hom.T)

        # Extract the 3D coordinates
        x_coords = triangulated_points_cartesian[:, 0, 0]
        y_coords = triangulated_points_cartesian[:, 0, 1]
        z_coords = triangulated_points_cartesian[:, 0, 2]
        
        # syntax for 3-D projection
        ax = plt.axes(projection ='3d')

        ax.scatter(x_coords,y_coords,z_coords, c='r', marker='o')
        
       


        plt.show()
        # Check if enough inliers are found
        #if (validFraction < 0.9 or len(t)==3):
            #continue
        

        #TODO: Add isValid method for triangulation

        initialized = True

# Store initial Key Frames and Points


    
                



# Detect and extract ORB features
def helperDetectAndExtractFeatures(Irgb, scale, levels, points):
    # Change to gray scale
    Igray = cv2.cvtColor(Irgb, cv2.COLOR_BGR2GRAY)
    
    # Create ORB Detector
    orb = cv2.ORB_create()
    orb.setScaleFactor(scale)
    orb.setNLevels(levels)
    orb.setMaxFeatures(points)
    
    # Compute the descriptors
    kp, des = orb.detectAndCompute(Igray,None) 
    return [des, kp]

if __name__ == "__main__":
    main()