# add the 'yolov5m to path to be able to import it into python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
try:
    sys.path.remove(str(parent)) # remove the current file's directory from sys.path
except ValueError: # Already removed
    pass

import torch
from yolov5m import train
from yolov5m.models.common import DetectMultiBackend
from yolov5m.utils.general import check_img_size, non_max_suppression
from yolov5m.utils.augmentations import letterbox
import numpy as np
import yaml


class modelController(object):
    def __init__(self) -> None:
        self.labelsIndex = None
        self.model = None

    def loadLabelsIndex(self, yamlFilepath) -> None:
        with open(yamlFilepath, 'r') as file:
            # Load the YAML file as a dictionary
            self.labelsIndex = yaml.safe_load(file)

    def trainModel(self, yamlFile, pretrainedWeights, imgTrainSize=(320, 320), epochs=20, batch_size=4) -> None:
        print("Started the training of object detection model")
        train.run(data=yamlFile, imgsz=imgTrainSize, weights=pretrainedWeights, epochs=epochs, batch_size=batch_size)

    def loadModel(self, weightsPath) -> None:
        DEFAULT_YAML_PATH = r"yolov5m\data\coco128.yaml" # to-do: check if this needs to be changed to the trained YAML
        self.model = DetectMultiBackend(weights=weightsPath, dnn=False, data=DEFAULT_YAML_PATH, fp16=False) # load the model
        self.pt_stride, self.pt_names, self.pt = self.model.stride, self.model.names, self.model.pt
        imgsz = check_img_size((640, 640), s=self.pt_stride)  # check image size

    def makeInference(self, img_arr, confThreshold=0.9, frameSize=(640, 640)) -> list:
        # Preprocess image for model input
        img_arr = letterbox(img_arr, frameSize, stride=self.pt_stride)[0]  # padded resize
        img_arr = img_arr.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img_arr = np.ascontiguousarray(img_arr)  # contiguous

        img_arr = torch.from_numpy(img_arr).to(self.model.device)
        img_arr = img_arr.half() if self.model.fp16 else img_arr.float()
        img_arr /= 255
        if len(img_arr.shape) == 3:
            img_arr = img_arr[None]  # expand for batch dim

        # Make inference, apply NMS
        preds = self.model(img_arr)
        preds = non_max_suppression(preds, conf_thres=confThreshold, iou_thres=0.25, max_det=500)

        # Filter and store predictions
        detections = [] # e.g. [{'name': 'cat', conf_score: 0.875, location: [0.644, 0.2, 0.15, 0.222]}, ... ]
        for pred in preds[0]:
            if len(pred) > 0 and float(pred[4]) >= confThreshold:
                xmin, ymin, xmax, ymax = pred[0], pred[1], pred[2], pred[3]  # detected box
                obj_acc = float(pred[4])  # detected confidence score
                obj_class = int(pred[5])  # detected class
                loc = [ymin, xmin, ymax, xmax]

                print(f"\t > Object detected, "
                        f"Name: '{self.labelsIndex['name'][obj_class]}', "
                        f"Accuracy: {round(obj_acc * 100, 1)}%, "
                        f"Location: {loc}")

                filtered_det_obj = {"name": self.labelsIndex['name'][obj_class],
                                    "conf_score": obj_acc,
                                    "location": loc}

                detections.append(filtered_det_obj)
        return detections

    def checkTrainCondition(self) -> bool:
        pass

