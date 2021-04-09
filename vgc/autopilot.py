"""
Software interface for the autopilot
"""

def connecting_with_autopilot():
    """ Connect to the Vehicle """
    connection_string = "/dev/ttyAMA0"
    baud_t = 57600
    vehicle = mavutil.mavlink_connection(connection_string,baud_t)
    return vehicle

def get_attitude_message(vehicle):
    """ Refreshes vehicle values """
    lis = None
    while lis is None:
        time.sleep(0.1)
        lis = vehicle.recv_match(type ="ATTITUDE")
    return lis

def get_gps_data_message(vehicle):
    """ Refreshes GPS data values """
    lis = None
    while lis is None:
        time.sleep(0.1)
        lis = vehicle.recv_match(type ="GPS_RAW_INT")
    return lis

def get_pitch(vehicle):
    """ Get vehicle pitch """
    return float(get_attitude_message(vehicle).pitch)

def get_yaw(vehicle):
    """ Get vehicle yaw """
    return float(get_attitude_message(vehicle).yaw)

def get_roll(vehicle):
    """ Get vehicle roll """
    return float(get_attitude_message(vehicle).roll)

def get_lat(vehicle):
    """ Get vehicle latitude """
    return float(get_gps_data_message(vehicle).lat)

def get_lon(vehicle):
    """ Get vehicle longitude """
    return float(get_gps_data_message(vehicle).lon)

def get_alt(vehicle):
    """ Get vehicle altitude """
    return float(get_gps_data_message(vehicle).alt)
    
