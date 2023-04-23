import os
import yaml
import cv2


class DataManager(object):
    '''
    class responsible for managing the training and inference of the model.
    The methods, when called MUST follow this order:
        1. loadLabelsIndex() - only done once per Project.
        2. trainModel() - only done few times (when the conditions for training are satisfied).
        3. loadModel() - done as many times as trainModel() has been called.
        4. makeInference() - done for every image/frame.

    refer to the documentation of each method for more details.
        
    TODO:
        - change the name of 'DataManager' to 'Project'
        - add 2 attributrs, one for total number of frames, and one for current number of frames
    '''
    totalFrameCount = 0

    def __init__(self, labelsArray, projectName) -> None:
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
        assert len(labelsArray) > 0, "labelsArray cannot be an empty list"
        self.labelsArray = labelsArray # ['cat', 'dog', 'horse', ...]
        self.projectName = projectName # 'myProject'
        self.labelsIndex = {i: self.labelsArray[i] for i in range(len(self.labelsArray))} # {0: 'cat', 1: 'dog', 2: 'horse', ...}
        self.labelsToIndex = {self.labelsIndex[i]: i for i in range(len(self.labelsIndex))} # {'cat': 0, 'dog': 1, 'horse': 2, ...}
    
    def createYaml(self, at) -> None:
        '''
        Create and store a YAML file for the set of labels provided. The file will be named after the project name provided in constructor.
        ====================================================
        Parameters:
            - at: string of the path of the directory where the .yaml file will be stored.
        returns: None.
        ====================================================
        Example of usage:
            > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
            > dm.createYaml(at=r"path\to\directory")
        '''
        assert os.path.exists(at), "Specified path to store YAML file doesn't exist."

        # Set the paths to the YAML file
        file_path = os.path.join(at, f'{self.projectName}.yaml')

        # If no file already exits, create one and fill it with the labels
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                myDataYaml = {'path': "../train_data", "train": "images/train", "val": "images/val", "names": self.labelsIndex.copy()}
                yaml.dump(myDataYaml, f, sort_keys=False)

                print(f'{file_path} created.')
        else:
            print(f'{file_path} already exists.')

    def extractFrames(self, videoFilepath, outputDir) -> None:
        '''
        prases a video into frames and stores them as .JPG images in a directory.
        ====================================================
        Parameters:
            - videoFilepath: string of the relative or absolute path of the video file.
            - outputDir: string of the relative or absolute path of the directory where all the parsed frames will be stored.
        returns: None.
        ====================================================
        Example of usage:
            > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
            > dm.extractFrames(r"path\to\video.mp4", r"path\to\images\directory")
            > print(os.listdir(r"path\to\images\directory"))
        0_animals_detection.jpg
        1_animals_detection.jpg
        2_animals_detection.jpg
        ...
        1203_animals_detection.jpg
        '''
        # Open the video file
        cap = cv2.VideoCapture(videoFilepath)

        # Create the output directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Initialize the frame count and loop over all frames
        count_init = self.totalFrameCount
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(outputDir, f"{self.totalFrameCount}_{self.projectName}.jpg") # EDIT projName to a class attribute
            if not os.path.exists(output_path):
                cv2.imwrite(output_path, frame)
            else:
                print(f"{output_path} already exists")

            # Increment the frame count
            self.totalFrameCount += 1

        # Release the video capture object
        cap.release()
        print(f"Extracted {self.totalFrameCount - count_init} frames from {videoFilepath}.")

    def storeAsYOLOtxt(self, annObjsArray, at) -> None:
        '''
        Given an array of python dictionaries in a specific format representing annotations, method will store the annotations in a .TXT file
        formatted according to YOLO's annotations specifications.
        TODO:
            - make it so that it accepts more than 1 annotation per image (can store multiple annotations in one .txt file)
        ====================================================
        Parameters:
            - annObjsArray: a list of lists, each in the following format: [img_file, label, x_center, y_center, width, height]. img_file is the file name of
              image containing this annotation. label is the name of the label tagged to this annotation. x_center and y_center are the x and y coordinates of the
              center of the bounding box. width and height are the width and height of the bounding box. Note that the x_center, y_center, width, and height here are
              not normalized.
            - at: string of the path of the directory where the .txt files will be stored.
        returns: None.
        ====================================================
        Example of usage:
            > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
            > dm.storeAsYOLOtxt([   
                                    ['12_animals_detection.JPEG', 'cat', 25.666, 355, 120, 560], 
                                    ['13_animals_detection.JPEG', 'dog', 60.686, 550, 220, 367] 
                                ],
                                at = r"train_data\labels\train")
            > print(os.listdir(r"train_data\labels\train"))
        0_animals_detection.txt
        1_animals_detection.txt
        2_animals_detection.txt
        ...
        144_animals_detection.txt
        '''
        for annObj in annObjsArray:
            # get image width and height
            full_path = os.path.join("AI", "sandbox", annObj[0]) # TODO: CHANGE 'AI\sandbox' TO 'train_data\images\train'
            img_height, img_width, _ = cv2.imread(full_path).shape

            # change file name to be from .JPG to .TXT
            filename_noExt = annObj[0].split('.')[0]
            path = os.path.join(at, filename_noExt + '.txt')

            # create the file, dump all the data into it and close it
            with open(path, 'w') as annFile:
                label = self.labelsToIndex[annObj[1]]
                x_center, y_center, width, height = self.normalize_coordinates(annObj[2], annObj[3], annObj[4], annObj[5], img_width=img_width, img_height=img_height)
                annFile.write(f"{label} {x_center} {y_center} {width} {height}")
                annFile.close()
    
    @staticmethod
    def normalize_coordinates(x, y, width, height, img_width, img_height):
        '''
        Used to normalize values given an image width. 
        Normalization in math is the calculation of having a number between 1 and 0 relative to another number.
        Normalization is needed as it's the standard form of numbers YOLO uses in storing the annotation labels.
        '''
        # Calculate the normalized values
        x_norm = x / img_width
        y_norm = y / img_height
        w_norm = width / img_width
        h_norm = height / img_height
        return x_norm, y_norm, w_norm, h_norm