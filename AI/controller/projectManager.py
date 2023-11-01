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
    
    def create_yaml(self, at) -> None:
        '''
        Create and store a YAML file for the set of labels provided. The file will be named after the project name provided in constructor.
        ====================================================
        Parameters:
            - at: the directory path where the .yaml file will be stored.
        ====================================================
        Example of usage:
            > pm = ProjectManager(['cat', 'dog', 'horse'], 'animals_detection')
            > pm.create_yaml(at=r"path\to\directory")
        '''
        assert os.path.exists(at), "Specified path to store YAML file doesn't exist."

        # Set the paths to the YAML file
        file_path = os.path.join(at, f'{self.project_name}.yaml')

        # If no file already exits, create one and fill it with the labels
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                myDataYaml = {'path': "../train_data", "train": "images/train", "val": "images/val", "names": self.index_to_labels.copy()}
                yaml.dump(myDataYaml, f, sort_keys=False)

                print(f'{file_path} created.')
        else:
            print(f'{file_path} already exists.')

    def extract_frames(self, video_filepath, output_dir) -> None:
        '''
        prases a video into frames and stores them as .JPG images in a directory.
        ====================================================
        Parameters:
            - video_filepath: the path to the video file.
            - output_dir: the directory path where all the frames will be stored.
        ====================================================
        Example of usage:
            > pm = ProjectManager(['cat', 'dog', 'horse'], 'animals_detection')
            > dm.extract_frames(r"path\to\video.mp4", r"path\to\images\directory")
            > print(os.listdir(r"path\to\images\directory"))
        0_animals_detection.jpg
        1_animals_detection.jpg
        2_animals_detection.jpg
        ...
        1203_animals_detection.jpg
        '''
        # Open the video file
        cap = cv2.VideoCapture(video_filepath)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Initialize the frame count and loop over all frames
        count_init = self.total_project_images
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(output_dir, f"{self.total_project_images}_{self.project_name}.jpg") # EDIT projName to a class attribute
            if not os.path.exists(output_path):
                cv2.imwrite(output_path, frame)
                self.all_frames_paths.append(output_path)
            else:
                print(f"{output_path} already exists")

            # Increment the frame count
            self.total_project_images += 1

        # Release the video capture object
        cap.release()
        print(f"Extracted {self.total_project_images - count_init} frames from {video_filepath}")

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
            - annotations_array: an array containing a list of annotation objects representing the boxes drawn. Each annotation object is represneted as: {'label': 'string', 'x_center': float, 'y_center': float, 'width': float, 'height': float}
               - label is the name of the label associated with the box, given as a string.
               - x_center and y_center are the x, y coordinates of the center of annotation boxes (absolute value, not normalized).
               - width and height are the dimesnsions of the annotation box (absolute value, not normalized).
            - saveto_dir: the path to the directory where the .txt file will be saved.
        ====================================================
        Usage Example:
        > pm.create_annotations_txt('path/to/trash_detection.yaml', "frame_00423", 400, 600, 
            [{'label': 'plastic', 'x_center': 80, 'y_center': 234, 'width': 30, 'height': 80}, 
             {'label': 'metal', 'x_center': 20.01, 'y_center': 354.2, 'width': 25, 'height': 45.6}], 
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
                bbox_x_center = annotation['x_center']
                bbox_y_center = annotation['y_center']
                bbox_width = annotation['width']
                bbox_height = annotation['height']

                # get the x, y, w, and h values normalized relative the img height and width
                x_center_norm, y_center_norm, width_norm, height_norm = ProjectManager.normalize_coordinates(bbox_x_center, bbox_y_center,
                                                                                                    bbox_width, bbox_height,
                                                                                                    img_width, img_height)

                # write to the txt file
                bbox_info_row = f"{label_index} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"
                if i != len(annotations_array) - 1: # so that last row doesn't create a new line
                    bbox_info_row = bbox_info_row + '\n'
                annotation_file.write(bbox_info_row)
        
    def retrieve_next_batch(self, starting_from=None, retrieval_size=10) -> str:
        '''
        returns a json string with retrieval_size number of images filepaths in batches every time it's called. Starts from 0 index and moves retrieval_size.
        retrieval_size is set to 10 by default.
        ====================================================
        Parameters:
            - retrieval_size: the number of filepaths to be returned in each batch.
        ====================================================
        returns: string representing json that contains a list of relative filepaths to 'output_dir' and all its files.
        ====================================================
        Example of usage:
            > pm = ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
            > pm.extract_frames(video_filepath=r".\dir\Vid.mp4", output_dir=r".\data")
            > pm.retrieve_next_batch()
        {
            "batch_start_index": 0,
            "batch_end_index": 10,                  
            "filepaths": 
            [
                .\\data\\0_animals_detection.jpg
                .\\data\\1_animals_detection.jpg
                .\\data\\2_animals_detection.jpg
                ...
                .\\data\\9_animals_detection.jpg
            ]
        }

        '''
        self.image_retrieval_index = starting_from if starting_from is not None else self.image_retrieval_index
        start = self.image_retrieval_index
        end = self.image_retrieval_index + retrieval_size

        if start < self.total_project_images - 1:
            if end < self.total_project_images - 1:
                self.image_retrieval_index = end
                paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_frames_paths[start:end]
                })
                return paths_batch_json
            else:
                end = self.total_project_images - 1
                self.image_retrieval_index = end
                paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_frames_paths[start:end]
                })
                return paths_batch_json
        else:
            paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": []
                })
            return paths_batch_json

    def retrieve_previous_batch(self, starting_from=None, retrieval_size=10) -> str:
        '''
        returns a json string with the previous retrieval_size number of images filepaths in batches every time it's called. Starts from 'starting_from' as an index.
        ====================================================
        Parameters:
            - retrieval_size: the number of filepaths to be returned in each batch.
            - starting_from: the index at which the previous batch will be retrieved. Defaults to the global imageRetrievalIndex pointer.
        ====================================================
        returns: string representing json that contains a list of relative filepaths to 'output_dir' and all its files.
        ====================================================
        Example of usage:
        > pm = ProjectManager(['cat', 'dog', 'lion'], 'animals_detection')
        > pm.extract_frames(video_filepath=r".\dir\Vid.mp4", output_dir=r".\data")
        > pm.retrieve_previous_batch(starting_from=100, retrieval_size=2)
        {
            "batch_start_index": 100,
            "batch_end_index": 98,                  
            "filepaths": 
            [
                .\\data\\99_animals_detection.jpg,
                .\\data\\100_animals_detection.jpg
            ]
        }
        > pm.retrievePreviousBatch(retrieval_size=2)
        {
            "batch_start_index": 98,
            "batch_end_index": 96,                  
            "filepaths": 
            [
                .\\data\\97_animals_detection.jpg,
                .\\data\\98_animals_detection.jpg
            ]
        }
        '''
        self.image_retrieval_index = starting_from if starting_from is not None else self.image_retrieval_index
        start = self.image_retrieval_index
        end = start - retrieval_size

        if start > 0:
            if end > -1:
                self.image_retrieval_index = end
                paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_frames_paths[end+1:start+1]
                })
                return paths_batch_json
            else:
                paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": self.all_frames_paths[0:start]
                })
                return paths_batch_json
        else:
            paths_batch_json = json.dumps({
                    "batch_start_index": start,
                    "batch_end_index": end,                  
                    "filepaths": []
            })
            return paths_batch_json

    @staticmethod
    def normalize_coordinates(x, y, w, h, img_width, img_height):
        '''
        Used to normalize values given an image width. 
        Normalization in math is the calculation of having a number between 1 and 0 relative to another number.
        Normalization is needed as it's the standard form of numbers YOLO uses in storing the annotation labels.
        '''
        # Calculate the normalized values
        x_norm = x / img_width
        y_norm = y / img_height
        w_norm = w / img_width
        h_norm = h / img_height
        return x_norm, y_norm, w_norm, h_norm
