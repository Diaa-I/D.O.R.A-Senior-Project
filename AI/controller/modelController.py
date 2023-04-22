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
from PIL import Image
import os


class ModelController(object):
    '''
    class responsible for managing the training and inference of the model.
    The methods, when called MUST follow this order:
        1. loadLabelsIndex() - only done once per Project.
        2. trainModel() - only done few times (when the conditions for training are satisfied).
        3. loadModel() - done as many times as trainModel() has been called.
        4. makeInference() - done for every image/frame.

    refer to the documentation of each method for more details.
    
    TODO:
        - test every method on a VM.
        - implement checkTrainCondition()
        - change the training output directory
        - add option to choose from a several starting checkpoint / model architecture for training.
    '''
    def __init__(self) -> None:
        self.labelsIndex = None
        self.model = None

    def trainModel(self, yamlFilepath, pretrainedWeights, imgTrainSize=(320, 320), epochs=20, batch_size=4) -> None:
        '''
        starts the training of the model with the given hyperparameters. 
        The trained model file is stored in yolov5m/runs/exp#/weights.
        The method assumes there's training dataset (images and labels) stored in train_data/images/train and train_data/labels/train.
        ====================================================
        Parameters:
            - yamlFilepath: string of the relative or absolute file path of the .yaml file of the dataset.
            - pretrainedWeights: string the relative or absolute file path of the .PT model file.
            - imgTrainSize: tuple representing (width, height). MUST both be equal, integers, and multiple of 160 (160, 320, 480 ..).
            - epochs: how many times the model will go through the whole dataset in training.
            - batch_size: how many images the model will train on during every iteration (forward and backward pass).
        returns: None.
        ====================================================
        Example of usage:
            > mc = ModelController()
            > mc.loadLabelIndex(r"yolov5m\data\myData.yaml")
            > mc.trainModel(yamlFilepath = r"yolov5m\data\myData.yaml", pretrainedWeights = r"yolov5m\yolov5m.pt", 
                            imgTrainSize = (640, 640), epochs = 10, batch_size = 4)
        '''
        train.run(data=yamlFilepath, imgsz=imgTrainSize, weights=pretrainedWeights, epochs=epochs, batch_size=batch_size)

    def loadTrainedModel(self, weightsPath, yamlFilepath) -> None:
        '''
        loads the model from a .PT file to an object self.model.
        loads the labelIndex as a dictionary from the .yaml file of the dataset. 
        the dictionary is used to convert labels from numerical form to a string.
        This function assumes a .yaml file has been created using the DataManager(), and the .PT using trainModel().
        ====================================================
        Parameters:
            - weightsPath: string of the relative or absolute path of the .PT model file.
            - yamlFilepath: the relative or absolute file path of the .yaml file of the dataset.
        returns: None.
        ====================================================
        Example of usage:
            > mc = ModelController()
            > mc.loadTrainedModel(weightsPath = r"yolov5m\runs\exp1\weights\best.pt", yamlFilepath = r"yolov5m\data\myData.yaml")
        '''
        # Load the YAML file as a dictionary
        with open(yamlFilepath, 'r') as file:
            self.labelsIndex = yaml.safe_load(file)
        
        # Load the trained PyTorch model file
        DEFAULT_YAML_PATH = r"yolov5m\data\coco128.yaml" # to-do: check if this needs to be changed to the trained YAML
        self.model = DetectMultiBackend(weights=weightsPath, dnn=False, data=DEFAULT_YAML_PATH, fp16=False) # load the model
        self.pt_stride, self.pt_names, self.pt = self.model.stride, self.model.names, self.model.pt
        imgsz = check_img_size((640, 640), s=self.pt_stride)  # check image size

    def makeInference(self, img, confThreshold=0.9, frameSize=(640, 640)) -> list:
        '''
        Processes an image (given as a 3D array) and outputs all the detected objects found.
        Detections will be considered only if they're above or equal to confThreshold.
        Image will be processed not according to its original size, but the size specified in frameSize.
        ====================================================
        Parameters:
            - img: a 3-D array representing the RGB of an image, or a 4-D array such that the last index is for batching.
            - confThreshold: float between 0 and 1 inclusive, only detected objects equal to or above this value will be returned.
            - frameSize: 2-value tuple of the dimensions of model input. MUST both be equal, integers, and multiple of 160 (160, 320, 480 ..).
        returns: list of python dictionaries of the form: [{'name': str, 'conf_score': float, 'location': [ymin, xmin, ymax, xmax]}, {...}, ...].
                In each dictionary, 'name' string represents the name of the label. 'conf_score' float between 0 and 1 represents how confident the model
                think this object belong to that label. 'location' is a list of the coordinates of the bounding box corners, the coordinates are normalized,
                hence they're all between 0 and 1.
        ====================================================
        Example of usage:
            > mc = ModelController()
            > mc.loadTrainedModel(weightsPath = r"yolov5m\runs\exp1\weights\best.pt", yamlFilepath = r"yolov5m\data\myData.yaml")
            > img = Image.open('path/to/image.png')
            > imgay = np.array(img)
            > det_1 = mc.makeInference(imgay, 0.8)
            > print(det_1)
        [{'name': 'cat', 'conf_score': 0.875, 'location': [0.644, 0.2, 0.15, 0.222]},
         {'name': 'cow', 'conf_score': 0.9753, 'location': [0.84, 0.23, 0.40, 0.15333]}]

            > det_2 = mc.makeInference(r"path\to\image.png", 0.5)
            > print(det_2[0])
        {'name': 'helicopter', 'conf_score': 0.68975, 'location': [0.55, 0.28, 0.15, 0.132]}
        '''
        assert (confThreshold <= 1 or confThreshold >= 0), "Confidence threshold must be equal to or less than 1 positive float."
        assert (frameSize[0] % 160 == 0 and frameSize[1] % 160 == 0), "Both the dimensions of the model input must be integers multiple of 160"
        assert ((isinstance(img, str) and os.path.exists(img)) or len(img.shape == 3) or len(img.shape == 4)), "invalid image input parameter, must be of a 3D or 4D shape, or a string to the path of an image file"

        # Preprocess image for model input
        img = letterbox(img, frameSize, stride=self.pt_stride)[0]  # padded resize
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB TODO: CHECK IF THIS SHOULD BE REMOVED
        img = np.ascontiguousarray(img)  # contiguous

        img = torch.from_numpy(img).to(self.model.device)
        img = img.half() if self.model.fp16 else img.float()
        img /= 255
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Make inference, apply NMS
        preds = self.model(img)
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
                        f"Confidence: {round(obj_acc * 100, 1)}%, "
                        f"Location: {loc}")

                filtered_det_obj = {"name": self.labelsIndex['name'][obj_class],
                                    "conf_score": obj_acc,
                                    "location": loc}

                detections.append(filtered_det_obj)
        return detections

    def checkTrainCondition(self) -> bool:
        pass

