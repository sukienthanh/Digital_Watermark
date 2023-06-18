import numpy as np
def logistic(x, r, len):
    # r = 3.9
    logistic = []
    for i in range(len):
        x = r * x * (1 - x)
        tmp = int(x*len)         
        logistic.append(tmp)        
        
    return logistic

