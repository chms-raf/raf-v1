import argparse

import cv2
import numpy as np
import re
import os
from cv_bridge import CvBridge

from detectron2 import model_zoo
from detectron2.config import get_cfg, CfgNode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultPredictor
from detectron2.structures import Instances
from detectron2.utils.visualizer import Visualizer, VisImage
from detectron2.utils.visualizer import ColorMode

from detectron2.data.datasets import register_coco_instances

br = CvBridge()

# import pickle

def _get_parsed_args() -> argparse.Namespace:
    """
    Create an argument parser and parse arguments.
    :return: parsed arguments as a Namespace object
    """

    parser = argparse.ArgumentParser(description="Detectron2 demo")

    # default model is the one with the 2nd highest mask AP
    # (Average Precision) and very high speed from Detectron2 model zoo
    parser.add_argument(
        "--base_model",
        default="COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
        help="Base model to be used for training. This is most often "
             "appropriate link to Detectron2 model zoo."
    )

    parser.add_argument(
        "--images",
        nargs="+",
        help="A list of space separated image files that will be processed. "
             "Results will be saved next to the original images with "
             "'_processed_' appended to file name."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = _get_parsed_args()

    register_coco_instances("train_set", {}, "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/train/annotations.json", "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/train")
    train_metadata = MetadataCatalog.get("train_set")
    # print(train_metadata)
    # dataset_dicts_train = DatasetCatalog.get("train_set")

    cfg: CfgNode = get_cfg()

    cfg.merge_from_file(model_zoo.get_config_file(args.base_model))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(args.base_model)
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/output_5k/model_final.pth")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 16
    cfg.DATASETS.TRAIN = ("train_set")

    train_metadata.thing_classes = ["Gripper", "Beans", "Cottage Cheese", "Yogurt", "Watermelon", "Banana", \
                                                      "Strawberry", "Celery", "Carrot", "Pretzel", "Knife", "Spoon", "Fork", \
                                                      "Cup", "Bowl", "Plate"]

    # Same but reversed order
    # train_metadata.thing_classes = ["Plate", "Bowl", "Cup", "Fork", "Spoon", "Knife", \
    #                                                   "Pretzel", "Carrot", "Celery", "Strawberry", "Banana", "Watermelon", "Yogurt", \
    #                                                   "Cottage Cheese", "Beans", "Gripper"]

    train_metadata.thing_colors = [(178, 80, 80), (140, 120, 240), (89, 134, 179), (250, 250, 55), (131, 224, 112), \
                                                     (255, 204, 51), (50, 183, 250), (102, 255, 102), (184, 61, 245), (36, 179, 83), \
                                                     (221, 255, 51), (255, 96, 55), (255, 0, 124), (52, 209, 183), (250, 50, 83), (51, 221, 255)]

    # Class List
    # 0 - Gripper
    # 1 - Beans
    # 2 - Cottage Cheese
    # 3 - Yogurt
    # 4 - Watermelon
    # 5 - Banana
    # 6 - Strawberry
    # 7 - Celery
    # 8 - Carrot
    # 9 - Pretzel
    # 10 - Knife
    # 11 - Spoon
    # 12 - Fork
    # 13 - Cup
    # 14 - Bowl
    # 15 - Plate

    # Save Metadata
    # f = open("metadata.pkl","wb")
    # pickle.dump(train_metadata, f)
    # f.close()

    # Load Metadata
    # with open('/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/output_50k/metadata.pkl', 'rb') as handle:
    #     train_metadata = pickle.load(handle)
    # handle.close

    predictor: DefaultPredictor = DefaultPredictor(cfg)

    image_file: str
    for image_file in args.images:
        img: np.ndarray = cv2.imread(image_file)

        output: Instances = predictor(img)["instances"]

        # predictions = predictor(img)["instances"]
        predictions = predictor(img)["instances"].to("cpu")
        pred_boxes = predictions.pred_boxes
        pred_masks = np.asarray(predictions.pred_masks)

        # masks = list()
        # for i in enumerate(pred_boxes):
        #     mask = np.zeros(pred_masks[i].shape, dtype="uint8")
        #     mask[pred_masks[i, :, :]]=255
        #     mask = br.cv2_to_imgmsg(mask)
        #     masks.append(mask)

        for box, mask in zip(pred_boxes, pred_masks):
            print("Type - box: ", type(box))
            print("Type - mask: ", type(mask))
            print("Box: ", box.tolist())
            # print("Mask: ", map(int, mask.tolist()))
            mask = mask.astype(np.uint8)
            print(type(mask))
            break

        v = Visualizer(img[:, :, ::-1],
                       train_metadata,
                       scale=1.0,
                       instance_mode=ColorMode.SEGMENTATION)
        result: VisImage = v.draw_instance_predictions(output.to("cpu"))
        result_image: np.ndarray = result.get_image()[:, :, ::-1]

        # get file name without extension, -1 to remove "." at the end
        out_file_name: str = re.search(r"(.*)\.", image_file).group(0)[:-1]
        out_file_name += "_processed.png"

        cv2.imshow('image', result_image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 

        # cv2.imwrite(out_file_name, result_image)