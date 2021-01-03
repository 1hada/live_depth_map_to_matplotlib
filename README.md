# Matplotlib and depth map fun
A fun toy project to view RGBD data from a kinect into matplotlib
The coordinates are colored and the video is live.

![ Matplotlib demo ](depth2plt.gif)

# VERY basic description of the changes I made
### Step 1
Recognize the values you'd need for the conversions could be found in :
> ./libfreenect/wrappers/cpp/cpp_pc_view.cpp
> DrawGLScene(..)
```
        if (!color) glColor3ub(255, 255, 255);
        for (int i = 0; i < 480*640; ++i)
        {   
	    if (color)
	        glColor3ub( rgb[3*i+0],    // R
	                    rgb[3*i+1],    // G
	                    rgb[3*i+2] );  // B

	    float f = 595.f;
	    // Convert from image plane coordinates to world coordinates
	    glVertex3f( (i%640 - (640-1)/2.f) * depth[i] / f,  // X = (x - cx) * d / fx
	                (i/640 - (480-1)/2.f) * depth[i] / f,  // Y = (y - cy) * d / fy
	                depth[i] );                            // Z = d
        }

```
### Step 2
* After Step 1 We now have access to point clouds coodinates from the depth image.
* I grab a random subset of those points so that matplotlib can load them faster
* I also decided to color each coordinate and you can experiment with seeing the coordinates in one color by changing the second line in matplotlib_ax_logic(ax,pc,colors) to :
```
scat = ax.scatter(pc[:,0],pc[:,1],pc[:,2])
```
* It's more fun with colors :)

### Step 3
Plug in your kinect and run :
```
python3 demo_mp3d_sync.py 
```




# REQUIREMENTS
```
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.5 LTS
Release:	18.04
Codename:	bionic
```
I've written is so that it is very easy to follow along.

```
sudo apt install python3-pip
mkdir kinect_stuff
cd kinect_stuff/
```

### Kinect Set up
 
go to https://github.com/OpenKinect/libfreenect and follow the Fetch & build instructions.
I'm posting some basic parts here for my own convenience.
```
git clone https://github.com/OpenKinect/libfreenect
cd libfreenect
mkdir build
cd build
cmake -L .. # -L lists all the project options
sudo make install #if you want to use the python wrapper #please read the freenect README
```

### Cython Python wrapper
check out https://openkinect.org/wiki/Python_Wrapper
Which should direct you to https://github.com/amiller/libfreenect-goodies
Then just follow the install instructions there.

Most importantly is 
```
cd ../wrappers/python
python3 setup.py install # you may have to run this as sudo
```

### finishing up
I still assume you are in "libfreenect/wrappers/python"
```
cp /PATH/TO/live_depth_map_to_matplotlib/demo_mp3d_sync.py ./
python3 demo_mp3d_sync.py 
```
Enjoy.




