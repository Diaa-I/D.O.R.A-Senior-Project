import os
import yaml
import cv2

'''
to-do:
    - change the name of 'DataManager' to 'Project'
'''

class DataManager(object):

    def __init__(self, labelsArray, projectName):
        self.labelsArray = labelsArray
        self.projectName = projectName
        self.labelsIndex = {i: self.labelsArray[i] for i in range(len(self.labelsArray))}

    def createYaml(self, at="sandbox"):
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

# createYaml("myProj", ['lab1', 'lab2', 'lab3'])

    def extractFrames(self, videoFile, outputDir):
        # Open the video file
        cap = cv2.VideoCapture(videoFile)

        # Create the output directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Initialize the frame count and loop over all frames
        count = 0
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(outputDir, f"{count}_{self.projectName}.jpg") # EDIT projName to a class attribute
            cv2.imwrite(output_path, frame)

            # Increment the frame count
            count += 1

        # Release the video capture object
        cap.release()
        print(f"Extracted {count} frames from {videoFile}.")

# extractFrames("sandbox/sample.mp4", "sandbox")

    def storeAsYOLOtxt(self, annObjsArray):
        # the annObjArray must be an array in the form of: 
        #    [[objLabel, x_center, y_center, width, height], [objLabel, x_center, y_center, width, height], ...]
        # x_center, y_center, width and height must all be normalized relative to the image dimensions.
        # objLabel is given as a name (e.g. cat) but converted using the labelIndex to a number
        pass