import logistic
import histogram
import cv2
import numpy as np
import pywt
import psnr
import ncc


def getGrayLayer(filename):   
    cover = cv2.imread("venv/static/cover/" + filename, 0)
    cv2.imwrite("venv/static/gray/" + filename, cover)

   