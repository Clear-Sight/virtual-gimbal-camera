
from .cameraFilter import CameraFilter 
from .viewController import ViewController
from .io.inputAdapter import InputAdapter

class Pipeline:
    """"
    Cross thread messaging pipeline

    __init__(self):
        Initializes the different modules
    start(self):
        Starts all the threads

    
    """

    def __init__(self):
        """ Initializes the different modules """
        self.camera_filter = CameraFilter(self)
        self.view_controller = ViewController(self)
        self.input_adapter = InputAdapter(self)

    def start(self):
        """ Starts all the threads """
        #self.camera_filter.start()
        self.view_controller.start()
        self.input_adapter.start()