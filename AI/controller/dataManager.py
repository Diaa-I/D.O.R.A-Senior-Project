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
        #    [[frameFileName, objLabel, x_center, y_center, width, height], [frameFileName, objLabel, x_center, y_center, width, height], ...]
        # e.g. ['12.JPEG', 'cat', 25.666, 355, 120, 560]
        # x_center, y_center, width and height must all be normalized relative to the image dimensions.
        # objLabel is given as a name (e.g. cat) but converted using the labelIndex to a number
        for annObj in annObjsArray:
            # change file name to be from .JPG to .TXT
            filename_noExt = annObj[0].split('.')[0]
            path = os.path.join(at, filename_noExt + '.txt')
            # create the file, dump all the data into it and close it
            with open(path, 'w') as annFile:
                objLabel = self.labelsToIndex[annObj[1]]
                x_center, y_center, width, height = annObj[2], annObj[3], annObj[4], annObj[5]
                annFile.write(f"{objLabel} {x_center} {y_center} {width} {height}")
                annFile.close()


# in use
# DM = DataManager(['cat', 'dog', 'horse'], 'projName')
# print("DataManger: initialized")

# DM.createYaml(at="AI\sandbox")
# print("DataManger: YAML created")

# DM.extractFrames(videoFile=r"AI\sandbox\sample.mp4", outputDir=r"AI\sandbox")
# print("DataManger: frames extracted")

# DM.storeAsYOLOtxt([['0_projName.jpg', 'cat', 25.666, 355, 120, 560]], at=r"AI\sandbox")
# print("DataManager: .txt annotation files created")