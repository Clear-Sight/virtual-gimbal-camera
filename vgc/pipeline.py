
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

    def push_usr_msg(self, usr_msg):
        """
        Updates view_controller with the user message
        from input_adapter to view_controller.
        """
        self.view_controller.update_server_input(
            usr_msg["compass"], usr_msg["angle"], usr_msg["lock_on"])
