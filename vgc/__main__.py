import cv2
from . import io
from . import cameraFilter
from . import config
from .pipeline import Pipeline

"""
This is the main file for virtual-gimbal-camera.
This file is the root of the project.  
"""

__version__ = "0.1.0"


def main():
    pipeline = Pipeline()
    pipeline.start()

if __name__ == '__main__':
    if config.CONFIG['debug']:
        main()
