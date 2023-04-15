import os
import yaml
import cv2

'''
to-do:
    - change the name of 'DataManager' to 'Project'
    - add 2 attributrs, one for total number of frames, and one for current number of frames
'''

class DataManager(object):
    currentFrame = 0

    def __init__(self, labelsArray, projectName):
        self.labelsArray = labelsArray # ['cat', 'dog', 'horse', ...]
        self.projectName = projectName # 'myProject'
        self.labelsIndex = {i: self.labelsArray[i] for i in range(len(self.labelsArray))} # {0: 'cat', 1: 'dog', 2: 'horse', ...}
        self.labelsToIndex = {self.labelsIndex[i]: i for i in range(len(self.labelsIndex))} # {'cat': 0, 'dog': 1, 'horse': 2, ...}
    
    def createYaml(self, at):
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

    def extractFrames(self, videoFile, outputDir):
        # Open the video file
        cap = cv2.VideoCapture(videoFile)

        # Create the output directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Initialize the frame count and loop over all frames
        count_init = self.currentFrame
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(outputDir, f"{self.currentFrame}_{self.projectName}.jpg") # EDIT projName to a class attribute
            if not os.path.exists(output_path):
                cv2.imwrite(output_path, frame)
            else:
                print(f"{output_path} already exists")

            # Increment the frame count
            self.currentFrame += 1

        # Release the video capture object
        cap.release()
        print(f"Extracted {self.currentFrame - count_init} frames from {videoFile}.")

    def storeAsYOLOtxt(self, annObjsArray, at):
        # the annObjArray must be an array in the form of: 
        #    [[frameFileName, img_width, img_height, objLabel, x_center, y_center, width, height], ...]
        # e.g. ['12.JPEG', 1200, 800, 'cat', 25.666, 355, 120, 560]
        # CHANGE IT SO THAT AN ANNOTATION FILE CAN HAVE MORE THAN 1 ANNOTATION
        for annObj in annObjsArray:
            # get image width and height
            full_path = os.path.join("AI", "sandbox", annObj[0]) # CHANGE 'AI\sandbox' TO 'train_data\images\train'
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
        # Calculate the normalized values
        x_norm = x / img_width
        y_norm = y / img_height
        w_norm = width / img_width
        h_norm = height / img_height
        return x_norm, y_norm, w_norm, h_norm



DM = DataManager(['cat', 'dog', 'horse'], 'projName')
print("DataManger: initialized")

DM.createYaml(at="AI\sandbox")
print("DataManger: YAML created")

DM.extractFrames(videoFile=r"AI\sandbox\sample.mp4", outputDir=r"AI\sandbox")
print("DataManger: frames extracted")

DM.storeAsYOLOtxt([['0_projName.jpg', 'cat', 25.666, 355, 120, 560], 
                   ['1_projName.jpg', 'dog', 16.566, 50, 40, 1000]], 
                   at=r"AI\sandbox")
print("DataManager: .txt annotation files created")