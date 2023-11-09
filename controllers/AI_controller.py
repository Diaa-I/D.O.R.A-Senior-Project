# import os, yaml, cv2, json
# from database import mongo_connection
# from flask import jsonify
#
#
# Projects = mongo_connection.Projects
# project_specifications = {
# "project_name":,
# "labels_index":,
#
# }
#
# def get_project_information():
#     Project = Projects.find_one({})
#     response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size']})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
#     return response
#
#
#  def storeAsYOLOtxt() -> None:
#         '''
#         Given an array of python dictionaries in a specific format representing annotations, method will store the annotations in a .TXT file
#         formatted according to YOLO's annotations specifications.
#         TODO:
#             - make it so that it accepts more than 1 annotation per image (can store multiple annotations in one .txt file)
#         ====================================================
#         Parameters:
#             - annObjsArray: a list of lists, each in the following format: [img_file, label, x_center, y_center, width, height]. img_file is the file name of
#               image containing this annotation. label is the name of the label tagged to this annotation. x_center and y_center are the x and y coordinates of the
#               center of the bounding box. width and height are the width and height of the bounding box. Note that the x_center, y_center, width, and height here are
#               not normalized.
#             - at: string of the path of the directory where the .txt files will be stored.
#         returns: None.
#         ====================================================
#         Example of usage:
#             > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
#             > dm.storeAsYOLOtxt([
#                                     ['12_animals_detection.JPEG', 'cat', 25.666, 355, 120, 560],
#                                     ['13_animals_detection.JPEG', 'dog', 60.686, 550, 220, 367]
#                                 ],
#                                 at = r"train_data\labels\train")
#             > print(os.listdir(r"train_data\labels\train"))
#         0_animals_detection.txt
#         1_animals_detection.txt
#         2_animals_detection.txt
#         ...
#         144_animals_detection.txt
#         '''
#         for annObj in annObjsArray:
#             # get image width and height
#             full_path = os.path.join("AI", "sandbox", annObj[0]) # TODO: CHANGE 'AI\sandbox' TO 'train_data\images\train'
#             img_height, img_width, _ = cv2.imread(full_path).shape
#
#             # change file name to be from .JPG to .TXT
#             filename_noExt = annObj[0].split('.')[0]
#             path = os.path.join(at, filename_noExt + '.txt')
#
#             # create the file, dump all the data into it and close it
#             with open(path, 'w') as annFile:
#                 # Location of yaml file
#                 label = self.labelsToIndex[annObj[1]]
#
#                 # x_center, y_center, width, height = self.normalize_coordinates(annObj[2], annObj[3], annObj[4], annObj[5], img_width=img_width, img_height=img_height)
#                 annFile.write(f"{label} {x_center} {y_center} {width} {height}")
#                 annFile.close()
#
#
#
# def createYaml(at) -> None:
#     '''
#     Create and store a YAML file for the set of labels provided. The file will be named after the project name provided in constructor.
#     ====================================================
#     Parameters:
#         - at: string of the path of the directory where the .yaml file will be stored.
#     returns: None.
#     ====================================================
#     Example of usage:
#         > dm = DataManager(['cat', 'dog', 'horse'], 'animals_detection')
#         > dm.createYaml(at=r"path\to\directory")
#     '''
#     assert os.path.exists(at), "Specified path to store YAML file doesn't exist."
#
#     # Set the paths to the YAML file
#     file_path = os.path.join(at, f'{self.projectName}.yaml')
#
#     # If no file already exits, create one and fill it with the labels
#     if not os.path.exists(file_path):
#         with open(file_path, 'w') as f:
#             myDataYaml = {'path': "../train_data", "train": "images/train", "val": "images/val",
#                           "names": self.labelsIndex.copy()}
#             yaml.dump(myDataYaml, f, sort_keys=False)
#
#             print(f'{file_path} created.')
#     else:
#         print(f'{file_path} already exists.')