"""Filters a video stream.

"""
import threading
import cv2

from .filter import Filter


class cameraFilter(Filter):
    """Filters a video stream
            
        This filter rotates and cropps a video stream according to a pitch, a jaw and a zoom variable . 
        The pitch, jaw and zoom variables are updated asynchronously through the update funciton.
    
    """

    def __init__(self, arg):
        """Docstring"""
        super().__init__()

        # Set defaults
        self.yaw_in, self.pitch_in, self.zoom_in = 0,0,1

        #Init thread
        self.sem = threading.Semaphore()
        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def __del__(self):
        """Docstring"""
        self.thread._delete()

    def update(self, jaw_in, pitch_in, zoom_in):
        """Docstring"""
        self.sem.acquire()
        self.jaw_in = jaw_in
        self.pitch_in = pitch_in
        self.zoom_in = zoom_in 
        self.sem.release()

    def start(self):
        """Docstring"""
        cap = cv2.VideoCapture(0)

        cnt = 0  # Initialize frame counter

        # Some characteristics from the original video
        w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Croping values
        w = 640    
        h = 480 

        # The output
        #fourcc = cv2.VideoWriter_fourcc(*´XVID´)
        #out = cv2.VideoWriter(´result.avi´, fourcc, fps, (w, h))

        while(cap.isOpened()):
            ret, frame = cap.read()  # Capture frame by frame
            cnt += 1  # Counting the frames

            # Avoid problems when video finish 
            if ret:
                self.sem.acquire()
                # Get rotation matrix
                M = cv2.getRotationMatrix2D((w_frame/2, h_frame/2), self.jaw_in, 1)
                # Aply rotation matrix
                rotated_frame = cv2.warpAffline(frame, M, (w_frame, h_frame))
                # Crop the frame
                crop_frame = cv2.getRectSubPix(rotated_frame, (int(w*self.zoom_in), int(h*self.zoom_in)), (w_frame/2, h_frame/2 - h*self.zoom_in/2 + self.pitch_in))
                # Resize the frame
                final_frame = cv2.resize(crop_frame, (w,h))
                self.sem.release()

            cap.release()
            #out.release()
            cv2.destroyAllWindows()

