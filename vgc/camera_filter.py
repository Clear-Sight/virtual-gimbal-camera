"""Filters a video stream.

Class CameraFilter - Crops, rotates and scales a videostream

Functions in CameraFiler:
    __init__(self) - Initialize variables
    __del__(self) - Deletes the thread
    update(self, jaw_in, pitch_in, zoom_in) - Updates variables
    stop(self) - Stops the camera filter
    start(self) - Starts the camera filter
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
            update(self, jaw_in, pitch_in, zoom_in) - Updates variables
            stop(self) - Stops the camera filter
            start(self) - Starts the camera filter
            main(self) - Main loop of the camerafilter
    """

    def __init__(self, pipeline):
        """Initializes the Camerafilter.

        Sets some default starting values
        Initializes and starts the CameraFilter thread.
        """

        #super().__init__() # dose not seem to be needed any more 
        self.pipeline = pipeline

        # Set defaults
        self.jaw_in, self.pitch_in, self.zoom_in = 0,0,1
        self.stopped = False

        # Init thread
        self.semaphore = threading.Semaphore()
        self.thread = threading.Thread(target=self.main)

        # Get ouptuptAdapter
        self.output_adapter = output_adapter.OutputAdapter()

    def update(self, jaw_in, pitch_in, zoom_in):
        """Updates the cropping values of the CameraFilter."""
        self.semaphore.acquire()
        self.jaw_in = jaw_in
        self.pitch_in = pitch_in
        self.zoom_in = zoom_in
        self.semaphore.release()

    def stop(self):
        """Stops the Camerafilter."""
        self.stopped=True

    def start(self):
        """Starts the Camerafilter."""
        self.thread.start()

    def main(self):
        """The main function of the class.

        Takes input videostream input.
        Crops and rotates according to jaw_in, pitch_in and zoom_in.
        Outputs the proccesed videostream.
        """
        cap = cv2.VideoCapture(config.CONFIG['cam_input'])

        if not cap.isOpened():
            raise ValueError("No camera")

        cnt = 0  # Initialize frame counter

        # Some characteristics from the original video
        w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Getting width and height of output from config file
        width = config.CONFIG['cam_width']
        height = config.CONFIG['cam_height']


        while not self.stopped:
            ret, frame = cap.read()  # Capture frame by frames
            cnt += 1  # Counting the frames

            # Avoid problems when video finish
            if ret:
                self.semaphore.acquire() # Get rotation matrix
                matrix = cv2.getRotationMatrix2D((w_frame/2, h_frame/2),
                                                self.jaw_in, 1)
                # Apply rotation matrix
                rotated_frame = cv2.warpAffine(frame, matrix,
                                               (w_frame, h_frame))
                # Crop the frame
                crop_frame = cv2.getRectSubPix(rotated_frame,
                                               (int(width*self.zoom_in),
                                                int(height*self.zoom_in)),
                                               (w_frame/2, h_frame/2
                                                - height*self.zoom_in/2
                                                + self.pitch_in))
                # Resize the frame
                final_frame = cv2.resize(crop_frame, (width,height))
                try:
                    self.output_adapter.send(final_frame)
                    cv2.waitKey(1)
                except KeyboardInterrupt:
                    self.stopped = True


                self.semaphore.release()

        cap.release()

        cv2.destroyAllWindows()
