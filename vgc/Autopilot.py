from pymavlink import mavutil
import time
import sys
import argparse
import math

def connecting_with_autopilot():
    """ Connect to the Vehicle """
    print ("Connecting...")
    connection_string = "/dev/ttyAMA0"
    baud_t = 57600
    """vehicle = connect(connection_string,
                 wait_ready=False ,
                baud = baud_t)"""
    vehicle = mavutil.mavlink_connection(connection_string,baud_t)   
    return vehicle

def get_attitude_massage(a):
    lis = None
    while lis == None:
        time.sleep(0.1)
        lis = a.recv_match(type ="ATTITUDE")
    return lis

        
            
""" Getters """    
def get_pitch(massage_atttitude):
    pitch = massage_atttitude.pitch
    return float(pitch)
def get_yaw(massage_atttitude):
    yaw = massage_atttitude.yaw
    return float(yaw)
def get_roll(massage_atttitude):
    roll = massage_atttitude.roll
    return float(roll)
def get_lat(self):
    return self.location.lat
def get_lon(v):
    return self.location.lon
def get_alt(v):
    return self.location.alt
    
