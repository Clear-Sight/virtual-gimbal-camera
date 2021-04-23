"""
This module calls functions and passes arguments to the c-file which
holds all of the fast math functions.

Functions:
cos(x)
sin(x)
tan(x)
arctan(x)
arccos(x)
"""
# pylint: disable=invalid-name
# snake-case names is not needed for mathematical functions.
from ctypes import CDLL, c_float
from numpy import arccos as acos
SO_FILE = "./vgc/trigonometric_fast.so"
tf = CDLL(SO_FILE)

SCALE = 1000000

def cos(x):
    """
    A fast version of the periodic function cosine(x),
    where x is in radians.
    """
    ans = tf.cos_t(c_float(x)) / SCALE
    if ans > 1:
        return 1
    if ans < -1:
        return -1
    return ans

def sin(x):
    """
    A fast version of the periodic function sine(x),
    where x is in radians.
    """
    ans = tf.sin_t(c_float(x)) / SCALE
    if ans > 1:
        return 1
    if ans < -1:
        return -1
    return ans

def tan(x):
    """
    A fast version of the periodic function tangens(x),
    where x is in radians.
    """
    if x < 0:
        return -tf.tan_t(c_float(-x)) / SCALE
    else:
        return tf.tan_t(c_float(x)) / SCALE

def arctan(x):
    """
    A fast version of the periodic function arctangens(x),
    where x is in radians.
    """
    if x < 0:
        return -tf.arctan_t_2(c_float(-x)) / SCALE
    else:
        return tf.arctan_t_2(c_float(x)) / SCALE

def arccos(x):
    """
    A fast version of the periodic function arccosine(x),
    where x is in radians.
    """
    if x < -1:
        x = -1
    if x > 1:
        x = 1
    return acos(x)
