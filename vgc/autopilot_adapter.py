"""
Software interface for the autopilot
"""

import time
from pymavlink import mavutil

class Vehicle:
    """ Class Vehicle represents the autopilot as vehicle. """  

    def __init__(self):
        """ Initiates connection """
        self.connection = mavutil.mavlink_connection("/dev/ttyAMA0", 57600)

    def get_attitude_massage(self):
        """ Refreshes vehicle values """
        lis = None
        while lis is None:
            time.sleep(0.1)
            lis = self.connection.recv_match(type ="ATTITUDE")
        return lis
    
    def get_GPS_data_massage(self):
        """ Refreshes GPS data values """
        lis = None
        while lis is None:
            time.sleep(0.1)
            lis = self.connection.recv_match(type ="GPS_RAW_INT")
        return lis

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
