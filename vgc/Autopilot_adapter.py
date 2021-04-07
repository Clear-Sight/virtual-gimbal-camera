from pymavlink import mavutil
import time
import sys
import argparse
import math

class vehicle:
    def __init__(self,connection ):
        self.connection = connection
        
    def get_attitude_massage(self):
        lis = None
        while lis == None:
            time.sleep(0.1)
            lis = self.connection.recv_match(type ="ATTITUDE")
        return lis
            
        """ Getters """    
    def get_pitch(self):
            pitch = self.get_attitude_massage().pitch
            return float(pitch)
        
    def get_yaw(self):
            yaw = self.get_attitude_massage().yaw
            return float(yaw)
        
    def get_roll(self):
        roll = self.get_attitude_massage().roll
        return float(roll)
            
    def get_lat(self):
            return self.connection.location().lat
        
    def get_lon(self):
            return self.connection.location().lon
        
    def get_alt(self):
            return self.connection.location().alt
    
