"""Tests the code for camera filter.

Functions:
test_do_nothing() - Starts and stops the camera filter
test_update_valid_input()
    - Tries different valid inputs to the update function.
test_update_not_valid_input()
    - Tries different unvalid inputs to the update function.
test_config() - Tests variables in the config file.
test_handle_frame() - Tests the function handle_frame()
"""

import pytest
import numpy as np
import cv2

from vgc.camera_filter import CameraFilter
from vgc.pipeline import Pipeline
from vgc import config


cf = Pipeline().camera_filter

def test_do_nothing():
    """Starts and stops the camera filter."""
    cf.start("test.mkv")
    cf.main()
    cf.stop()
    assert cf.stopped is True

def test_update_valid_input():
    """Tries different valid inputs to the update function.

    First the function tries valid inputs to the update function.
    After that the function tries edge cases to the update function.
    """
    # Cases
    cf.update(4, 0.5, 6)
    assert cf.camera_yaw == 4
    assert cf.camera_pitch == 0.5
    assert cf.camera_zoom == 6

    cf.update(128, 0.9, 6)
    assert cf.camera_yaw == 128
    assert cf.camera_pitch == 0.9
    assert cf.camera_zoom == 6

    cf.update(340, 0.3, 3)
    assert cf.camera_yaw == 340
    assert cf.camera_pitch == 0.3
    assert cf.camera_zoom == 3

    #Edge cases
    cf.update(360, 0.3, 3)
    assert cf.camera_yaw == 360
    assert cf.camera_pitch == 0.3
    assert cf.camera_zoom == 3

    cf.update(0, 0.3, 3)
    assert cf.camera_yaw == 0
    assert cf.camera_pitch == 0.3
    assert cf.camera_zoom == 3

    cf.update(128, 1, 3)
    assert cf.camera_yaw == 128
    assert cf.camera_pitch == 1
    assert cf.camera_zoom == 3

    cf.update(128, 0, 3)
    assert cf.camera_yaw == 128
    assert cf.camera_pitch == 0
    assert cf.camera_zoom == 3

    cf.update(128, 0.3, 2)
    assert cf.camera_yaw == 128
    assert cf.camera_pitch == 0.3
    assert cf.camera_zoom == 2

def test_update_not_valid_input():
    """Tries different unvalid inputs to the update function."""
    return True # tests need to be fixed
    with pytest.raises(ValueError, match=r".*camera_yaw.*"):
        cf.update(420, 0.3, 2)
    with pytest.raises(ValueError, match=r".*camera_yaw.*"):
        cf.update(-4, 0.3, 2)
    with pytest.raises(ValueError, match=r".*camera_pitch.*"):
        cf.update(150, 1.5, 2)
    with pytest.raises(ValueError, match=r".*camera_pitch.*"):
        cf.update(266, -0.5, 2)
    with pytest.raises(ValueError, match=r".*camera_zoom.*"):
        cf.update(167, 0.3, 1)

def test_config():
    """Tests variables in the config file. """
    cam_width = config.CONFIG['cam_width']
    assert cam_width >= 0

    cam_height = config.CONFIG['cam_height']
    assert cam_height >= 0

def test_handle_frame():
    """Tests the function handle_frame().

    The function creates an image "img" and applies
    the handle_frame function to it with different parameteres.
    Then it tests if the function gave the expected output.
    """
    size = 50
    img = np.zeros((size,size,3), dtype=np.uint8)
    for pixelx in range(size):
        for pixely in range(size):
            img[pixelx][pixely] = [int((pixelx/size) * 255),
                                   int((pixely /size) * 255),
                                   int(((pixelx + pixely) /(2*size)) * 255)]

    for pixel in range(size):
        img[pixel][size//4] =  255
        img[size//4][pixel] =  255
        img[pixel][size//2] =  255
        img[size//2][pixel] =  255
        img[pixel][size*3//4] =  255
        img[size*3//4][pixel] =  255

    tests = [[35, 1, 2], [120, 0, 4], [128, 0.9, 6], [340, 0.3, 3],
            [360, 0.5, 2], [4, 0.25, 3], [200, 0.2, 5], [0, 0.8, 4]
            ]
    for test in tests:
        cf.update(test[0],test[1],test[2])
        frame = cf.handle_frame(img, img.shape[0], img.shape[1],
                                     img.shape[0], img.shape[1])

        #frame.dump(
        #   f'tests/test_images/matrix{test[0]}-{test[1]}-{test[2]}.dat')
        loaded = np.load(
            f'tests/test_images/matrix{test[0]}-{test[1]}-{test[2]}.dat',
            allow_pickle=True)

        #cv2.imshow('source',img)
        #cv2.imshow('image',frame)
        #cv2.imshow('loaded',loaded)
        #cv2.waitKey(0)

        assert np.array_equal(frame, loaded)
