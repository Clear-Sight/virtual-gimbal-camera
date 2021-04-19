
from .camera_filter import CameraFilter
from .view_controller import ViewController
from .io.input_adapter import InputAdapter
from .config import CONFIG

class Pipeline:
    """"
    Cross thread messaging pipeline.
    Threads communicates by calling pipeline's
    class functions

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


    def set_cropping(self, camera_yaw, camera_pitch, camera_zoom=2):
        """" Sets the point for the filter to crop out """
        if CONFIG["debug"]:
            print(f"set cropping: yaw {camera_yaw}, pitch {camera_pitch}, zoom {camera_zoom}")
        self.camera_filter.update(camera_yaw=camera_yaw, camera_pitch=camera_pitch, camera_zoom=camera_zoom)


    def push_usr_msg(self, usr_msg):
        """
        Updates view_controller with the user message
        from input_adapter to view_controller.
        """
        if CONFIG["debug"]:
            print(f"user input recieved: {usr_msg}")
        self.view_controller.update_server_input(
            usr_msg["angle"], usr_msg["compass"], usr_msg["lock_on"])
