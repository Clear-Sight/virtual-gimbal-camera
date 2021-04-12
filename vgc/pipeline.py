
from .cameraFilter import CameraFilter 

class Pipeline:

    def __init__(self):
        self.camerafilter = CameraFilter(self)
        #self.viewController = CameraFilter(self)
        
    def start(self):
        self.camerafilter.start()