"""
This module is used adjust the camera on the drone accordingly to
how we move in a three dimensional space. Input variables are from
the auto-pilot fixhawk that gives roll, yaw and pitch. We can also
fix the view to a certaion point given longitude and latitude coordinates.

Classes:
ViewController

Threading:
pipepline
thread

INPUT from input_adapter.py
(There is a setter to this.)
theta_in
phi_in
lock_on (true/false)

INPUT from fixHawkadapter.py
(There is a setter to this.)
d_roll
d_yaw
d_pitch
d_height
d_coordinate

OUTPUT to cameraFilter.py
(There is a getter to this)
phi_final
dist_from_center
"""
# pylint: disable=no-self-use
# There is no better place for these functions

# pylint: disable=too-many-instance-attributes
# 16 is needed for the ViewController class.

# pylint: disable=invalid-name
# ViewController is a valid fucking name, fuck off

# pylint: disable=too-many-arguments
# 7 arguments is needed for this function.

import numpy as np
import threading

class ViewController():

    """
    The purpose of this class is provide with the functionality needed
    in order to adjust the camera accordingly to how the drone moves in
    a three-dimensional space. The camera view is meant to be set to a
    fixed point.

    Functions in the class:
    update_fixhawk_input()
    update_server_input()
    coordinate_to_point()
    point_to_coordinate()
    adjust_aim()
    main()
    start()
    main_thread()
    """

    def __init__(self, pipeline):
        """
        Input controller. Communicates with the auto pilot FixHawk and
        relays data from it.

        INPUT VARIABLES FROM AUTO PILOT FIXHAWK
        Roll, pitch and yaw are defined as the rotation around each axis
        with positive angle signifying a clockwise rotation. Roll is defined
        as rotation around the y-axis, pitch around the x-axis and yaw
        around the z-axis.
        """
        #Threading parameters, need pipeline in init

        self.pipeline = pipeline
        self.thread = threading.Thread(target=self.main)

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
        self.lock_on = False
        self.init_lock_on = False

        # INTERNAL VARIABLES
        self.new_fixhawk_values = False
        self.new_server_values = False
        self.aim_coordinate = (0, 0) # Saved coordinate to center focus on
        self.phi_final = 0
        self.theta_final = 0 # Adjusted angle theta

        # OUTPUT VARIABLES
        # These variables reflect where on the image feeded from the camera
        # we wish to look. If, say, we want to look north and in a 45-degree
        # angle and the drone has yawed right by 30 degrees, our phi_final
        # would be -30 degrees and
        # dist_from_center = IMAGE_RADIUS * np.sin(theta_final).

        self.phi_final = 0
        self.dist_from_center = 0

        self.camera_yaw = 0
        self.camera_pitch = 0
        self.camera_zoom = 2


    def start(self):
        """
        Start thread
        """
        self.thread.start()


    def main_thread(self):
        """
        Main for thread, changed name due to conflict
        with other main-method.
        """
        pass

    def update_fixhawk_input(self, roll, yaw, pitch, height, lon, lat):
        """
        Updates data from the auto pilot adapter.
        SETTER
        """
        if not self.new_fixhawk_values:
            self.d_roll = roll
            self.d_pitch = pitch
            self.d_yaw = yaw
            if height >= 0:
                self.d_height = height
            self.d_coordinate = (lon, lat)
            self.new_fixhawk_values = True

    def update_server_input(self, theta = 0, phi = 0, lock_on = False, zoom_in = 2,):
        """
        Updates data from user interface
        SETTER
        """
        if not self.new_server_values:
            if not lock_on:
                if theta > 90:
                    self.theta_in = 89
                    self.phi_in = phi
                elif theta < 0:
                    self.theta_in = 0
                    self.phi_in = phi
                else:
                    self.theta_in = theta
                    self.phi_in = phi
            if(lock_on is True and self.lock_on is False):
                self.init_lock_on = True
            self.lock_on = lock_on
            if(zoom_in >= 2 and zoom_in <= 50):
                self.camera_zoom = zoom_in
            self.new_server_values = True

    def coordinate_to_point(self, coord1, coord2, height):
        """
        Calculates where to look given two coordinates where coord1 is
        the origin.

        Arguments coord1 and coord2 are tuples and height is the height
        from where we are looking, in meters. Function returns the
        point in its angular form(theta, phi). Used in lock-on mode.
        """
        coord_diff = (coord2[0] - coord1[0], coord2[1] - coord1[1])
        x_diff = np.tan(np.deg2rad(coord_diff[1])) * self.earth_radius_at_lat(coord1[1])
        y_diff = np.tan(np.deg2rad(coord_diff[0])) * self.earth_radius_at_lat(coord1[1])
        phi = np.arctan2(x_diff, y_diff)
        theta_2 = np.arctan(np.sqrt(np.power(x_diff, 2) + np.power(y_diff, 2)) / height)
        return np.rad2deg(theta_2), (np.rad2deg(phi) + 360) % 360

    def point_to_coordinate(self, theta, phi, height, d_coord):
        """
        Calculates the coordinate existent at the center of view.

        Argument theta and phi represent our aim, height is our
        height from sea level and d_coord is the drone's current
        coordinate. Thisfunction is used when lock_on mode first is
        initialized.
        """
        p_lat = np.deg2rad(d_coord[1]) +\
            np.arctan((height * np.tan(np.deg2rad(theta))*\
            np.sin(np.deg2rad(phi))) / self.earth_radius_at_lat(d_coord[1]))
        p_long = np.deg2rad(d_coord[0]) +\
            np.arctan((height * np.tan(np.deg2rad(theta))*\
            np.cos(np.deg2rad(phi))) / self.earth_radius_at_lat(d_coord[1]))
        return np.rad2deg(p_long), np.rad2deg(p_lat)

    def adjust_aim(self, theta, phi):
        """
        Adjust the camera view accordingly to how the drone operates
        in three dimensions.

        Given two angles theta and phi that desbribes how the camera
        is oriented this function will compensate for the drone
        movement in three dimensions and adjust the camera accordingly.
        The input should be the two angles seperated and the output is
        a new theta and phi in a tuple.
        """
        inverse_rotation_matrix = self.rotation_matrix(self.d_roll,
        self.d_yaw, self.d_pitch).transpose()
        aim_spherical = self.angular_to_spherical(theta, phi)
        aim_spherical_adjusted = inverse_rotation_matrix.dot(aim_spherical)
        return self.spherical_to_angular(aim_spherical_adjusted)

    def main(self):
        """
        Main-function that runs all the time and updates our view
        angle. Other components simply call the setter functions and
        then waits for the main-function to update  where we are
        looking. Then you can call the getter-function to recieve
        the updated values.
        """
        if self.new_fixhawk_values or self.new_server_values:
            self.new_fixhawk_values = True
            self.new_server_values = True
            if self.lock_on:
                if self.init_lock_on:
                    self.aim_coordinate = self.point_to_coordinate(
                        self.theta_in, self.phi_in,
                        self.d_height, self.d_coordinate)
                    self.init_lock_on = False

                (theta_temp, phi_temp) = self.coordinate_to_point(
                    self.d_coordinate, self.aim_coordinate, self.d_height)
                self.theta_final, self.phi_final = \
                self.adjust_aim(theta_temp, phi_temp)
                self.camera_pitch = np.sin(self.theta_final)
                self.camera_yaw = self.phi_final
                self.new_fixhawk_values = False
                self.new_server_values = False
            else:
                self.theta_final, self.phi_final = \
                self.adjust_aim(self.theta_in, self.phi_in)
                self.camera_pitch = np.sin(self.theta_final)
                self.camera_yaw = self.phi_final
                self.new_server_values = False
                self.new_fixhawk_values = False
            #self.pipeline.set_cropping_point(
            #    self.camera_yaw,
            #    self.camera_pitch,
            #    self.camera_zoom)

    def rotation_matrix(self, roll, yaw, pitch):
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

    def earth_radius_at_lat(self, lat):
        """
        Input current latitude and return earth's approximate radius at
        that position.
        """
        earth_radius_at_equator = 6378137
        radius_difference_pole_equator = 21385
        return earth_radius_at_equator - \
        (lat/90) * radius_difference_pole_equator

    def angular_to_spherical(self, theta, phi):
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

    def spherical_to_angular(self, coord):
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
