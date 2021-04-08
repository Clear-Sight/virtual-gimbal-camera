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


def test_main():
    """
    This function is to be called to execute all the tests to ViewController.py
    """

    #Test getting the right target coordiante even if we move
    #print(get_target_coordinate(15, 15))
    #assert np.allclose(get_target_coordinate(15, 15), (15, 15), 0.00000001, 0.00000001)
    
    

    testroll = 34
    print(get_camera_angle_when_roll(testroll))
    assert np.allclose(get_camera_angle_when_roll(testroll), (90 + testroll, 90), 0.00000001, 0.00000001)
    # test_lock_on()

    #assert main(504504, 6464, 646, 6464) == (theta_final, phi final)
   # main(0, 0, 0, 10, 15, 15, 0, 45, False)
   # assert main(0, 0, 0, 10, 15, 15, 0, 0, True) == ()
    # more tests....

def get_camera_angle_when_roll(roll):
    vc.update_fixhawk_input(roll, 0, 0, 0, 0, 0)
    vc.update_server_input(90, 90, False)
    vc.main()
    return (vc.theta_final, vc.phi_final)

def get_target_coordinate(long, lat):
    vc.update_fixhawk_input(0, 0, 0, 100, long, lat)
    vc.update_server_input(0, 180, False)
    vc.main()
    vc.update_server_input(25, 25, True)
    vc.main()
    return(vc.aim_coordinate[0], vc.aim_coordinate[1]) 

def plot(p_long, p_lat, roll, yaw, pitch, theta, phi, lock_on, height, redraw = False):
    d_long = 15
    d_lat = 15
    if(lock_on):
        vc.update_server_input(theta, phi, False)
        vc.main()
    vc.update_fixhawk_input(roll, yaw, pitch, height, d_long, d_lat)
    vc.update_server_input(theta, phi, lock_on)
    vc.main()

    #Target coordinate as a point
    if(lock_on):
        coord_diff = (vc.aim_coordinate[0] - d_long, vc.aim_coordinate[1] - d_lat)
    else:
        coord_diff = (p_long - d_long, p_lat - d_lat)

    x_diff = np.tan(np.deg2rad(coord_diff[1])) * vc.earth_radius_at_lat(d_lat)
    y_diff = np.tan(np.deg2rad(coord_diff[0])) * vc.earth_radius_at_lat(d_lat)

    p_3dcoordinate = np.matrix([[x_diff], [y_diff], [-height]])

    rot_matrix = vc.rotation_matrix(roll, yaw, pitch)
    rot_matrix_inv = rot_matrix.transpose()

    # Figur
    fig = plt.figure()
    ax = fig.gca(projection='3d', xlim=(-1*SIZE,SIZE), ylim=(-1*SIZE,SIZE), zlim=(-SIZE,SIZE), autoscale_on = False, aspect = 'auto')
    ax.set_ylabel('Drönarens riktning (y)')
    ax.set_xlabel('Drönarens sidor (x)')

    ### Sfär
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
    x = (VIEW_SIZE)*np.cos(u)*np.sin(v)
    y = (VIEW_SIZE)*np.sin(u)*np.sin(v)
    z = (VIEW_SIZE)*np.cos(v)
    ax.plot_wireframe(x, y, z, color="r", alpha = 0.2)
    

    # Marken
    #rect = Rectangle((-SIZE,SIZE), SIZE*2, SIZE*2, -90, alpha=0.4)
    #ax.add_patch(rect)
    #art3d.pathpatch_2d_to_3d(rect, z=-height, zdir="z")

    point = np.array([[0], [0], [-height]])
    point = rot_matrix_inv.dot(point)
    normal = np.array([[0], [0], [1]])
    normal = rot_matrix_inv.dot(normal)
    p = np.array([point.item(0), point.item(1), point.item(2)])
    n = np.array([normal.item(0), normal.item(1), normal.item(2)])
    d = -p.dot(n)
    xx, yy = np.meshgrid(range(-SIZE,SIZE+100,100), range(-SIZE,SIZE+100,100), sparse = True)
    z = (-n[0] * xx - n[1] * yy - d) * 1. /n[2]
    ax.plot_surface(xx, yy, z, alpha = 0.5)


    # plotta sökt koordinat
    p_3dcoordinate = rot_matrix_inv.dot(p_3dcoordinate)
    ax.scatter(p_3dcoordinate.item(0), p_3dcoordinate.item(1), p_3dcoordinate.item(2), marker = '^')

    # plotta drönarens riktning
    drone_dir = vc.angular_to_spherical(90, 0)

    ax.scatter(VIEW_SIZE*drone_dir.item(0), VIEW_SIZE*drone_dir.item(1), drone_dir.item(2)*VIEW_SIZE, marker = '^')
    ax.scatter(0, 0, 0, marker = 'o')

    #Norr
    north = rot_matrix_inv.dot(drone_dir)
    ax.scatter(VIEW_SIZE * north.item(0), VIEW_SIZE * north.item(1), VIEW_SIZE * north.item(2), marker='o')

    ### Kamerans sikte
    theta_final, phi_final = vc.theta_final, vc.phi_final
    print(theta_final, phi_final)
    
    cam_dir_adjusted = vc.angular_to_spherical(theta_final, phi_final)
    ax.scatter(VIEW_SIZE*cam_dir_adjusted.item(0), VIEW_SIZE*cam_dir_adjusted.item(1), VIEW_SIZE*cam_dir_adjusted.item(2), marker = 'x')
    if(not redraw):
        plt.show()
    else:
        plt.draw()
    

def test_cos(n):
    print("Calculating cos(3) ", n, " times...")
    timethen = datetime.now()
    for t in range(n):
        x = np.cos(3)
    print("Time taken: ", datetime.now() - timethen, "cos(3) = ", x)

def test_cos_approx(n):
    print("Approximating cos(3) ", n, " times...")
    timethen = datetime.now()
    for t in range(n):
        x = (-1 + (1/2 * (3 - np.pi)**2))
    print("Time taken: ", datetime.now() - timethen, "cos(3) = ", x)

#test_main(30, 50, 15)
if __name__ == "__main__":
    print("Hej")

def test_loop(times):
    for t in range(10):
        timethen = datetime.now()
        for i in range(times):
            theta = (i * 3)%90
            phi = i + 3
            theta_new, phi_new = vc.adjust_aim(theta, phi)
        
        timenow = datetime.now()
        print("Time taken: ", timenow - timethen , "New theta and phi is: ", theta_new, phi_new)
        