"""
This module is used to test the functionality in
viewController.py. The main function is test_main()
which executes all the different testfunctions.
"""
# pylint: disable=invalid-name
# This is a test file, it uses tons of short variables used only
# for visualization. Having understandable names for these is
# unnecessary.

# pylint: disable=import-error
# Works when executed. Dynamic compiler is stuffed.

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# Rather too many local variables than using magic numbers.
# Also, 9 arguments for function "plot" is necessary.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors
from vgc.view_controller_fast import ViewController
from vgc.pipeline import Pipeline
import threading

vc = Pipeline().view_controller

SIZE = 200
VIEW_SIZE = 50

def is_close(x, y, margin):
    if type(x) is tuple:
        return abs(x[0] - y[0]) <= margin and abs(x[1] - y[1]) <= margin
    return abs(x - y) <= margin

def test_main():
    """
    This function is to be called to execute all the tests to
    ViewController.py

    Since viewController translates between different coordinate
    systems it cannot be expected to return exact expected values.
    Instead, the numpy function allclose is used to compare expected
    return values.
    """
    margin = 0.5 #Margin of error for functions' return values

    # Test getting the right target coordiante even if we move
    for test_coord in [(10, 13), (0, 0), (-13, -37)]:
        assert is_close(get_target_coordinate(test_coord),
        test_coord, margin)

    # Test if theta is correct when we yaw
    for testyaw in [45, -45, 360, 1066]:
        assert is_close(get_camera_angle_when_yaw(testyaw)[0],
    45, margin)

    # Test if theta is right when we roll
    for testroll in [-10, 25, 40]:
        assert is_close(get_camera_angle_when_roll(testroll),
        (45 + testroll, 90), margin)

    # Test if theta and phi is right when we pitch
    for testpitch in [-42, 69, 0.1]:
        assert is_close(get_camera_angle_when_pitch(testpitch),
        (np.abs(testpitch), unitstep(testpitch)), margin)

    # Test if height doesn't change when entering an invalid value
    for test_height in [-10, 10, 9999, 1000]:
        assert get_inappropriate_height(test_height)

    #Test so that theta can not be set to an invalid value.
    for test_theta in [20, 30, -10, 110]:
        assert get_inappropriate_theta(test_theta)

    print("Passed all tests")

# Return 0 if x is negative, 180 if positive
unitstep = lambda x : 0 if x <= 0 else 180

def get_camera_angle_when_pitch(pitch):
    """
    This function tests if the camera angle
    behaves accordingly if the drone pitches.
    """
    pitch = np.deg2rad(pitch)
    vc.update_autopilot_input(0, 0, pitch, 0, 0, 0)
    vc.update_server_input(0, 0)
    vc.main()
    return(vc.theta_final, vc.phi_final)

def get_camera_angle_when_yaw(yaw):
    """
    This function tests if the camera angle
    behaves accordingly if the drone yaws.
    """
    yaw = np.deg2rad(yaw)
    vc.update_autopilot_input(0, yaw, 0, 0, 0, 0)
    vc.update_server_input(45, 0)
    vc.main()
    return(vc.theta_final, vc.phi_final)

def get_camera_angle_when_roll(roll):
    """
    This function tests if the camera angle
    behaves accordingly if the drone rolls.
    """
    roll = np.deg2rad(roll)
    vc.update_autopilot_input(roll, 0, 0, 0, 0, 0)
    vc.update_server_input(45, 90, False)
    vc.main()
    return (vc.theta_final, vc.phi_final)

def get_inappropriate_theta(theta):
    """
    This function tests that different
    thetas and checks if they are set correctly.
    """
    vc.update_autopilot_input(0, 0, 0, 0, 0, 0)
    vc.update_server_input(theta, 0, False)
    vc.main()
    return vc.theta_in < 90 and vc.theta_in >= 0

def get_inappropriate_height(height):
    """
    This function tests different heights
    and checks if they are set correctly.
    """
    vc.update_autopilot_input(0, 0, 0, height, 0, 0)
    vc.update_server_input(45, 90, False)
    vc.main()
    return vc.d_height >= 0 and vc.d_height < 10000

def get_target_coordinate(coord):
    """
    This function inputs a coordinat, locks on it, and then
    tries to move to another point. This should not be possible
    since we looked on a specific coordinat.
    """
    vc.update_autopilot_input(0, 0, 0, 100, coord[0], coord[1])
    vc.update_server_input(0, 180, False)
    vc.main()
    vc.update_server_input(25, 25, True)
    vc.main()
    return(vc.aim_coordinate[0], vc.aim_coordinate[1])

def plot(p_long, p_lat, roll, yaw, pitch, theta, phi, lock_on, height):
    """
    This function plots the drone and its field of view. Red dot is
    north, orange triangle is direction of drone, the X is where the
    camera is aiming and blue triangle is the coordinate it focuses on,
    if lock_on is true.
    """
    d_long = 15
    d_lat = 15
    if lock_on:
        vc.update_server_input(theta, phi, False)
        vc.main()
    vc.update_autopilot_input(roll, yaw, pitch, height, d_long, d_lat)
    vc.update_server_input(theta, phi, lock_on)
    vc.main()
    print(vc.d_roll, vc.d_yaw, vc.d_pitch)

    #Target coordinate as a point
    if lock_on:
        coord_diff = (vc.aim_coordinate[0] - d_long,
        vc.aim_coordinate[1] - d_lat)
    else:
        coord_diff = (p_long - d_long, p_lat - d_lat)

    x_diff = np.tan(np.deg2rad(coord_diff[1])) * vc.earth_radius_at_lat(d_lat)
    y_diff = np.tan(np.deg2rad(coord_diff[0])) * vc.earth_radius_at_lat(d_lat)

    p_3dcoordinate = np.matrix([[x_diff], [y_diff], [-height]])

    rot_matrix = vc.rotation_matrix(vc.d_roll, vc.d_yaw, vc.d_pitch)
    rot_matrix_inv = rot_matrix.transpose()

    # Figure
    fig = plt.figure()
    ax = fig.gca(projection='3d', xlim=(-1 * SIZE, SIZE), ylim=(-1 * SIZE, SIZE),
    zlim=(-SIZE,SIZE), autoscale_on = False, aspect = 'auto')
    #ax.set_ylabel('Drönarens riktning (y)')
    #ax.set_xlabel('Drönarens riktning (x)')

    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Plot ground
    point = np.array([[0], [0], [-height]])
    point = rot_matrix_inv.dot(point)
    normal = np.array([[0], [0], [1]])
    normal = rot_matrix_inv.dot(normal)
    p = np.array([point.item(0), point.item(1), point.item(2)])
    n = np.array([normal.item(0), normal.item(1), normal.item(2)])
    d = -p.dot(n)
    xx, yy = np.meshgrid(range(-SIZE*2,SIZE*2+15,15), range(-SIZE*2,SIZE*2+15,15),
    sparse = True)
    colors_list = np.empty([len(xx[0]), len(yy)], dtype=list)
    rownum = 0
    colnum = 0
    for row in yy:
        for col in xx[0]:
            alpha = 1/(1*(1+np.power(np.e, (-np.sqrt(row[0]**2 + col**2) - 100)/90)))
            colors_list[rownum, colnum] = [0.1, 0.3, 0.9, 1 - alpha]
            colnum += 1
        rownum += 1
        colnum = 0

    z = (-n[0] * xx - n[1] * yy - d) * 1. /n[2]
    ax.plot_surface(xx, yy, z, facecolors=colors_list)

    # Plot camera sphere
    u, v = np.mgrid[0:2*np.pi:20j, -np.pi/2:np.pi/2:20j]
    x = (VIEW_SIZE)*np.cos(u)*np.sin(v)
    y = (VIEW_SIZE)*np.sin(u)*np.sin(v)
    z = -(VIEW_SIZE)*np.cos(v)
    ax.plot_wireframe(x, y, z, color=[0.2, 0.4, 0.2, 0.2])

    # Plot drone
    xd = [-10,10,0]
    yd = [-10,-10,20]
    zd = [0,0,0]
    verts1 = [list(zip(xd,yd,zd))]
    coll1 = Poly3DCollection(verts1)
    coll1.set_color(colors.rgb2hex([1, 0.5, 0.2]))
    coll1.set_edgecolor('k')
    xd2 = [0,0,0]
    yd2 = [-10,-10,20]
    zd2 = [0,-5,0]
    verts2 = [list(zip(xd2,yd2,zd2))]
    coll2 = Poly3DCollection(verts2)
    coll2.set_color(colors.rgb2hex([0.2, 1, 0.5]))
    coll2.set_edgecolor('k')
    ax.add_collection3d(coll2)
    ax.add_collection3d(coll1)

    # Plot target coordinate
    p_3dcoordinate = rot_matrix_inv.dot(p_3dcoordinate)
    ax.scatter(p_3dcoordinate.item(0), p_3dcoordinate.item(1),
    p_3dcoordinate.item(2), marker = '^')

    # Plot drone direction
    drone_dir_y = vc.angular_to_spherical(90, 0)
    #drone_dir_y = rot_matrix.dot(drone_dir_y)
    ax.scatter(VIEW_SIZE*drone_dir_y.item(0), VIEW_SIZE*drone_dir_y.item(1),
    drone_dir_y.item(2)*VIEW_SIZE, marker = '^')
    ax.scatter(0, 0, 0, marker = 'o')

    # Plot North
    north = vc.angular_to_spherical(90, 0)
    north = rot_matrix_inv.dot(north)
    ax.scatter(VIEW_SIZE * north.item(0), VIEW_SIZE * north.item(1),
    VIEW_SIZE * north.item(2), marker='o')
    
    # Plot final camera angle
    theta_final, phi_final = vc.theta_final, vc.phi_final
    cam_dir_final = vc.angular_to_spherical(theta_final, phi_final)
    #cam_dir_final = rot_matrix.dot(cam_dir)
    ax.scatter(VIEW_SIZE*cam_dir_final.item(0),
    VIEW_SIZE*cam_dir_final.item(1), VIEW_SIZE*cam_dir_final.item(2),
    marker = 'x')

    # Plot connection between drone and camera aim
    if not lock_on:
        ax.plot([VIEW_SIZE*cam_dir_final.item(0), 0],
                [VIEW_SIZE*cam_dir_final.item(1), 0],
                [VIEW_SIZE*cam_dir_final.item(2), 0], c='r')
    else:
        ax.plot([p_3dcoordinate.item(0), 0],
                [p_3dcoordinate.item(1), 0],
                [p_3dcoordinate.item(2), 0], c='r')
    plt.show()