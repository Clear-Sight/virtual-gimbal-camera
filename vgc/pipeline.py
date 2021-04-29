"""
Class Pipeline which initializes modules and works
as a middle hand for communication.
"""
from .log import logger
from .camera_filter import CameraFilter
from .view_controller_fast import ViewController
from .io.input_adapter import InputAdapter
from .autopilot_adapter import Vehicle
from .config import CONFIG

# pylint: disable=logging-fstring-interpolation
# Don't really know what this is, but the part of the code
# where pylint is angry works perfectly.

# pylint: disable=too-many-arguments
# 6 arguments are needed.

class Pipeline:
    """"
    Cross thread messaging pipeline.
    Threads communicates by calling pipeline's
    class functions

    __init__(self) --
        Initializes the different modules
    start(self) --
        Starts all the threads
    set_cropping(self, camera_yaw, camera_pitch, camera_roll, camera_zoom) --
        Sets the point for the filter to crop out, called from ViewController
    push_usr_msg(self, usr_msg) --
        Updates view_controller with the user message
        from input_adapter to view_controller.
    autopilot_update(self, roll, yaw, pitch, height, lon, lat) --
        Updates view_controller with the values
        from autopilot to view_controller.
    """

    def __init__(self):
        """ Initializes the different modules """
        self.camera_filter = CameraFilter(self)
        self.view_controller = ViewController(self)
        self.input_adapter = InputAdapter(self)
        if CONFIG["local"]:
            self.autopilot = Vehicle(self)

    def start(self):
        """ Starts all the threads """
        logger.info('Starting threads')
        self.camera_filter.start()
        self.view_controller.start()
        self.input_adapter.start()
        if CONFIG["local"]:
            self.autopilot.start()


    def set_cropping(self, camera_yaw, camera_pitch, camera_roll,\
        camera_zoom=2):
        """ Sets the point for the filter to crop out """
        logger.debug(f"set cropping: yaw {camera_yaw}, pitch {camera_pitch},\
            zoom {camera_zoom}")
        self.camera_filter.update(camera_yaw=camera_yaw,
        camera_pitch=camera_pitch, camera_roll=camera_roll,\
            camera_zoom=camera_zoom)

    def push_usr_msg(self, usr_msg):
        """
        Updates view_controller with the user message
        from input_adapter to view_controller.
        """
        logger.debug(f"user input recieved: {usr_msg}")
        self.view_controller.update_server_input(
            usr_msg["angle"], usr_msg["compass"],
            usr_msg["lock_on"], usr_msg["zoom"])


    def autopilot_update(self, roll, yaw, pitch, height, lon, lat):
        """
        Updates view_controller with the values
        from autopilot to view_controller.
        """
        logger.debug(f"autopilot:{[roll, yaw, pitch, height, lon, lat]}")
        self.view_controller.update_autopilot_input(roll=roll, yaw=yaw,
                pitch=pitch, height=height, lon=lon, lat=lat)
