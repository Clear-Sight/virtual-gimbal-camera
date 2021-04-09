"""
Test for autopilot_adapter.py
"""
from . import config
from vgc import autopilot_adapter

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


def test_autopilot_adapter():
    """test all test functions localy"""
    if config.CONFIG['local']:
        vehicle_1 = Vehicle(mavutil.mavlink_connection("/dev/ttyAMA0", 57600))
        assert is_yaw_pitch_roll_float(vehicle) and is_gps_float(vehicle)





    
