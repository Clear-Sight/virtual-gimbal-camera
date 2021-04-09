"""
Test for autopilot_adapter.py
"""

def is_yaw_pitch_roll_float(self):
    """Float control for the roll,pitch and yaw"""
    roll  = self.get_roll()
    pitch = self.get_pitch()
    yaw   = self.get_yaw()
    return isinstance(roll, float) and isinstance(pitch, float) and isinstance(yaw, float)

def is_gps_float(self):
    """Float control for GPS data"""
    lat   = self.get_lat()
    lon   = self.get_lon()
    alt   = self.get_alt()
    return isinstance(lat, float) and isinstance(lon, float) and isinstance(alt, float)