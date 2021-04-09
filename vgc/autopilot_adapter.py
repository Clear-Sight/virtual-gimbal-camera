"""
Test for autopilot_adapter.py
"""
"""
Software interface for the autopilot
"""

import time
class Vehicle:
    """ Class Vehicle represents the autopilot as vehicle. """  

    def __init__(self,connection ):
        """ Initiates connection """
        self.connection = connection

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

    def get_pitch(self):
        """ Get vehicle pitch """
        pitch = self.get_attitude_massage().pitch
        return float(pitch)

    def get_yaw(self):
        """ Get vehicle yaw """
        yaw = self.get_attitude_massage().yaw
        return float(yaw)

    def get_roll(self):
        """ Get vehicle roll """
        roll = self.get_attitude_massage().roll
        return float(roll)

    def get_lat(self):
        """ Get vehicle latitude """
        return float(self.get_GPS_data_massage().lat)

    def get_lon(self):
        """ Get vehicle longitude """
        return float(self.get_GPS_data_massage().lon)

    def get_alt(self):
        """ Get vehicle altitude """
        return float(self.get_GPS_data_massage().alt)