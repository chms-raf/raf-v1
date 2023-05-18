from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.modeling import build_model
from detectron2.checkpoint import DetectionCheckpointer

import pickle

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.merge_from_list(["MODEL.WEIGHTS", "/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/models/final_model/output_35k/model_0034999.pth"])
cfg.DATALOADER.NUM_WORKERS = 4
cfg.SOLVER.IMS_PER_BATCH = 8
cfg.SOLVER.BASE_LR = 0.001
cfg.SOLVER.MAX_ITER = 300 # 300 iterations seems good enough, but you can certainly train longer
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 16

# print(cfg.dump())  # print formatted configs
# with open("output.yaml", "w") as f:
#   f.write(cfg.dump())   # save config to file
# f.close()

print(cfg.MODEL.WEIGHTS)

input("Press ENTER when ready to build model...")

model = build_model(cfg)  # returns a torch.nn.Module
DetectionCheckpointer(model).load(cfg.MODEL.WEIGHTS)

# checkpointer = DetectionCheckpointer(trainer.model, save_dir=cfg.OUTPUT_DIR)
# torch.save(trainer.model.state_dict(), os.path.join(cfg.OUTPUT_DIR, "test.pth"))
# torch.save(trainer.model.state_dict(), os.path.join(cfg.OUTPUT_DIR, "test.pkl"))

# f = open("model_final.pkl","wb")
# pickle.dump(model.state_dict(), f)
# f.close()

### OPEN WEIGHTS ###
# with open('/home/labuser/ros_ws/src/odhe_ros/arm_camera_dataset2/model_final_f10217.pkl', 'rb') as handle:
#     data1 = pickle.load(handle)
# handle.close

# with open('model_state_dict.pkl', 'rb') as handle:
#     data2 = pickle.load(handle)
# handle.close

data = dict()
data['model'] = model.state_dict()
data['__author__'] = 'Jack Schultz'

f = open("model_final.pkl","wb")
pickle.dump(data, f)
f.close()

print("done.")

# ### PRINT SOME INFO ###
# print("\n --- Default model weights ---")
# print(type(data1))
# print(data1.keys())
# print(data1['__author__'])
# print(type(data1['model']))
# print(data1['model'].keys())

# # for key, value in data1.items() :
# #     print (key, value)

# print("\n --- Custom model weights ---")
# print(type(data3))
# print(data3.keys())
# print(data3['__author__'])
# print(type(data3['model']))
# print(data3['model'].keys())