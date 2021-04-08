import numpy as np
def rotation_matrix(roll, yaw, pitch):
    """
    Returns the rotation matrix given the roll(y-axis), yaw(z-axis)
    and pitch(x-axis).

    A positive roll indicates a clock-wise rotation as seen from
    the negative side of the axis. This is the case for the pitch
    as well. A positive yaw, however, indicates a clock-wise
    rotation as seen from the positive side of the axis. One could
    also say "as seen from above". This reflects the way the
    FixHawk roll, yaw and pitch work. Note that for rotation
    matrices the inverse and transponent are the same. So, if a
    counter-clockwise rotation is needed, the transponent can be
    used.
    """
    roll_rad = np.deg2rad(roll)
    roll_matrix = np.matrix([
                            [np.cos(roll_rad), 0, np.sin(roll_rad)],
                            [0, 1, 0],
                            [-np.sin(roll_rad), 0, np.cos(roll_rad)]
                            ])
    yaw_rad = np.deg2rad(yaw)
    yaw_matrix = np.matrix([
                            [np.cos(yaw_rad), np.sin(yaw_rad), 0],
                            [-np.sin(yaw_rad), np.cos(yaw_rad), 0],
                            [0, 0, 1]])
    pitch_rad = np.deg2rad(pitch)
    pitch_matrix = np.matrix([
                            [1, 0, 0],
                            [0, np.cos(pitch_rad), -np.sin(pitch_rad)],
                            [0, np.sin(pitch_rad), np.cos(pitch_rad)]
                            ])
    return roll_matrix.dot(yaw_matrix.dot(pitch_matrix))

def earth_radius_at_lat(lat):
    """
    Input current latitude and return earth's approximate radius at
    that position.
    """
    earth_radius_at_equator = 6378137
    radius_difference_pole_equator = 21385
    return earth_radius_at_equator - \
    (lat/90) * radius_difference_pole_equator

def angular_to_spherical(theta, phi):
    """
    Translates an angular coordinate to a spherical.

    The returned value is of type numpy.matrix(see documentation
    for further information).
    """
    theta_rad = np.deg2rad(theta)
    phi_rad = np.deg2rad(phi)
    return np.matrix([
                    [np.sin(theta_rad) * np.sin(phi_rad)],
                    [np.sin(theta_rad)*np.cos(phi_rad)],
                    [-np.cos(theta_rad)]
                    ])

def spherical_to_angular(coord):
    """
    Translates a given spherical coordinate to an angular
    coordinate.

    Given a spherical coordinate on the form (x,y,z) this
    function will return it in its angular form (theta, phi).
    The input should be a numpy.matrix and the returned value is a
    tuple.
    """
    phi = np.arctan2(coord.item(0), coord.item(1))
    theta = np.arccos(-coord.item(2))
    return np.rad2deg(theta), np.rad2deg(phi) % 360