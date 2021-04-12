"""
Test for autopilot_adapter.py
"""
#from . import config

#import vgc.autopilot_adapter
from vgc import autopilot_adapter
#from ConfigParser import SafeConfigParser
#import configparser


#parser = configparser.ConfigParser()
#parser.read("config.json")

def is_yaw_pitch_roll_float(vehicle):
    """Float control for the roll,pitch and yaw"""
    roll  = vehicle.roll
    pitch = vehicle.pitch
    yaw   = vehicle.yaw
    return isinstance(roll, float) and isinstance(pitch, float) and isinstance(yaw, float)

def is_gps_float(vehicle):
    """Float control for GPS data"""
    lat = vehicle.latitude
    lon = vehicle.longitude
    alt = vehicle.altitude
    return isinstance(lat, float) and isinstance(lon, float) and isinstance(alt, float)


#def test_autopilot_adapter():
#    """test all test functions localy"""
#    if config.CONFIG['local']:
    #if parser.get("config","local"):
#        vehicle = Vehicle(mavutil.mavlink_connection("/dev/ttyAMA0", 57600))
#        assert is_yaw_pitch_roll_float(vehicle) and is_gps_float(vehicle)
