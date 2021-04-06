#from mpl_toolkits import mplot3d
from math import *
#%matplotlib inline
import numpy as np
#import matplotlib.pyplot as plt
from numba import jit
from datetime import datetime

d_roll = 3
d_yaw = 50
d_pitch = 6
d_height = 100
d_coordinate = (30, 55)


def rotation_matrix(roll, yaw, pitch):
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

@jit(nopython = True)
def earth_radius_at_lat(d_lat):
    """
    Input current latitude and return earth's approximate radius at that
    position.
    """
    earth_radius_at_equator = 6378137
    radius_difference_pole_equator = 21385
    return earth_radius_at_equator - (d_lat/90) * radius_difference_pole_equator


def angular_to_spherical(theta, phi):
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


def spherical_to_angular(coord):
    """
    Translates a given spherical coordinate to an angular coordinate.
    
    Given a spherical coordinate on the form (x,y,z) this
    fucntion will return it in its angular form (theta, phi).
    The input should be a numpy.matrix and the returned value is tuple.
    """
    phi = np.arctan2(coord.item(0), coord.item(1))
    theta = np.arccos(-coord.item(2))
    return np.rad2deg(theta), np.rad2deg(phi) % 360

@jit(nopython = True)
def coordinate_to_point(coord1, coord2, z):
    """
    Calculates where to look given two coordinates where coord1 is the origin.

    Arguments coord1 and coord2 are tuples and z is the height from where we
    are looking, in meters. Function returns the point in its angular form,
    (theta, phi).
    """
    theta = np.arctan((earth_radius_at_lat(coord2[1])/z) *\
        np.sqrt(pow(np.tan(np.deg2rad(coord1[1] - coord2[1])), 2)\
        + pow(np.tan(np.deg2rad((coord1[0] - coord2[0])/2)), 2)))
    temp_x = np.arccos(np.deg2rad(coord1[1])) *\
        np.sin(np.deg2rad(coord1[0] - coord2[0]))
    temp_y = (np.cos(np.deg2rad(coord2[1])) * np.sin(np.deg2rad(coord1[1])))\
        - (np.sin(np.deg2rad(coord2[1])) * np.cos(np.deg2rad(coord1[1])) *\
            np.cos(np.deg2rad(coord1[0] - coord2[0])))
    phi = np.arctan2(temp_x, temp_y)
    return np.rad2deg(theta), np.rad2deg(phi) % 360  #Force phi to be positive


def adjust_aim(theta, phi):
    """
    Adjust the camera view accordingly to how the drone operates in three dimensions.

    Given two angles theta and phi that desbribes how the camera is oriented 
    this function will compensate for the drone movement in three dimensions and
    adjust the camera accordingly. The input should be the two angles seperated and
    the output is a new theta and phi in a tuple.
    """
    inverse_rotation_matrix = rotation_matrix(d_roll, d_yaw, d_pitch).transpose()
    aim_spherical = angular_to_spherical(theta, phi)
    aim_spherical_adjusted = inverse_rotation_matrix.dot(aim_spherical)
    return spherical_to_angular(aim_spherical_adjusted)



def main():
    # Note that the height must be greater than zero. Otherwise we divide by zero.
    #All angles should be given in degrees, not in radians. Height in meter.
    #All functions will return the angle in degrees as well. It will only internally be radians.
    #point_to_coordinate may not work on the south part of the globe and around the equator.

    #PixRacer variables ( not used a the moment )
    yaw = 0
    pitch = 0
    roll = 0

    d_lat = -0.004701
    d_long = 0.004701
    p_lat = 58.411129
    p_long = 15.616761
    theta = 0
    phi = 0
    height = 106
    
    rot_matrix = rotation_matrix(roll_matrix(roll), yaw_matrix(yaw), pitch_matrix(pitch))
    rot_matrix_inv = rot_matrix.transpose()

    #theta, phi = coordinate_to_point(p_lat,p_long,d_lat,d_long, height)
    #print(degrees(theta), degrees(phi))
    point_lat, point_long = point_to_coordinate(theta, phi, height, d_long, d_lat)
    print(point_lat, point_long)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d', xlim=(-1,1), ylim=(-1,1), zlim=(-1,1), autoscale_on = True, aspect = 'auto')
    ax.set_ylabel('Nord/syd (y)')
    ax.set_xlabel('Väst/öst (x)')

    ### Sfär
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color="r", alpha = 0.2)
    
    ### Punkten norr samt drönarens riktning
    north = angular_to_spherical(90, 0)
    ax.scatter(north.item(0), north.item(1), north.item(2), marker = 'o')
    
    drone_dir = rot_matrix.dot(north)
    ax.scatter(drone_dir.item(0), drone_dir.item(1), drone_dir.item(2), marker = 'o')
    
    ### Kamerans sikte
    cam_dir_def = angular_to_spherical(theta, phi)
    ax.scatter(cam_dir_def.item(0), cam_dir_def.item(1), cam_dir_def.item(2), marker = '^')
    
    
    cam_dir_manipulated = rot_matrix.dot(cam_dir_def)
    ax.scatter(cam_dir_manipulated.item(0), cam_dir_manipulated.item(1), cam_dir_manipulated.item(2), marker = '^')
    
    cam_dir_adjusted = rot_matrix_inv.dot(cam_dir_manipulated)
    ax.scatter(cam_dir_adjusted.item(0), cam_dir_adjusted.item(1), cam_dir_adjusted.item(2), marker = 'x')
    
    
    ### Punkt 1 roterad
    """
    point_pitch = pitch_matrix(pitch).dot(point)
    point_yaw_pitch = yaw_matrix(yaw).dot(point_pitch)
    point_final = roll_matrix(roll).dot(point_yaw_pitch)
    ax.scatter(point_final.item(0), point_final.item(1), point_final.item(2), marker = '^')
    ax.scatter(point_yaw_pitch.item(0), point_yaw_pitch.item(1), point_yaw_pitch.item(2), marker = 'o')
    """
    
    plt.show()
    
def test_main(r, y, p):
    roll = r
    yaw = y
    pitch = p
    timethen = datetime.now()
    print(rotation_matrix(roll, yaw, pitch))
    timenow = datetime.now()
    print("Time taken: ", timenow - timethen)

#test_main(30, 50, 15)
if __name__ == "__main__":
    print("Hej")

def test_loop(times):
    for t in range(10):
        timethen = datetime.now()
        for i in range(times):
            theta = (i * 3)%90
            phi = i + 3
            theta_new, phi_new = adjust_aim(theta, phi)
        
        timenow = datetime.now()
        print("Time taken: ", timenow - timethen , "New theta and phi is: ", theta_new, phi_new)
        