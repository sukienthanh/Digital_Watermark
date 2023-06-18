import cv2
import numpy as np
import math
def psnr(path1, path2):

    image1=cv2.imread(path1,0)
    image2=cv2.imread(path2,0)    
   
    psnr = cv2.PSNR(image1, image2)
    return psnr




