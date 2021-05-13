# colab-ros-camera-node

## Overview
This repository contains two nodes that publishes images and camera calibration. ROS package `usb_cam` is only used for calibration.


However, camera calibration MUST be first performed to get the camera calibration yaml file.

## Calibration
### Packages
- [usb_cam](http://wiki.ros.org/usb_cam)

Install the packages and git clone under `catkin_ws/src` then run `catkin_make`.

Also, install the usb-cam package that'll install the package to `/opt/ros/noetic/lib` directory.
```
sudo apt-get install ros-noetic-usb-cam
```

### Procedure

- Type `ls /dev/video*` and look for the correct webcam device (e.g. /dev/video1).

    - To use an external cam, locate the usb_cam-test.launch file in folder `cd ~/catkin-ws/src/usb_cam/launch`. Change `<param name="video_device" value="/dev/video0" />` to `<param name="video_device" value="/dev/video1" />` From `cd ~/catkin-ws/src/usb_cam/launch`. Modify the video* accordingly.
    - <strike>Also, change the `/dev/video*` on line 92 of the `usb_cam_node.cpp`.</strike>
-  <strike> Build the catkin_ws by typing `catkin_make`. </strike>

- Run `roslaunch usb_cam-test.launch`.

<p align="center">
    <image width="500"src="./img/duck.png">
</p>

- On a separate terminal run `rviz`.
    - Click `Add` located on the bottom left of the window and add `Image`.

<p align="center">
    <image width="500"src="./img/rviz.png">
</p>

- Once the `Image` has been added on the left panel, change the `Image Topic` to `/usb_cam/image_raw`. This will display the image on rviz as well.


<p align="center">
    <image width="500"src="./img/rviz_duck.png">
</p>

### Rqt Graph
The usb-cam launch file runs `/usb-cam` and `/image_view` nodes with `/usb_cam/Image_raw` topic.
<p align="center">
    <image width="500"src="./img/rqt_graph.png">
</p>

### Calibration
Once the launch file is ran, run the following commands. If your checkboard has 8 rows and 6 columns, make sure to put 7x5. 
On first terminal, run

```
roslaunch usb_cam usb_cam-test.launch 
```
and on a different terminal, run
```
rosrun camera_calibration cameracalibrator.py --size 7x5 --square 0.031 image:=/usb_cam/image_raw camera:=/usb_cam
```

Place the checkerboard in front of the camera and move it around until the `X, Y, Size, Skew` bar turns green. Then click `calibrate`. This may take couple of minutes(3-5 minutes). Wait until the `Save` buttons become available.


<p align="center">
    <image width="500"src="./img/camera_calibration.png">
</p>

Once the calibration finishes, a display like below will be printed out.
camera_calibration.png

<p align="center">
    <image width="500"src="./img/calibration_info.png">
</p>
    
## Running launch file

Calibration data will be saved to `/tmp/calibrationdata.tar.gz`. 
Unzip the file and move the `ost.yaml` under the `config` folder. The `ost.yaml` file contains all the camera calibration data.


A launch file can be used as shown below which takes in two parameters. A camera device must be provided in the argument (/dev/video2 is set as default value) was used for this example. Also, the path for the `ost.yaml` must be provided. This value is set as default.
```
roslaunch colab-ros-camera-node camera_image_and_info.launch cam_dev:=/dev/video2 cam_info_path:=ost.yaml
```
