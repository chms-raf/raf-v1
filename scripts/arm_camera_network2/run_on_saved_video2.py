#!/usr/bin/env python3
# -- coding: utf-8 --

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
# import some common libraries
import numpy as np
import tqdm
import cv2
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.data import MetadataCatalog
import time

from detectron2.data.datasets import register_coco_instances

# Extract video properties
video = cv2.VideoCapture('/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/raw_videos/test_videos/test_2c.avi')
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames_per_second = video.get(cv2.CAP_PROP_FPS)
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Initialize video writer
video_writer = cv2.VideoWriter('out.mp4', fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=float(frames_per_second), frameSize=(width, height), isColor=True)

# Register the training set
register_coco_instances("train_set", {}, "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/train/annotations.json", "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/train")
train_metadata = MetadataCatalog.get("train_set")

# train_metadata.thing_classes = ["Gripper", "Beans", "Cottage Cheese", "Yogurt", "Watermelon", "Banana", \
#                                                       "Strawberry", "Celery", "Carrot", "Pretzel", "Knife", "Spoon", "Fork", \
#                                                       "Cup", "Bowl", "Plate"]

train_metadata.thing_classes = ["Plate", "Bowl", "Cup", "Fork", "Spoon", "Knife", \
                                                      "Pretzel", "Carrot", "Celery", "Strawberry", "Banana", "Watermelon", "Yogurt", \
                                                      "Cottage Cheese", "Beans", "Gripper"]

train_metadata.thing_colors = [(178, 80, 80), (140, 120, 240), (89, 134, 179), (250, 250, 55), (131, 224, 112), \
                                                    (255, 204, 51), (50, 183, 250), (102, 255, 102), (184, 61, 245), (36, 179, 83), \
                                                    (221, 255, 51), (255, 96, 55), (255, 0, 124), (52, 209, 183), (250, 50, 83), (51, 221, 255)]

# Initialize predictor
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("train_set")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set threshold for this model
# cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.WEIGHTS = "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/models/final_model/output_35k/model_0034999.pth"
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 16
predictor = DefaultPredictor(cfg)

# Initialize visualizer
v = VideoVisualizer(train_metadata, ColorMode.IMAGE)

def runOnVideo(video, maxFrames):
    """ Runs the predictor on every frame in the video (unless maxFrames is given),
    and returns the frame with the predictions drawn.
    """

    readFrames = 0
    while True:
        hasFrame, frame = video.read()
        if not hasFrame:
            break

        # Get prediction results for this frame
        outputs = predictor(frame)

        # Make sure the frame is colored
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Draw a visualization of the predictions using the video visualizer
        visualization = v.draw_instance_predictions(frame, outputs["instances"].to("cpu"))

        # Convert Matplotlib RGB format to OpenCV BGR format
        visualization = cv2.cvtColor(visualization.get_image(), cv2.COLOR_RGB2BGR)

        yield visualization

        readFrames += 1
        if readFrames > maxFrames:
            break

# Create a cut-off for debugging
num_frames = 1000

# Enumerate the frames of the video
for visualization in tqdm.tqdm(runOnVideo(video, num_frames), total=num_frames):

    # Write test image
    # cv2.imwrite('POSE detectron2.png', visualization)

    # Write to video file
    video_writer.write(visualization)

# Release resources
video.release()
video_writer.release()
cv2.destroyAllWindows()