from time import sleep
from vgc.camera_filter import CameraFilter 

def test_camerafilter():
    """Testing the Came"""
    cf = CameraFilter([])
    sleep(4)
    cf.update(6, 10, 2)
    sleep(4)
    cf.stop()
    sleep(2)

    assert True

    