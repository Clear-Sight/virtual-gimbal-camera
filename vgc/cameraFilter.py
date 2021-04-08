"""Filters a video stream.
"""
import threading
import cv2

from .filter import Filter
from .io import outputAdapter


class CameraFilter(Filter):
    """Filters a video stream

        This filter rotates and cropps a video stream according to
        a pitch, a jaw and a zoom variable. The pistch, jaw and zoom
        variables are updated asynchronously through the update funciton.
    """

    def __init__(self):
        """Initializes the Camerafilter.

        Sets some default starting values
        Initializes and starts the CameraFilter thread.
        """

        super().__init__()

        # Set defaults
        self.jaw_in, self.pitch_in, self.zoom_in = 0,0,1
        self.stopped = False

        # Init thread
        self.sem = threading.Semaphore()
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
        self.output_adapter = outputAdapter.outputAdapter()

    def __del__(self):
        """Deletes the thread if the CameraFilter is deleted."""
        self.thread._delete()

    def update(self, jaw_in, pitch_in, zoom_in):
        """Updates the cropping values of the CameraFilter."""
        self.sem.acquire()
        self.jaw_in = jaw_in
        self.pitch_in = pitch_in
        self.zoom_in = zoom_in
        self.sem.release()

    def stop(self):
        """Stops the Camerafilter."""
        self.stopped=True

    def start(self):
        """The main function of the class.

        Takes input videostream input.
        Crops and rotates according to jaw_in, pitch_in and zoom_in.
        Outputs the proccesed videostream.
        """
        cap = cv2.VideoCapture(0)

        cnt = 0  # Initialize frame counter

        # Some characteristics from the original video
        w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        #frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Croping values
        width = 640
        height = 480

        # The output, subject to change
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('result.avi', fourcc, fps, (width, height))

        while(cap.isOpened() and not self.stopped):
            ret, frame = cap.read()  # Capture frame by frames
            cnt += 1  # Counting the frames

            # Avoid problems when video finish
            if ret:
                self.sem.acquire()
                # Get rotation matrix
                matrix = cv2.getRotationMatrix2D((w_frame/2, h_frame/2), self.jaw_in, 1)
                # Aply rotation matrix
                rotated_frame = cv2.warpAffine(frame, matrix, (w_frame, h_frame))
                # Crop the frame
                crop_frame = cv2.getRectSubPix(rotated_frame, (int(width*self.zoom_in),
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
                    cv2.destroyAllWindows()
                    out.write(final_frame)

                self.sem.release()

        cap.release()

        out.release()
        cv2.destroyAllWindows()
