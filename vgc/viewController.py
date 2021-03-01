"""
This module is used adjust the camera on the drone accordingly to
how we move in a three dimensional space. Input variables are from 
the auto-pilot fixhawk that gives roll, yaw and pitch. We can also
fix the view to a certaion point given longitude and latitude coordinates.

Classes:
ViewController

TODO: Read about numba.

"""
import math
import numpy as np


class ViewController():
    """
    The purpose of this class is provide with the functionality needed
    in order to adjust the camera accordingly to how the drone moves in a 
    three-dimensional space. The camera view is meant to be set to a fixed point.

    Functions in the class:
    update_fixhawk_input()
    rotation_matrix()
    earth_radius_at_lat()
    angular_to_spherical()
    spherical_to_angular()
    coordinate_to_point()
    adjust_aim()
    """
    
    def __init__(self, image_radius, inputController):
        # Input controller. Communicates with the auto pilot FixHawk and
        # relays data from it.
        self.inputController = inputController
        
        # INPUT VARIABLES FROM AUTO PILOT FIXHAWK
        # Roll, pitch and yaw are defined as the rotation around each axis 
        # with positive angle signifying a clockwise rotation. Roll is defined
        # as rotation around the y-axis, pitch around the x-axis and yaw
        # around the z-axis.
        self.d_roll = 0
        self.d_pitch = 0
        self.d_yaw = 0
        self.d_height = 0 # Height in meters above sea level
        self.d_coordinate = (0, 0) # Longitude, latitude
        
        # INPUT VARIABLES FROM WEB SERVER
        # Angles theta and phi are the spherical coordinates of where to look.
        # Theta = 0 means looking straight down, phi = 0 is looking north.
        self.theta_in = 0
        self.phi_in = 0
        
        # VARIABLES FROM CONFIG FILE
        self.IMAGE_RADIUS = 1080 # Needs to be fetched from file

        # INTERNAL VARIABLES
        self.aim_coordinate = (0, 0) # Saved coordinate to center focus on
        self.theta_final = 0 # Adjusted angle theta

        # OUTPUT VARIABLES
        # These variables reflect where on the image feeded from the camera
        # we wish to look. If, say, we want to look north and in a 45-degree
        # angle and the drone has yawed right by 30 degrees, our phi_final
        # would be -30 degrees and 
        # dist_from_center = IMAGE_RADIUS * sin(theta_final).
        self.phi_final = 0 
        self.dist_from_center = 0

    def update_fixhawk_input(self):
        """
        Updates data from the auto pilot adapter.
        """
        self.d_roll = 0 # self.inputController.get_roll()
        self.d_pitch = 0 # self.inputController.get_pitch()
        self.d_yaw = 0 # self.inputController.get_yaw()
        self.d_height = 0 # self.inputController.get_height()
        self.d_coordinate = (0, 0) # self.inputController.get_coordinates()

    def rotation_matrix(self, roll, yaw, pitch):
        """
        Returns the rotation matrix given the roll(y-axis), yaw(z-axis) and
        pitch(x-axis).

        A positive roll indicates a clock-wise rotation as seen from the negative
        side of the axis. This is the case for the pitch as well. A positive yaw,
        however, indicates a clock-wise rotation as seen from the positive side of
        the axis. One could also say "as seen from above". This reflects the way
        the FixHawk roll, yaw and pitch work.
        Note that for rotation matrices the inverse and transponent are the same.
        So, if a counter-clockwise rotation is needed, the transponent can be used.
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


    def earth_radius_at_lat(self, d_lat):
        """
        Input current latitude and return earth's approximate radius at that
        position.
        """
        earth_radius_at_equator = 6378137
        radius_difference_pole_equator = 21385
        return earth_radius_at_equator - (d_lat/90) * radius_difference_pole_equator


    def angular_to_spherical(self, theta, phi):
        """
        Translates an angular coordinate to a spherical.

        The returned value is of type numpy.matrix(see documentation for further
        information).
        """
        theta_rad = np.deg2rad(theta)
        phi_rad = np.deg2rad(phi)
        return np.matrix([
                        [np.sin(theta_rad) * np.sin(phi_rad)],
                        [np.sin(theta_rad)*np.cos(phi_rad)],
                        [-np.cos(theta_rad)]
                        ])


    def spherical_to_angular(self, coord):
        """
        Translates a given spherical coordinate to an angular coordinate.
        
        Given a spherical coordinate on the form (x,y,z) this
        fucntion will return it in its angular form (theta, phi).
        The input should be a numpy.matrix and the returned value is tuple.
        """
        phi = np.arctan2(coord.item(0), coord.item(1))
        theta = np.arccos(-coord.item(2))
        return np.rad2deg(theta), np.rad2deg(phi) % 360


    def coordinate_to_point(self, coord1, coord2, z):
        """
        Calculates where to look given two coordinates where coord1 is the origin.

        Arguments coord1 and coord2 are tuples and z is the height from where we
        are looking, in meters. Function returns the point in its angular form,
        (theta, phi).
        """
        theta = np.arctan((self.earth_radius_at_lat(coord2[1])/z) *\
            np.sqrt(pow(np.tan(np.deg2rad(coord1[1] - coord2[1])), 2)\
            + pow(np.tan(np.deg2rad((coord1[0] - coord2[0])/2)), 2)))
        temp_x = np.arccos(np.deg2rad(coord1[1])) *\
            np.sin(np.deg2rad(coord1[0] - coord2[0]))
        temp_y = (np.cos(np.deg2rad(coord2[1])) * np.sin(np.deg2rad(coord1[1])))\
            - (np.sin(np.deg2rad(coord2[1])) * np.cos(np.deg2rad(coord1[1])) *\
                np.cos(np.deg2rad(coord1[0] - coord2[0])))
        phi = np.arctan2(temp_x, temp_y)
        return np.rad2deg(theta), np.rad2deg(phi) % 360  #Force phi to be positive


    def adjust_aim(self, theta, phi):
        """
        Adjust the camera view accordingly to how the drone operates in three dimensions.

        Given two angles theta and phi that desbribes how the camera is oriented 
        this function will compensate for the drone movement in three dimensions and
        adjust the camera accordingly. The input should be the two angles seperated and
        the output is a new theta and phi in a tuple.
        """
        inverse_rotation_matrix = self.rotation_matrix(d_roll, d_yaw, d_pitch).transpose()
        aim_spherical = self.angular_to_spherical(theta, phi)
        aim_spherical_adjusted = inverse_rotation_matrix.dot(aim_spherical)
        return self.spherical_to_angular(aim_spherical_adjusted)
