"""
Test for autopilot.py
"""
from vgc import autopilot

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
    vehicle = autopilot.connecting_with_autopilot()
    assert is_yaw_pitch_roll_float(vehicle) and is_gps_float(vehicle)





    
