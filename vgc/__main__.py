import cv2
from . import primes
from . import buffer
from . import io
from . import cameraFilter

__version__ = "0.1.0"


def main():
    filter = cameraFilter.CameraFilter()
    filter.start()



if __name__ == '__main__':
    main()
