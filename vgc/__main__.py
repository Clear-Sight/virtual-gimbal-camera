from .config import CONFIG
from .pipeline import Pipeline

"""
This is the main file for virtual-gimbal-camera.
This file is the root of the project.
"""

__version__ = "1.0.0"


def main():
    pipeline = Pipeline()
    pipeline.start()

if __name__ == '__main__':
    main()
