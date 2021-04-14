
from .camera_filter import CameraFilter
from .view_controller import ViewController
from .io.input_adapter import InputAdapter

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
        self.camera_filter.start()
        self.view_controller.start()
        self.input_adapter.start()


    def set_cromping_point(self, phi, theta):
        """" Sets the point for the filter to crop out """
        # BUG: THIS NEED TO BE FIXED! dont know witch whan is on and zoom??? 
        self.camera_filter.update(jaw_in=phi, pitch_in=theta, zoom_in=0)
