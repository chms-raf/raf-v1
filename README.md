# Development and Evaluation of a Prototype Robotic Assistance Platform for Self-Feeding

The ability to prepare a meal and feed oneself is one of the highest priority tasks for people with reduced arm and hand function. In this work, we present a prototype robot-assisted feeding system for people who have difficulty feeding themselves. 

## Overview

Check out a demo video [here](https://youtu.be/AmBzfEcXVCc)!

<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/System%20Overview.png" width=50%>
<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/Evaluation.png" width=50%>
<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/Baxter%20Arm.png" width=50%>
<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/GUI.png" width=50%>
<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/Object%20Detection.png" width=40%>

Below are the files associated with this project iteration.

### Launch File:
```bash
raf_study.launch
    - camera_multiple.launch
    - tag_detection.py
    - arm_camera_network.py
    - dlt.py
```

```bash
raf.launch 
```
Top-level launch file for the project.

```bash
camera_multiple.launch     
```
Launches both the LIDAR and STEREO depth cameras. Requires serial numbers.

```bash
tag_detection.py         
```
Detects the AprilTag Fiducial markers and draws the tag coordinate frame.

```bash
arm_camera_network_run.py   
```
Detects food items on the plate. 

```bash
dlt.py    
```
Defines the plane of the table and publishes DLT parameters.

### Scripts:
```bash
calibrate_camera.py     
```
Runs the logic for performing the calibration which defines the camera in robot coordinates.

```bash
raf.py            
```
Main project script file. Handles all experiment logic and robot motion.

```bash
realtime_ros.py  
```
Currently not in the project workspace. Located in face-alignment. This code detects the person's face.

### Other Files:
```bash
raf_grasp_demo.py  
```
Demonstrates picking up food items anywhere on the plate.

```bash
raf_setPos_demo.py  
```
Demonstrates picking up a food item in a set position and orientation.

```bash
raf_visualization.py  
```
Test code that draws GUI info for food item detection. This got integrated into raf.py now.

```bash
raf_visualize_grasp.py   
```
Nice visualization for the position and orientation of food item.
