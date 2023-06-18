import numpy as np  
import cv2
def ncc(path1, path2):

    img1 = cv2.imread(path1, 0)
    img2 = cv2.imread(path2, 0)

    img1 = np.float32(img1)
    img2 = np.float32(img2)

    # Calculate normalized correlation 
    # Using OpenCV's normalized_correlation()
    corr = cv2.compareHist(img1, img2, cv2.HISTCMP_CORREL)

    return corr