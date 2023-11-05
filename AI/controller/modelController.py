# add the 'yolov5m to path to be able to import it into python
import sys
from pathlib import Path
from ultralytics import YOLO

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
try:
    sys.path.remove(str(parent))  # remove the current file's directory from sys.path
except ValueError:  # Already removed
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
        1. train_model() - only done few times (when the conditions for training are satisfied).
        2. make_inference() - done for every image/frame.

    refer to the documentation of each method for more details.

    TODO:
        - change the training output directory
        - add option to choose from a several starting checkpoint / model architecture for training.
    '''

    @staticmethod
    def train_model(yaml_filepath, pretrained_model_path, saveto_dir, name, img_train_size=640, epochs=20, batch_size=4) -> str:
        '''
        starts the training of the model with the given hyperparameters.
        The trained model file is stored in yolov5m/runs/exp#/weights.
        The method assumes there's training dataset (images and labels) stored in train_data/images/train and train_data/labels/train.
        ====================================================
        Parameters:
            - yaml_filepath: string of the relative or absolute file path of the .yaml file of the dataset.
            - pretrained_model_path: string the relative or absolute file path of the .PT model file.
            - saveto_dir: the directory where the model's new directory will be save (the new directory will be saveto_dir/name)
            - name: the name of the directory which contains the weights, it will be a child of saveto_dir. MUST be a unique name.
            - img_train_size: tuple representing (width, height). MUST both be equal, integers, and multiple of 160 (160, 320, 480 ..).
            - epochs: how many times the model will go through the whole dataset in training.
            - batch_size: how many images the model will train on during every iteration (forward and backward pass).
        Returns:
            the filepath of where the model file is stored (saveto_dir/name/weights/best.pt)
        ====================================================
        Example of usage:
            > mc = ModelController()
            > mc.train_model(yaml_filepath = r"yolov5m\data\myData.yaml", pretrained_model_path = r"yolov5m\yolov5m.pt", 
                            saveto_dir = '~/Desktop', name='exp322', img_train_size = 320, epochs = 10, batch_size = 4)
        '''
        model = YOLO(pretrained_model_path)
        model.train(data=yaml_filepath, imgsz=img_train_size, epochs=epochs,
                  batch_size=batch_size, noplots=True, project=saveto_dir, name=name)
        trained_model_path = os.path.join(saveto_dir, name, 'weights', 'best.pt')
        return trained_model_path

    @staticmethod
    def make_inference(img, yaml_filepath, model_filepath, normalization_dims, conf_threshold=0.9) -> list:
        '''
        Processes an image and outputs all the detected objects found in it.
        Detections will be considered only if they're above or equal to conf_threshold.
        Image will be processed not according to its original size, but the size specified in FRAME_SIZE.
        ====================================================
        Parameters:
            - img: the path of the image.
            - yaml_filepath: the path to the .yaml file that contains the labels of the trained model to use for inference.
            - model_filepath: the path to the .pt model file that will be used for inference.
            - normalization_dims: a tuple in the form of (weight, height) that the returned coordinates of each detection will be relative to.
            - conf_threshold: float between 0 and 1 inclusive, only detected objects equal to or above this value will be returned.
        returns: 
            list of python dictionaries of the form: [{'name': str, 'conf_score': float, 'location': [xmin, ymin, xmax, ymax]}, {...}, ...].
            In each dictionary, 'name' string represents the name of the label. 'conf_score' float between 0 and 1 represents how confident the model
            think this object belong to that label. 'location' is a list of the coordinates of the bounding box corners, the coordinates are normalized,
            hence they're all between 0 and 1.
        ====================================================
        Example of usage:
        > det = con.modelController.ModelController.make_inference(img='path/to/image.jpg',
                                                    normalization_dims=(512, 384),
                                                    yaml_filepath=r"path/to/yaml/trash_detection.yaml",
                                                    model_filepath=r"path/to/model/best.pt",
                                                    conf_threshold=0.8)
        [{'name': 'metal', 'conf_score': 0.480242, 'location': [144.26025, 108.88249, 261.6675, 263.0825]},
         {'name': 'metal', 'conf_score': 0.13452, 'location': [61.7375, 146.6877, 378.0625, 267.0625]}]
        '''
        FRAME_SIZE = (640, 640) # the size of the processed image into the model
        assert (conf_threshold <= 1 or conf_threshold >= 0), "Confidence threshold must be equal to or less than 1 positive float."
        
        # If img is given as a file path, load the image, and convert it to 3D numpy array
        img_object = Image.open(img)
        img_object = img_object.resize(FRAME_SIZE, Image.LANCZOS)
        img = np.array(img_object)

        # Load the YAML file as a dictionary
        with open(yaml_filepath, 'r') as file:
            index_to_labels = yaml.safe_load(file)
        
        # Load the trained PyTorch model file
        pt_model = DetectMultiBackend(weights=model_filepath, dnn=False, data=yaml_filepath,
                                      fp16=False)  # load the model
        pt_stride, pt_names, pt = pt_model.stride, pt_model.names, pt_model.pt
        imgsz = check_img_size(FRAME_SIZE, s=pt_stride)  # check image size
        
        # Preprocess image for model input
        img = letterbox(img, FRAME_SIZE, stride=pt_model.stride)[0]  # padded resize
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB TODO: CHECK IF THIS SHOULD BE REMOVED
        img = np.ascontiguousarray(img)  # contiguous

        img = torch.from_numpy(img).to(pt_model.device)
        img = img.half() if pt_model.fp16 else img.float()
        img /= 255
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Make inference, apply NMS
        preds = pt_model(img)
        preds = non_max_suppression(preds, conf_thres=conf_threshold, iou_thres=0.25, max_det=500)
        # Filter and store predictions
        detections = []  # e.g. [{'name': 'cat', conf_score: 0.875, location: [0.644, 0.2, 0.15, 0.222]}, ... ]
        for pred in preds[0]:
            if len(pred) > 0 and float(pred[4]) >= conf_threshold:
                xmin, ymin, xmax, ymax = float(pred[0]), float(pred[1]), float(pred[2]), float(pred[3])  # detected box
                norm_w, norm_h = normalization_dims[0], normalization_dims[1] # to return the coordinates relative to the given dimensions
                xmin, ymin, xmax, ymax = (xmin/FRAME_SIZE[0])*norm_w, (ymin/FRAME_SIZE[0])*norm_h, (xmax/FRAME_SIZE[0])*norm_w, (ymax/FRAME_SIZE[0])*norm_h
                obj_acc = float(pred[4])  # detected confidence score
                obj_class = int(pred[5])  # detected class
                loc = [float(xmin), float(ymin), float(xmax), float(ymax)]

                print(f"\t > Object detected, "
                        f"Name: '{index_to_labels['names'][obj_class]}', "
                        f"Confidence: {round(obj_acc * 100, 1)}%, "
                        f"Location: {loc}")

                filtered_det_obj = {"name": index_to_labels['names'][obj_class],
                                    "conf_score": obj_acc,
                                    "location": loc}
                detections.append(filtered_det_obj)

        return detections

