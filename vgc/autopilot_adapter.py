"""
Software interface for the autopilot
"""
import threading
from pymavlink import mavutil
from .config import CONFIG

class Vehicle:
    """ Class Vehicle represents the autopilot as vehicle. """

    def __init__(self, pipeline):
        """ Initiates connection """
        if not CONFIG['local']:
            self.connection = mavutil.mavlink_connection("/dev/ttyS0", 97600)
        self.thread = threading.Thread(target=self.main)
        self.pipeline = pipeline
        self.cached_gps_data = [58.391675, 15.591384, 75]

    def get_attitude_massage(self):
        """ Refreshes vehicle values """
        return self.connection.recv_match(type ="ATTITUDE", blocking=True)

    def get_GPS_data_massage(self):
        """ Refreshes GPS data values """
        data = self.connection.recv_match(type ="GPS_RAW_INT")
        if not data and self.cached_gps_data:
            return self.cached_gps_data
        elif not data:
            data = self.connection.recv_match(type =
                  "GPS_RAW_INT", blocking=False)
        self.cached_gps_data = [data.lat/10000000,
                    data.lon/10000000, data.alt/1000]
        return self.cached_gps_data


    @property
    def pitch(self):
        """ Get vehicle pitch """
        return float(round(self.get_attitude_massage().pitch,3))

    @property
    def yaw(self):
        """ Get vehicle yaw """
        print(self.get_attitude_massage().yaw)
        return float(round(self.get_attitude_massage().yaw,3))

    @property
    def roll(self):
        """ Get vehicle roll """
        return float(round(self.get_attitude_massage().roll,3))

    @property
    def latitude(self):
        """ Get vehicle latitude """
        return float(self.get_GPS_data_massage()[0])

    @property
    def longitude(self):
        """ Get vehicle longitude """
        return float(self.get_GPS_data_massage()[1])

    @property
    def altitude(self):
        """ Get vehicle altitude """
        return float(self.get_GPS_data_massage()[2])

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
                print(self.altitude)
            else:
                # default values if not connected to a autopilot
                self.pipeline.autopilot_update(
                    roll=0, yaw=0,
                    pitch=0, height=0,
                    lon=0, lat=0)
            #time.sleep(CONFIG["autopilot_update_frequency"])
