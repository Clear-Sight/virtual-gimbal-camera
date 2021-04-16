from ctypes import CDLL, c_float
so_file = "C:/python/kandidat/trigonometric_fast.so"
tf = CDLL(so_file)
from numpy import arccos as acos

def cos(x):
    ans = tf.cos_t(c_float(x)) / 1000000
    if(ans > 1):
        return 1
    if(ans < -1):
        return -1
    return(ans)

def sin(x):
    ans = tf.sin_t(c_float(x)) / 1000000
    if(ans > 1):
        return 1
    if(ans < -1):
        return -1
    return(ans)

def tan(x):
    if(x < 0):
        return(-tf.tan_t(c_float(-x)) / 1000000)
    else:
        return(tf.tan_t(c_float(x)) / 1000000)

def arctan(x):
    if(x < 0):
        return(-tf.arctan_t_2(c_float(-x)) / 1000000)
    else:
        return(tf.arctan_t_2(c_float(x)) / 1000000)

def arccos(x):
    if(x < -1):
        x = -1
    if(x > 1):
        x = 1
    return acos(x)