"""Filters a video stream.

Class CameraFilter - Crops, rotates and scales a videostream

Functions in CameraFiler:
    __init__(self) - Initialize variables
    __del__(self) - Deletes the thread
    update(self, camera_yaw , camera_pitch, camera_zoom) - Updates variables
    stop(self) - Stops the camera filter
    start(self) - Starts the camera filter
    handle_frame(self, frame, frame_width, frame_height,
                 out_width, out_height) - Crops and resizes a frame.
"""
import threading
import cv2

from .io import output_adapter
from . import config


class CameraFilter:
    """Filters a video stream.

        This filter rotates and cropps a video stream according to
        a pitch, a jaw and a zoom variable. The videostream is from
        a 180+ degree camera pointing straigt down. To mimic a gimal
        camera the pitch, jaw and zoom variables are the angle,
        rotation and zoom needed to look at a specific poriton of
        the 180+ degree video stream.
        The pitch, jaw and zoom variables are updated asynchronously
        through the update funciton.

        Functions in the class:
            __init__(self) - Initialize variables
            update(self, camera_yaw , camera_, camera_zoom)
                                        - Updates variables
            stop(self) - Stops the camera filter
            start(self) - Starts the camera filter
            main(self) - Main loop of the camerafilter
            handle_frame(self, frame, frame_width, frame_height,
                                            out_width, out_height)
                                        - Crops and resizes a frame.
    """

    def __init__(self, pipeline):
        """Initializes the Camerafilter.

        Sets some default starting values
        Initializes and starts the CameraFilter thread.
        """

        self.pipeline = pipeline

        # Init thread
        self.semaphore = threading.Semaphore()
        self.thread = threading.Thread(target=self.main)

        # Set Defaults
        self.camera_yaw , self.camera_pitch, self.camera_zoom = 0,0,4
        self.stopped = False
        self.camera_input = 0

        # Get ouptuptAdapter
        self.output_adapter = output_adapter.OutputAdapter()


    def update(self, camera_yaw , camera_pitch, camera_zoom):

        """Updates the cropping values of the CameraFilter."""

        if not 0 <= camera_yaw <= 360:
            raise ValueError("camera_yaw out of bounds (0 to 360)")

        if not 0 <= camera_pitch <= 1:
            raise ValueError("camera_pitch out of bounds (0 to 1)")

        if not 2 <= camera_zoom:
            raise ValueError("camera_zoom out of bounds ( >= 2)")

        self.semaphore.acquire()

        self.camera_yaw  = camera_yaw
        self.camera_pitch = camera_pitch
        self.camera_zoom = camera_zoom

        self.semaphore.release()

    def stop(self):
        """Stops the Camerafilter."""
        self.stopped = True
        self.thread.join()


    def start(self, camera_input=0):
        """Starts the Camerafilter."""
        # Set defaults
        self.camera_yaw , self.camera_pitch, self.camera_zoom = 0,0,4
        self.stopped = False
        self.camera_input = camera_input

        self.thread.start()

    def main(self):
        """The main function of the class.

        Takes input videostream input.
        Crops and rotates according to camera_yaw ,
        camera_pitch and camera_zoom.

        Outputs the proccesed videostream.
        """
        cap = cv2.VideoCapture(self.camera_input if self.camera_input
                                            else config.CONFIG['cam_input'])

        if not cap.isOpened():
            raise ValueError("No camera")

        cnt = 0  # Initialize frame counter

        # Some characteristics from the original video
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Getting width and height of output from config file
        width = config.CONFIG['cam_width']
        height = config.CONFIG['cam_height']


        while not self.stopped:
            ret, frame = cap.read()  # Capture frame by frames
            cnt += 1  # Counting the frames

            # Avoid problems when video finish

            if not ret:
                break

            self.semaphore.acquire() # Get rotation matrix
            final_frame = self.handle_frame(frame, frame_width,
                                            frame_height, width, height)
            try:
                self.output_adapter.send(final_frame)
                cv2.waitKey(1)
            except KeyboardInterrupt:
                self.stopped = True
            self.semaphore.release()

            cap.release()


        cv2.destroyAllWindows()

    def handle_frame(self, frame, frame_width, frame_height,
                                    out_width, out_height):
        """Handles the frame.

        Takes a frame, the width and height of the frame,
        and the width and the height of the croped frame as an input.
        Then the function converts the frame to a matrix, rotates it,
        and the crops the frame. The function returns a croped resized frame.
        """
        matrix = cv2.getRotationMatrix2D((frame_width/2, frame_height/2),
                                        self.camera_yaw , 1)
        # Apply rotation matrix
        rotated_frame = cv2.warpAffine(frame, matrix,
                                        (frame_width, frame_height))
        # Crop the frame
        relative_pitch = (frame_height/2 -
                          (out_height/2)/self.camera_zoom)* self.camera_pitch

        crop_frame = cv2.getRectSubPix(rotated_frame,
                                        (int(out_width/self.camera_zoom),
                                        int(out_height/self.camera_zoom)),
                                        (frame_width/2, frame_height/2
                                        - relative_pitch))
        # Resize the frame
        return cv2.resize(crop_frame, (out_width,out_height))