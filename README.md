# Robot-Assisted Feeding - raf-v2

This repository houses all code related to the first robot-assisted feeding prototype system using the Baxter robot.

## Head-Mounted System
The first iteration of the project used the iSCAN etl-600 wearable
eye tracker. We used a faster-RCNN object detection network to detect cups, 
bowls, plates, forks, and spoons. The network used the iSCAN's head-mounted 
camera as the input. To demo the system, we placed a cup in
the scene. The user then directs their gaze to the cup. When they are 
ready, the user issues a voice command such as "grab the cup". Baxter then 
picks up the cup that the user was looking at and delivers it to in front 
of the user's mouth. They then move their body to sip through a straw in 
the cup. 

<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/IMG_7340.png" width=40%>

<img src="https://github.com/jschultz299/odhe_ros/blob/main/images/Object%20Detection%20Example.gif" width=50%>

## Tablet Interface System
The second iteration of this project got rid of the head-mounted eye 
tracker. Also, we decided to interact with different food items on a 
plate, instead of dishes and utensils. For the interface, we used a 
tablet monitor with a Tobii Eye tracker 4 mounted on the bottom. We 
detected objects using a mask-RCNN object detection network from 
detectron2. The network used an Intel L515 LIDAR depth camera as the 
input. The plane of the table was defined using an AprilTag fiducial 
marker. We used Talon to interface with the eyetracker. Talon also 
has the ability to allow the user to issue commands. The depth camera is 
mounted to Baxter's wrist. The camera videos food items on a plate, and 
the image is sent to the tablet with food item outlines drawn. The person 
uses their eye movements to direct a cursor to a food item. After a short 
dwell time, the food item is selected. Baxter picks up the food item and 
then turns to video the user's face. We used the face-alignment ROS 
package for facial keypoint detection. When the user open's their mouth, 
Baxter approaches the user's face and releases the food item. 

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
