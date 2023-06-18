import cv2
import numpy as np
import pywt
import psnr
import ncc
import attack

def embed(coverName , wmName, alpha):
    coverPath = 'venv/static/cover/' + coverName
    wmPath = 'venv/static/watermark/' + wmName
    embedPath = 'venv/static/watermarked/' + coverName
    alpha = float(alpha) 

    cover = cv2.imread(coverPath,0)     
    #DWT
    coefficients = pywt.wavedec2(cover, wavelet='haar', level = 1)
    # băng LL = Coefficients[0]
    LLSize = min(coefficients[0].shape)
    
    #SVD
    Uc, Sc, Vc = np.linalg.svd(coefficients[0])

    watermark = cv2.imread(wmPath,0) 

    #SVD  
    Uw, Sw, Vw = np.linalg.svd(watermark)    

    #nhúng
    Sc = Sc + alpha * Sw    

    LLnew = np.zeros((LLSize, LLSize))
    #I-SVD
    LLnew = Uc.dot(np.diag(Sc)).dot(Vc)
    
    #thay LL = LL'
    coefficients[0] = LLnew

    #I-DWT
    grayLayer = pywt.waverec2(coefficients, 'haar')  

    # lưu ảnh đã nhúng thủy vân
    cv2.imwrite(embedPath, grayLayer)

    # tính PSNR
    psnrval = psnr.psnr(embedPath, coverPath)
    
    return round(psnrval, 5)

def extract(embedName, wmName, alpha):

    extractedPath = 'venv/static/extracted/' + wmName    
    coverPath = 'venv/static/cover/' + embedName
    wmPath = 'venv/static/watermark/' + wmName
    embedPath = 'venv/static/watermarked/' + embedName 
    alpha = float(alpha) 

   
    cover_img=cv2.imread(coverPath, 0)   
    embed_img=cv2.imread(embedPath, 0)

    #DWT
    C = pywt.wavedec2(cover_img, wavelet='haar', level = 1)    
    Cwc= pywt.wavedec2(embed_img, wavelet='haar', level = 1)
    
    #SVD
    Uwc, Swc, Vwc = np.linalg.svd(Cwc[0])
    Uc, Sc, Vc = np.linalg.svd(C[0])

    original_watermark =  cv2.imread(wmPath,0)

    #SVD
    Uw, Sw, Vw = np.linalg.svd(original_watermark,0)
    
    #trích xuất
    Sw = ( Swc - Sc ) / alpha

    #I-SVD
    extracted_wm = Uw.dot(np.diag(Sw)).dot(Vw)
    
    # lưu ảnh trích xuất được vào file 
    cv2.imwrite(extractedPath, extracted_wm)

    # tính NCC
    nccVal = ncc.ncc(extractedPath, wmPath)

    return round(nccVal, 5)
   
def extract_after_attacked(embedName, wmName, method, alpha):

    alpha = float(alpha)     
    
    extractedAttacked = 'venv/static/attacked/extracted/' +method + '_' + wmName
    coverPath = 'venv/static/cover/' + embedName
    wmPath = 'venv/static/watermark/' + wmName
    embedPath = 'venv/static/attacked/' + method + '_' + embedName
  
    cover_img=cv2.imread(coverPath, 0)   
    embed_img=cv2.imread(embedPath, 0)

    #DWT
    C = pywt.wavedec2(cover_img, wavelet='haar', level = 1)    
    Cwc= pywt.wavedec2(embed_img, wavelet='haar', level = 1)
    
    #SVD
    Uwc, Swc, Vwc = np.linalg.svd(Cwc[0])
    Uc, Sc, Vc = np.linalg.svd(C[0])

    original_watermark =  cv2.imread(wmPath,0)

    #SVD
    Uw, Sw, Vw = np.linalg.svd(original_watermark,0)
    
    #trích xuất
    Sw = ( Swc - Sc ) / alpha

    #I-SVD
    extracted_wm = Uw.dot(np.diag(Sw)).dot(Vw)
    
    # lưu ảnh trích xuất được vào file 
    cv2.imwrite(extractedAttacked, extracted_wm)

    # tính NCC
    nccVal = ncc.ncc(extractedAttacked, wmPath)

    return round(nccVal,5)   
    
def attackImage(method, attackedName, percent):
    embedPath = 'venv/static/watermarked/'
    attackedPath  = attackedPath = 'venv/static/attacked/' + method+'_' + percent + "_" + attackedName

    if method == "rotate" :
        attacked = attack.rotation_attack(embedPath + attackedName, percent)
        cv2.imwrite(attackedPath, attacked)
    elif method == 'crop':
        attacked = attack.crop_attack(embedPath + attackedName, percent)
        cv2.imwrite(attackedPath, attacked)
    elif method == 'noise':
        attacked = attack.noise_attack(embedPath + attackedName, percent)
        cv2.imwrite(attackedPath, attacked)
    elif method == 'compress':
        attacked = attack.noise_attack(embedPath + attackedName,percent)
        cv2.imwrite(attackedPath, attacked)
            
    psnrVal = psnr.psnr(attackedPath, embedPath + attackedName)
    return round(psnrVal, 5)

