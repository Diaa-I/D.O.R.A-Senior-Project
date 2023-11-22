# add the 'yolov5m to path to be able to import it into python
import sys
from pathlib import Path
from ultralytics import YOLO
import os

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
try:
    sys.path.remove(str(parent))  # remove the current file's directory from sys.path
except ValueError:  # Already removed
    pass


class ModelController(object):

    @staticmethod
    def train_model(yaml_filepath, pretrained_model_path, saveto_dir, name, img_train_size=320, epochs=20, batch_size=8) -> str:
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
                  batch=batch_size, plots=False, project=saveto_dir, name=name)
        trained_model_path = os.path.join(saveto_dir, name, 'weights', 'best.pt')
        return trained_model_path

    @staticmethod
    def make_inference(img_filepath, model_filepath, normalization_dims, conf_threshold=0.8) -> list:
        '''
        Processes an image and outputs all the detected objects found in it.
        Detections will be considered only if they're above or equal to conf_threshold.
        The location of the returned boxes will be relative to 'normalization_dims'.
        ====================================================
        Parameters:
            - img_filepath: the path of the image.
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
                                                    model_filepath=r"path/to/model/best.pt",
                                                    conf_threshold=0.8)
        [{'name': 'metal', 'conf_score': 0.880242, 'location': [144.26025, 108.88249, 261.6675, 263.0825]},
         {'name': 'paper', 'conf_score': 0.93452, 'location': [61.7375, 146.6877, 378.0625, 267.0625]}]
        '''
        model = YOLO(model_filepath)
        result = model(img_filepath)[0] # only 1 image file will be passed
        filtered_results = []
        norm_w, norm_h = normalization_dims[0], normalization_dims[1]

        # get data from model in python standard data types
        index2label = result.names
        detected_classes = [int(cls) for cls in result.boxes.cls]
        conf_scores = [float(conf) for conf in result.boxes.conf]
        xyxy_norm = [[float(coord) for coord in coords_list] for coords_list in result.boxes.xyxyn]

        # store the data as json objects in one list
        for cls, conf, coords in zip(detected_classes, conf_scores, xyxy_norm):
            if conf >= conf_threshold:
                label = index2label[cls]
                x_min, y_min, x_max, y_max = coords[0], coords[1], coords[2], coords[3]
                x_min, y_min, x_max, y_max = x_min*norm_w, y_min*norm_h, x_max*norm_w, y_max*norm_h #de-normalize the coordinates
                filtered_result = {'name':label, 'conf_score':conf, 'location':[x_min, y_min, x_max, y_max]}
                print(filtered_result)
                filtered_results.append(filtered_result)

        return filtered_results

