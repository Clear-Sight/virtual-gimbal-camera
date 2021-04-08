"""
Test for autopilot.py
"""
from autopilot import get_roll
from autopilot import get_pitch
from autopilot import get_yaw
from autopilot import get_lat
from autopilot import get_lon
from autopilot import get_alt
from autopilot import connecting_with_autopilot

def is_yaw_pitch_roll_float(vehicle):
    """Float control for the roll,pitch and yaw"""
    roll  = get_roll(vehicle)
    pitch = get_pitch(vehicle)
    yaw   = get_yaw(vehicle)
    return isinstance(roll, float) and isinstance(pitch, float) and isinstance(yaw, float)

def is_gps_float(vehicle):
    """Float control for GPS data"""
    lat  = get_lat(vehicle)
    lon = get_lon(vehicle)
    alt   = get_alt(vehicle)
    return isinstance(lat, float) and isinstance(lon, float) and isinstance(alt, float)


def autopilot_adapter_test():
    """test all test functions"""
    vehicle = connecting_with_autopilot()
    assert is_yaw_pitch_roll_float and is_gps_float(vehicle)





    
