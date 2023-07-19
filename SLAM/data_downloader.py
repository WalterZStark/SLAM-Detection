# Script to Download Test Data
# Written by Walter Stark
# Adapted from Matlab code: https://ch.mathworks.com/help/vision/ug/monocular-visual-simultaneous-localization-and-mapping.html

import requests
from pathlib import Path
import os
import tarfile
from tqdm import tqdm

def downloadTest (url,fileName):
    
    print("Got to Function")
    # Check if test data has been downloaded
    path = Path('./'+fileName)
    if (not path.is_file()):
        '''
        print("Downloading SLAM Testing Data Set")
        r = requests.get(url,allow_redirects = True)
        open(fileName, 'wb').write(r.content)
        '''
        print("Downloading SLAM Testing Data Set")
        
        response = requests.get(url, stream=True)
        '''
        with tqdm.wrapattr(open(fileName, "wb"), "write", miniters=1,
                        total=int(response.headers.get('content-length', 0)),
                        desc=fileName) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)

        '''

        # Get the total content length from the response headers
        total_size = int(response.headers.get("content-length", 0))

        # Use the context manager to wrap the file write operation with tqdm
        with open(fileName, "wb") as fout:
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=fileName, miniters=1) as pbar:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)
                    pbar.update(len(chunk))

        print("Extracting SLAM Testing Data Set")
        my_tar = tarfile.open(fileName)
        my_tar.extractall('./SLAM_Data') # specify which folder to extract to
        my_tar.close()


    else:
        print('SLAM Testing Data Set Already Downloaded')

