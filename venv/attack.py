import numpy as np 
import cv2
from scipy import ndimage
import exposure

def compress(path, percent):
    # Đọc ảnh đầu vào
    img = cv2.imread(path,0)

    # Nén ảnh đầu vào với mức độ nén theo % và định dạng JPG
    _, enc_img = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), int(percent)])

    # Giải nén ảnh
    dec_img = cv2.imdecode(enc_img, cv2.IMREAD_GRAYSCALE)

    return dec_img

#Noise attack
def noise_attack(path, percent):    
    img = cv2.imread(path,0) 
    # lấy giá trị trung bình điểm ảnh
    #mean = np.mean(img)
    # độ lệch chuẩn 
    stddev = np.std(img)
    noise_stddev = stddev * (int(percent)/100)
    noise = np.zeros(img.shape, np.uint8)
    # tạo mảng nhiễu có kích thước bằng ảnh
    cv2.randn(noise, 0, noise_stddev)
    # thêm nhiễu vào ảnh    
    noisy_img = cv2.add(img, noise)
    return noisy_img

#Crop attack
def crop_attack(path, percent ):

    img = cv2.imread(path,0)    
    height, width = img.shape

    # chiều cao mới sau khi cắt theo phần trăm
    new_height = int(height * (100- int(percent))/100)

    # cắt ảnh theo chiều dọc
    img_cropped = img[0:new_height, 0:width]

    # tạo mảng chứa toàn giá trị 0, kích thước bằng ảnh ban đầu
    img_new = np.zeros((height, width), dtype=np.uint8)

    # chép toàn bộ ảnh phần cắt vào mảng 0 vừa tạo bên trên
    img_new[0:new_height, 0:width] = img_cropped
    
    return img_new

#Rotation attack  
def rotation_attack(path, percent):    
    img = cv2.imread(path) 
    M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), int(percent), 1)
    img_rotated = cv2.warpAffine(img, M, img.shape[:2])
    return img_rotated


