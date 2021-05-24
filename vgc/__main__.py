"""
This is the main file for virtual-gimbal-camera.
This file is the root of the project.
"""

from .pipeline import Pipeline

__version__ = "1.0.0"


def main():
    """
    initalise the systems by s
    tarting all the treads
    """
    pipeline = Pipeline()
    pipeline.start()

if __name__ == '__main__':
    main()
