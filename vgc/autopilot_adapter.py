"""
Software interface for the autopilot
"""
from .config import CONFIG
import time
from pymavlink import mavutil
import threading
import sys

class Vehicle:
    """ Class Vehicle represents the autopilot as vehicle. """

    def __init__(self, pipeline):
        """ Initiates connection """
        self.connection = mavutil.mavlink_connection("/dev/ttyAMA0", 57600)
        self.thread = threading.Thread(target=self.main)
        self.pipeline = pipeline
        self.cached_gps_data = None

    def get_attitude_massage(self):
        """ Refreshes vehicle values """
        return self.connection.recv_match(type ="ATTITUDE", blocking=True)

    def get_GPS_data_massage(self):
        """ Refreshes GPS data values """
        data = self.connection.recv_match(type ="GPS_RAW_INT")
        if data and data.get_type() == "BAD_DATA":
            print(data)
        if data.get_type() == "BAD_DATA" and mavutil.all_printable(data.data):
                sys.stdout.write(data.data)
                sys.stdout.flush()

        if not data and self.cached_gps_data:
            data = self.cached_gps_data
            self.cached_gps_data = None # might over write data due to ref
            return self.cached_gps_data
        elif not data and not self.cached_gps_data:
            data = self.connection.recv_match(type ="GPS_RAW_INT", blocking=True)
        self.cached_gps_data = data
        return data


    @property
    def pitch(self):
        """ Get vehicle pitch """
        return float(self.get_attitude_massage().pitch)

    @property
    def yaw(self):
        """ Get vehicle yaw """
        return float(self.get_attitude_massage().yaw)

    @property
    def roll(self):
        """ Get vehicle roll """
        return float(self.get_attitude_massage().roll)

    @property
    def latitude(self):
        """ Get vehicle latitude """
        return float(self.get_GPS_data_massage().lat)

    @property
    def longitude(self):
        """ Get vehicle longitude """
        return float(self.get_GPS_data_massage().lon)

    @property
    def altitude(self):
        """ Get vehicle altitude """
        return float(self.get_GPS_data_massage().alt)

    def start(self):
        """ thread starting funciton """
        self.thread.start()

    def main(self):
        """ Continuously updates values from autopilot """
        while True:
            if CONFIG["local"]:
                self.pipeline.autopilot_update(
                    roll=self.roll, yaw=self.yaw,
                    pitch=self.pitch, height=self.altitude,
                    lon=self.longitude, lat=self.latitude)
            else:
                # default values if not connected to a autopilot
                self.pipeline.autopilot_update(
                    roll=0, yaw=0,
                    pitch=0, height=0,
                    lon=0, lat=0)
            #time.sleep(CONFIG["autopilot_update_frequency"])
