import viewController as viewController
from mpl_toolkits import mplot3d
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
vc = viewController.ViewController(1080)
from matplotlib.patches import Rectangle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d

SIZE = 200
VIEW_SIZE = 50

# pylint: disable=invalid-name
# This is a test file, it uses tons of short variables used only
# for visualization. Having understandable names for these is
# unnecessary.

def test_main():
    """
    This function is to be called to execute all the tests to
    ViewController.py

    Since viewController translates between different coordinate
    systems it cannot be expected to return exact expected values.
    Instead, the numpy function allclose is used to compare expected
    return values.
    """
    margin = 0.00000001 #Margin of error for functions' return values

    # Test getting the right target coordiante even if we move
    for test_coord in [(10, 13), (0, 0), (-13, -37)]:
        assert np.allclose(get_target_coordinate(test_coord),
        test_coord, margin, margin)

    # Test if theta is correct when we yaw
    for testyaw in [45, -45, 360, 1066]:
        assert np.allclose(get_camera_angle_when_yaw(testyaw)[0],
    45, margin)

    # Test if theta is right when we roll
    for testroll in [-10, 25, 40]:
        assert np.allclose(get_camera_angle_when_roll(testroll),
        (45 + testroll, 90), margin, margin)

    # Test if theta and phi is right when we pitch
    for testpitch in [-42, 69, 0.1]:
        assert np.allclose(get_camera_angle_when_pitch(testpitch),
        (np.abs(testpitch), unitstep(testpitch)), margin, margin)

    # Test if height doesn't change when entering an invalid value
    for test_height in [-10, 10, 9999, 1000]:
        assert testing_inappropriate_height(test_height)

    print("Passed all tests")

# Return 0 if x is negative, 180 if positive
unitstep = lambda x : 0 if x <= 0 else 180

def get_camera_angle_when_pitch(pitch):
    vc.update_fixhawk_input(0, 0, pitch, 0, 0, 0)
    vc.update_server_input(0, 0)
    vc.main()
    return(vc.theta_final, vc.phi_final)

def get_camera_angle_when_yaw(yaw):
    vc.update_fixhawk_input(0, yaw, 0, 0, 0, 0)
    vc.update_server_input(45, 0)
    vc.main()
    return(vc.theta_final, vc.phi_final)

def get_camera_angle_when_roll(roll):
    vc.update_fixhawk_input(roll, 0, 0, 0, 0, 0)
    vc.update_server_input(45, 90, False)
    vc.main()
    return (vc.theta_final, vc.phi_final)

def testing_inappropriate_theta(theta):
    vc.update_fixhawk_input(0, 0, 0, 0, 0, 0)
    vc.update_server_input(theta, 0, False)
    vc.main()
    return vc.theta_in < 90 and vc.theta_in >= 0

def testing_inappropriate_height(height):
    vc.update_fixhawk_input(0, 0, 0, height, 0, 0)
    vc.update_server_input(45, 90, False)
    vc.main()
    return vc.d_height >= 0 and vc.d_height < 10000

def get_target_coordinate(coord):
    vc.update_fixhawk_input(0, 0, 0, 100, coord[0], coord[1])
    vc.update_server_input(0, 180, False)
    vc.main()
    vc.update_server_input(25, 25, True)
    vc.main()
    return(vc.aim_coordinate[0], vc.aim_coordinate[1])

def plot(p_long, p_lat, roll, yaw, pitch, theta, phi, lock_on, height):
    d_long = 15
    d_lat = 15
    if lock_on:
        vc.update_server_input(theta, phi, False)
        vc.main()
    vc.update_fixhawk_input(roll, yaw, pitch, height, d_long, d_lat)
    vc.update_server_input(theta, phi, lock_on)
    vc.main()

    #Target coordinate as a point
    if lock_on:
        coord_diff = (vc.aim_coordinate[0] - d_long,
        vc.aim_coordinate[1] - d_lat)
    else:
        coord_diff = (p_long - d_long, p_lat - d_lat)

    x_diff = np.tan(np.deg2rad(coord_diff[1])) * vc.earth_radius_at_lat(d_lat)
    y_diff = np.tan(np.deg2rad(coord_diff[0])) * vc.earth_radius_at_lat(d_lat)

    p_3dcoordinate = np.matrix([[x_diff], [y_diff], [-height]])

    rot_matrix = vc.rotation_matrix(roll, yaw, pitch)
    rot_matrix_inv = rot_matrix.transpose()

    # Figur
    fig = plt.figure()
    ax = fig.gca(projection='3d', xlim=(-1 * SIZE, SIZE), ylim=(-1 * SIZE, SIZE),
    zlim=(-SIZE,SIZE), autoscale_on = False, aspect = 'auto')
    ax.set_ylabel('Drönarens riktning (y)')
    ax.set_xlabel('Drönarens sidor (x)')

    ### Sfär
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
    x = (VIEW_SIZE)*np.cos(u)*np.sin(v)
    y = (VIEW_SIZE)*np.sin(u)*np.sin(v)
    z = (VIEW_SIZE)*np.cos(v)
    ax.plot_wireframe(x, y, z, color="r", alpha = 0.2)

    # Marken
    point = np.array([[0], [0], [-height]])
    point = rot_matrix_inv.dot(point)
    normal = np.array([[0], [0], [1]])
    normal = rot_matrix_inv.dot(normal)
    p = np.array([point.item(0), point.item(1), point.item(2)])
    n = np.array([normal.item(0), normal.item(1), normal.item(2)])
    d = -p.dot(n)
    xx, yy = np.meshgrid(range(-SIZE,SIZE+100,100), range(-SIZE,SIZE+100,100),
    sparse = True)
    z = (-n[0] * xx - n[1] * yy - d) * 1. /n[2]
    ax.plot_surface(xx, yy, z, alpha = 0.5)

    # plotta sökt koordinat
    p_3dcoordinate = rot_matrix_inv.dot(p_3dcoordinate)
    ax.scatter(p_3dcoordinate.item(0), p_3dcoordinate.item(1),
    p_3dcoordinate.item(2), marker = '^')

    # plotta drönarens riktning
    drone_dir = vc.angular_to_spherical(90, 0)

    ax.scatter(VIEW_SIZE*drone_dir.item(0), VIEW_SIZE*drone_dir.item(1),
    drone_dir.item(2)*VIEW_SIZE, marker = '^')
    ax.scatter(0, 0, 0, marker = 'o')

    #Norr
    north = rot_matrix_inv.dot(drone_dir)
    ax.scatter(VIEW_SIZE * north.item(0), VIEW_SIZE * north.item(1),
    VIEW_SIZE * north.item(2), marker='o')

    ### Kamerans sikte
    theta_final, phi_final = vc.theta_final, vc.phi_final

    cam_dir_adjusted = vc.angular_to_spherical(theta_final, phi_final)
    ax.scatter(VIEW_SIZE*cam_dir_adjusted.item(0),
    VIEW_SIZE*cam_dir_adjusted.item(1), VIEW_SIZE*cam_dir_adjusted.item(2),
    marker = 'x')
    plt.show()
    