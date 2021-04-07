from Autopilot_as_class import *

a = vehicle(mavutil.mavlink_connection("/dev/ttyAMA0",57600))
b = vehicle(mavutil.mavlink_connection("/dev/ttyAMA0",57600))
print(a.get_pitch())
print(b.get_pitch())
print(a.get_lat())