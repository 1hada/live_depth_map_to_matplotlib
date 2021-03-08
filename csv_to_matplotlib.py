"""
a file to view point clouds which are saved in csv format

author : jonathan sanabria

"""
import numpy as np 
import matplotlib.pyplot as plt
USE_COLORS = True # ideally not necessary for segmentation but I saved the pc's with colors to make it easier to understand the plot
FILE_NAME = 'point_cloud_5.csv'


def reduce_pc(pc,colors=None, return_count=10000):
    """
    get a random sample of the coordinates so that it's faster to display them on matplotlib
    
    @param pc : is the data you want the color to be dependent on
    @param colors : colors are the pixel-wise rbg array values
    """
    # remove where the points are not (0,0,0) 
    # because the way we gathered the point clouds maps coordinates 
    # that are too deep or too shallow to (0,0,0)
    non_zero_indices = np.where(0!=np.linalg.norm(pc-np.array([[0,0,0]]),axis=1))
    pc = pc[non_zero_indices]

    # get back to reduction logic
    return_count = int(return_count)
    random_mask = np.random.choice( pc.shape[0] , return_count )
    pc = pc[random_mask]
    if not type(colors) == type(None):
        colors = colors[non_zero_indices]
        colors = colors[random_mask]
        return pc,colors
    return pc
    
def main():
    fig = plt.figure(111,figsize=(20.0,20.0),dpi=75)
    ax = fig.add_subplot(111, projection='3d')
    
    # rotating b.c. the pointcloud is in camera frame which is dif than the objects world frame
    # https://www.stereolabs.com/docs/positional-tracking/coordinate-frames/
    altitude = -90
    azimuth = -90
    ax.view_init(altitude, azimuth)
    
    if USE_COLORS :
        data = np.genfromtxt(FILE_NAME, delimiter=',')
        #print(data.shape)
        pc,colors = data[:,:3], data[:,3:]

        assert(type(pc) == np.ndarray) # just asserting it's a numpy array
        assert(pc.shape[1] == 3 )      # nx3 array of coordinates
        assert(colors.shape[1] == 4)   # nx4 array of RGBA colors

        # normalize rgb value between (0,1) for matplotlib
        colors[:,:3] /= 255 
        #print(colors)
        
        pc,colors = reduce_pc(pc,colors)
        scat = ax.scatter(pc[:,0],pc[:,1],pc[:,2],color=colors,marker="o")
    else :
        pc = np.genfromtxt(FILE_NAME, delimiter=',')
        #print(pc.shape)
        
        pc = reduce_pc(pc)
        scat = ax.scatter(pc[:,0],pc[:,1],pc[:,2])

    # define plot axis limits as cube
    max_val = np.max(pc)
    min_val = -max_val
    ax.set_xlim(min_val//2,max_val//2)
    ax.set_ylim(min_val//2,max_val//2)
    ax.set_zlim(min_val//2,max_val//2)
    
    plt.show()
    
    
    
if __name__ == "__main__":
    main()
