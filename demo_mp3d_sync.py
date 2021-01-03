#!/usr/bin/env python3
"""
This is some code I wrote to access the 3d depth image from the kinect via python.
I used the original demo_mp_sync.py file found in the kinect wrappers as a starting off point to get the depth image.
For fun I decided to display it in matplotlib.

author : Jonathan Sanabria
"""

import freenect
import matplotlib.pyplot as plt
import frame_convert
import signal

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

keep_running = True

def get_depth():
    d = freenect.sync_get_depth()[0]
    return frame_convert.pretty_depth(d)


def get_video():
    return freenect.sync_get_video()[0]

def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False



def get_pc():
    """
    @returns a pointcloud and the matchin color info based on kinect functions
    """
    depth_image_data = get_depth()
    # get point cloud data
    pc_coordinates = point_cloud(depth_image_data)
    mask = np.where(np.isfinite(pc_coordinates[:,:,2]) )
    pc_coordinates = pc_coordinates[mask]
    
    # get color 
    rgb = get_video()
    rgb = rgb[mask]/255
    alphachannel = np.ones((rgb.shape[0],1))
    rgb = np.hstack((rgb,alphachannel))

    return pc_coordinates, rgb


def reduce_pc(pc,colors, return_count=10):
    """
    @param pc : is the data you want the color to be dependent on
    @param colors : colors are the pixel-wise rbg array values
    """
    return_count = int(return_count)
    random_mask = np.random.choice( pc.shape[0] , return_count )
    pc = pc[random_mask]

    colors = colors[random_mask]
    return pc,colors

# referenced : https://codereview.stackexchange.com/questions/79032/generating-a-3d-point-cloud
# my version uses the values found in ./libfreenect/wrappers/cpp/cpp_pc_view.cpp
def point_cloud(depth):
    """Transform a depth image into a point cloud with one point for each
    pixel in the image, using the camera transform for a camera
    centred at cx, cy with field of view fx, fy.

    depth is a 2-D ndarray with shape (rows, cols) containing
    depths from 1 to 254 inclusive. The result is a 3-D array with
    shape (rows, cols, 3). Pixels with invalid depth in the input have
    NaN for the z-coordinate in the result.
    """
    rows, cols = depth.shape

    c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
    valid = (depth > 0) & (depth < 255)

    # depth to coordinate variables
    ux = (c - (640-1)/2.0)
    uy = (r - (480-1)/2.0)
    # set focal lengths
    fx = 595.0
    fy = fx

    z = np.where(valid, depth , np.nan)
    x = np.where(valid, z * ux /fx, 0)
    y = np.where(valid, z * uy /fy, 0)

    return np.dstack((x, y, z))


def matplotlib_ax_logic(ax,pc,colors):
    ax.clear()
    scat = ax.scatter(pc[:,0],pc[:,1],pc[:,2],color=colors,marker="o")
    max_val = np.max(pc)
    min_val = -max_val

    ax.set_xlim(min_val//2,max_val//2)
    ax.set_ylim(min_val//2,max_val//2)
    ax.set_zlim(int(max_val*.25),max_val)


def main():
    plt.ion()
    fig = plt.figure(111,figsize=(20.0,20.0),dpi=75)
    ax = fig.add_subplot(111, projection='3d')
    altitude = -90
    azimuth = -90
    delta = 10
    ax.view_init(altitude, azimuth)

    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)

    pc,colors = get_pc()
    REDUCTION_AMOUNT = pc.shape[0]/10
    pc,colors = reduce_pc(pc,colors,REDUCTION_AMOUNT)

    matplotlib_ax_logic(ax,pc,colors)

    while keep_running:
        pc,colors = get_pc()
        pc,colors = reduce_pc(pc,colors,REDUCTION_AMOUNT)

        matplotlib_ax_logic(ax,pc,colors)

        ###########################
        # START live rotation logic
        if (altitude < -90 and delta < 0) \
        or (altitude > -35 and delta > 0):
            delta *= -1
        altitude += delta
        azimuth += delta//2
        ax.view_init(altitude, azimuth)
        # END live rotation logic
        ###########################

        plt.draw()
        plt.waitforbuttonpress(0.01)

if __name__ == "__main__":
    main()


