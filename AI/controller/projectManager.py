import os, yaml, cv2, json


class ProjectManager(object):
    '''
    class containing utilities for creating required files before, during, and after training.
    refer to the documentation of each method for more details.
    '''
    total_project_images = 0
    image_retrieval_index = 0
    all_frames_paths = []

    def __init__(self, labels_array, project_name) -> None:
        '''
        Instansiates an object specific to a set of labels.
        ====================================================
        Parameters:
            - labelsArray: a list containing strings of the names of each label in the dataset.
            - projectName: a string representing the title of the dataset's project.
        returns: None.
        ====================================================
        Example of usage:
            > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
            > print(dm.labelsIndex)
        {0: 'cat', 1: 'dog', 2:'horse'}
            > print(dm.labelsToIndex)
        {'cat': 0, 'dog': 1, 'horse': 2}
        '''
        assert len(labels_array) > 0, "labelsArray cannot be an empty list"
        self.labels_array = labels_array # ['cat', 'dog', 'horse', ...]
        self.project_name = project_name # 'myProject'
        self.index_to_labels = {i: self.labels_array[i] for i in range(len(self.labels_array))} # {0: 'cat', 1: 'dog', 2: 'horse', ...}
        self.labels_to_index = {self.index_to_labels[i]: i for i in range(len(self.index_to_labels))} # {'cat': 0, 'dog': 1, 'horse': 2, ...}

    @staticmethod
    def create_annotations_txt(yaml_filepath, associated_image_name, img_width, img_height, annotations_array, saveto_dir) -> None:
        '''
        Create an annotation file following YOLO's format for training models.
        ====================================================
        Parameters:
            - yaml_filepath: the path to the .yaml file that contains the labels of the project.
            - associated_image_name: name of the frame/image of where the annotation box is located. Can be a name only (e.g. frame_0443), or a file name (e.g. frame_0443.png) or a path.
            - img_width: the width of the image where the annotation box is located.
            - img_height: the height of the image where the annotation box is located.
            - annotations_array: an array containing a list of annotation objects representing the boxes drawn. Each annotation object is represneted as: {'label': 'string', 'x_min': float, 'y_min': float, 'width': float, 'height': float}
               - label is the name of the label associated with the box, given as a string.
               - x_center and y_center are the x, y coordinates of the center of annotation boxes (absolute value, not normalized).
               - width and height are the dimesnsions of the annotation box (absolute value, not normalized).
            - saveto_dir: the path to the directory where the .txt file will be saved.
        ====================================================
        Usage Example:
        > pm.create_annotations_txt('path/to/trash_detection.yaml', "frame_00423", 400, 600, 
            [{'label': 'plastic', 'x': 80, 'y': 234, 'width': 30, 'height': 80}, 
             {'label': 'metal', 'x': 20.01, 'y': 354.2, 'width': 25, 'height': 45.6}], 
            "./mydir")
        '''
        # Load the YAML file as a dictionary
        with open(yaml_filepath, 'r') as file:
            index_to_labels = yaml.safe_load(file)['names']

        labels_to_index = {index_to_labels[i]: i for i in range(len(index_to_labels))} # {'cat': 0, 'dog': 1, 'horse': 2, ...}

        # get the associated image name only (without extension, or the file path)
        base_name, extension = os.path.splitext(associated_image_name)
        associated_image_name_without_extension = os.path.basename(base_name)

        # get the file path of where the .txt annotations file will be saved
        saveto_filepath = os.path.join(saveto_dir, associated_image_name_without_extension + '.txt')
        with open(saveto_filepath, "w") as annotation_file:

            # annotation object format: {'label': 'dog', 'x_center': 45.5, 'y_center': 79.0, 'width': 14.3, 'height': 30.0}
            for i, annotation in enumerate(annotations_array):
                # get the labels index (the number representing the label)
                label_index = labels_to_index[annotation['label']]
                bbox_width = annotation['width']
                bbox_height = annotation['height']
                bbox_x_center = annotation['x'] + (bbox_width / 2.0)
                bbox_y_center = annotation['y'] + (bbox_height / 2.0)


                # get the x, y, w, and h values normalized relative the img height and width
                x_center_norm, y_center_norm, width_norm, height_norm = ProjectManager.normalize_coordinates(bbox_x_center, bbox_y_center,
                                                                                                    bbox_width, bbox_height,
                                                                                                    img_width, img_height)

                # write to the txt file
                bbox_info_row = f"{label_index} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"
                if i != len(annotations_array) - 1: # so that last row doesn't create a new line
                    bbox_info_row = bbox_info_row + '\n'
                annotation_file.write(bbox_info_row)

    @staticmethod
    def normalize_coordinates(x, y, w, h, img_width, img_height):
        '''
        Used to normalize values (x, y, w, h) of a coordinates given an image width and height.
        x and w will be normalized relative to img_width. y and h will be normalized relative to img_height.
        Normalization in math is the calculation of having a number between 1 and 0 relative to another number.
        Normalization is needed as it's the standard form of numbers YOLO uses in storing the annotation labels.
        '''
        # check for irregularities (such as coordinates outside of image)
        TOLERANCE = 5
        assert img_height > 0 and img_width > 0, "Image width and height cannot be a negative"
        assert x > 0 and y > 0 and w > 0 and h > 0, 'The provided values to be normalized must not contain a negative number'
        assert x <= img_width + TOLERANCE and y <= img_height + TOLERANCE and w < img_width + TOLERANCE and h < img_height + TOLERANCE, \
            "The provided values to be normalized are out of the image boundaries"

        # Calculate the normalized values
        x_norm = x / img_width
        y_norm = y / img_height
        w_norm = w / img_width
        h_norm = h / img_height
        return x_norm, y_norm, w_norm, h_norm
    
    @staticmethod
    def denormalize_coordinates(x_norm, y_norm, w_norm, h_norm, img_width, img_height):
        '''
        Does the opposite operation as to 'normalize_coordinates'. That is, given a set of values representing the coordinates (x, y, w, h)
        That are normalized (and therefore between 0 and 1), the function will return their true absolute position relative to the image.
        '''
        assert img_height > 0 and img_width > 0, "Image width and height cannot be a negative"
        assert 1 >= x >= 0 and 1 >= y >= 0 and 1 >= w >= 0 and 1 >= h >= 0, 'The provided values to be de-normalized must be between 0 and 1'
        x = x_norm * img_width
        y = y_norm * img_height
        w = w_norm * img_width
        h = h_norm * img_height

        TOLERANCE = 5
        assert x <= img_width + TOLERANCE and y <= img_height + TOLERANCE and w < img_width + TOLERANCE and h < img_height + TOLERANCE, \
        "The provided values to be de-normalized are out of the image boundaries"
        return x, y, w, h