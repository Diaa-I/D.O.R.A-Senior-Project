import os
import subprocess
import sys
from natsort import natsorted
import cv2
import numpy as np
import yaml
from flask import Flask,flash,render_template,redirect,request,url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

# from AI.yolov5m.models.common import DetectMultiBackend
import test_processing
from database import mongo_connection
from flask_pymongo import ObjectId
import AI.controller.modelController as mc
import AI.controller.projectManager as pm

import json
# import pymongo
# from pymongo import MongoClient

# from AI.controller.dataManager import ProjectManager
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}

db_connection = {
    "Users":mongo_connection.Users,
    "Projects":mongo_connection.Projects,
    "Annotations":mongo_connection.Annotations
}

Users = db_connection['Users']
Projects = db_connection['Projects']
Annotations = db_connection['Annotations']

project_currently_used = {"_id":""}

def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To be changed to WorkspaceController
class workspaceController:
    project_name = ""
    def get_labels(project_id):
        # function to get labels that were entered by the user
        labels = []
        # Labels are stored in the DB record, once the form is submitted in the landing page
        Project = Projects.find_one({"_id":ObjectId(project_id)})
        # the labels are returned to be used on the front end
        response = jsonify({"labels":Project['Labels']})

        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    def get_project_information(project_id):
        # Return the project details
        project_currently_used['_id'] = ObjectId(project_id)
        Project = Projects.find_one({"_id":ObjectId(project_id)})
        print(Project)
        response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size']})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
        return response

    # I THINK NO LONGER BEING USED
    # def workspace():
    #     # checking if the request sent was a post request
    #     if request.method == "POST":
    #         # Checking whether a video was uploaded that satisfies the conditions was uploaded
    #         if 'video' not in request.files:
    #             flash("No file was uploaded, Upload a video that satisfies the conditions")
    #             return redirect(url_for("landing.rendering"))
    #
    #         # Storing the video in a temporary variable for ease of use
    #         file = request.files['video']
    #
    #         # Checking whether a video was selected that satisfies the conditions was uploaded
    #         if file.filename == '':
    #             flash("No selected file,Upload a video that satisfies the conditions")
    #             return redirect(url_for("landing.rendering"))
    #
    #
    #         if file and allowed_file(file.filename):
    #             file_path = os.path.join('uploads/files', secure_filename(file.filename))
    #             file.save(file_path)
    #
    #             project_name = request.form['project_name']
    #             path = os.getcwd()
    #
    #             # here is where the labels are stored in a file
    #             with open("./uploads/files/labels.txt",'w+') as label_file:
    #                 label_file.writelines(request.form['labels'])
    #             # returning the SPA page
    #             return send_from_directory(path+'/frontend/build/',"index.html")
    #             # return render_template("/views/workspace.html", filename=file.filename, labels=labels)
    #         else:
    #             flash("Upload a video that satisfies the conditions")
    #             return redirect(url_for("landing.rendering"))


    def delete_annotation():
        # Annotations from web
        annotation_arr = request.json['Annotations']

        # Frame number
        frameNumber = request.json['frameNumber']

        # Project id from web app
        project_id = ObjectId(request.json['project_id'])

        # Annotations from Database
        frameAnnotation = list(Annotations.find({"frame":frameNumber,'project_id':project_id}))
        # Existing Annotations from database
        # existing_annotations = [i for i in annotation_arr if i in frameAnnotation]
        #
        # # Finding the annotations to delete using the annotations in database
        # delete_annotations = [annotation for annotation in frameAnnotation if annotation not in existing_annotations]
        # print(delete_annotations)
        # Delete Annotations
        if len(frameAnnotation)>0:
            for annotation in frameAnnotation:
                Annotations.delete_many({"_id":annotation["_id"]})
        return "Hello"


    def save_annotation():
        # Annotations from web app
        annotation = request.json['Annotations']

        # Project id from web app
        project_id = ObjectId(request.json['project_id'])

        # Annotations from database
        allAnnotations = list(Annotations.find({"frame": request.json['frameNumber'],"project_id":project_id}, {'_id': False,'frame':False,'project_id':False}))

        # Finding all the existing annotations from database, ones that haven't been modified on web
        existing_annotations = [i for i in annotation if i in allAnnotations]

        # Finding the annotations to delete using the annotations in database
        delete_annotations = [annotation for annotation in allAnnotations if annotation not in existing_annotations]

        # Finding annotations to add using the annotations not found to be existing in the database be were sent with web request
        add_annotations = [i for i in annotation if i not in existing_annotations]

        # Modifying all the new annotations to be similar to ones that exist
        for i in range(len(add_annotations)):
             add_annotations[i]= {
                 "frame": request.json['frameNumber'],
                 "label": add_annotations[i]['label'],
                 "x": add_annotations[i]['x'],
                 "y": add_annotations[i]['y'],
                 "width": add_annotations[i]['width'],
                 "height": add_annotations[i]['height'],
                 "project_id":project_id
                 }

        response = jsonify({"data": "Successfully modified the database"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        # Adding all new annotations
        if len(add_annotations) > 0:
            Annotations.insert_many(add_annotations)
        # Removing annotations that no longer exist
        if len(delete_annotations)>0:
            for anno in delete_annotations:
                # (WE CANT USE ID WE ARE NOT REQUESTING ID DUE TO  COMPARING)
                Annotations.delete_many({"x":anno['x'],'y':anno['y'],'height':anno['height'],'width':anno['width'],"project_id":project_id})
        return response

    def retrieve_next_batch(project_id):
        # Because we are using file directories then we get all the files locations, but if GridFS then we check if portions
        # We can write the defaults if not present
        print(project_id)
        args = request.args

        Project = Projects.find_one({"_id":ObjectId(project_id)})
        dir_list = []
        image_dir = Project['Directory_of_File']
        # To open the images on frontend it will already be in /public
        opening_dir = Project['Directory_of_File'].split('/')[2:]
        opening_dir = '/'+'/'.join(opening_dir)
        files_sorted = []
        # Sort the files using natsort which uses decimal because normal sorted returns it wrong
        for file in os.listdir(image_dir):
            files_sorted.append(file)
        files_sorted = natsorted(files_sorted)
        # CHANGE IT TO CONTAIN ALL TYPES OF PHOTOS ALSO SAY THE TYPES IN REPORT
        # Should later change to accessing from database the frames
        # use the sorted file list to return the actual frame ordered properly
        for file in files_sorted:
            if file.endswith(".jpg"):
                # print(file)
                # Extract the width and height of images
                # im = cv2.imread(os.getcwd() + '/' + image_dir + f'/{file}')
                # print({'width': im.shape[1], 'height': im.shape[0]})
                # Image location + Metadata
                # dir_list.append({"image_loc": opening_dir + f'/{file}', 'width': im.shape[1], 'height': im.shape[0]})
                dir_list.append({"image_loc": opening_dir + f'/{file}', 'width': Project['Dimensions']['width'], 'height': Project['Dimensions']['height']})
        # dir_list[0] = './'+ Project['Directory_of_File'] + dir_list[0]
        # print(dir_list.sort(key='image_loc'))
        # print(dir_list.sort(key='image_loc'))
        # print(dir_list.items())
        # print(sorted(dir_list, key=lambda item: item['image_loc']))

        response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size'],"Image_Dir":dir_list})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    def retrieve_previous_batch(project_id):
        args = request.args
        frame_number = int(args.get('frameNumber'))
        print(ObjectId(project_id))
        allAnnotations = list(Annotations.find({"frame":frame_number,"project_id":ObjectId(project_id)}, {'_id': False, "frame": False,'project_id':False}))
        print(allAnnotations)
        response = jsonify({"Annotations": allAnnotations})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    def train_model(project_id):
        Project = Projects.find_one({"_id": ObjectId(project_id)})
        annotated_frames = request.json['annotatedFrames']
        annotations = Annotations.find({"project_id":project_id})
        # Check if already training by checking if isTraining == false or isTraining == a number
        if Project['isTraining'] == False:
            # If not training then take all the frames ( the question is which frames ) and annotations related to
            # those frames and do createAnnotaions function
            # Maybe trained frames should be in DB
            # already they is an array called annotatedFrames, so we take that and check which one has already been
            # trained and don't train those
            # anytime you want to exit workspace save them to DB or no need just save the trained frames (second yes)
            # Get frames that are annotated and get their annotations, then pass to createAnnotation_txt
            annotatedFrames = request.json['annotatedFrames']
            # Get the annotations related to only frames that were annotated
            all_annotations = list(Annotations.find(
                {"project_id": ObjectId("6544fb62801230ccdc4d166c"), "frame": {"$in": annotatedFrames}},
                {'_id': False, 'project_id': False}))
            # response = jsonify({"Annotations": json.loads(json_util.dumps(all_annotations))})

            # Set doesn't allow duplications, give me all the frame numbers that were annotated with no duplicates
            frames_annotated = {annotation['frame'] for annotation in all_annotations}

            # after knowing the frames that were annotated, now I want a dictionary containing the frame numbers as a parent
            array_of_annotations = {}
            for frames in frames_annotated:
                array_of_annotations[frames] = []


            # the children are an array of annotations in that specific frame, parent is commented above which is frame number
            for annotation in all_annotations:
                array_of_annotations[annotation['frame']].append(annotation)
            # for each frame create txt file for annotations using the create_annotations_txt function
            for frame_num in frames_annotated:
                image_name = f"{frame_num}_test.jpg"
                pm.create_annotations_txt(Project['yaml_filepath'], image_name, Project['Dimensions']['width'],
                                          Project['Dimensions']['height'], array_of_annotations[frame_num],
                                          'AI/train_data/labels/train')

            #           Dimensions are added already
        #           Project['Dimensions']['width'],Project['Dimensions']['height']
        #           now retrieval of annotations + where to save the file
        #           Also now we need to pick where to save the model

            mc.ModelController().train_model(Project['yaml_filepath'], Project['model_filepath'], img_train_size=320)
            DETACHED_PROCESS = 0x00000008
            pid = subprocess.Popen([sys.executable, "test_processing.py", Project['yaml_filepath'], Project['model_filepath'], "320"],
                                                          creationflags=DETACHED_PROCESS).pid
            return True
            pass
        else:
            # Return that it is already being trained
            # when that happens then add how many needs to be trained
            # Maybe when done training send the annotatedFrames and it will do training
            return False
            pass

        test_processing.start_training(Project['yaml_filepath'],Project['model_filepath'] ,img_train_size=320)
        return 'Done'


    def trained_model(project_id):
        # Find project, In DB project <-> model, so we can have relation which project relies on model.
        Project = Projects.find_one({"_id": ObjectId(project_id)})
        print(Project)
        print(request.json['currentFrame'])
        print((Project['Dimensions']['width'],Project['Dimensions']['height']))
        # Make prediction
        predictions = mc.ModelController().make_inference("frontend/public/"+request.json['currentFrame'], Project['yaml_filepath'],Project['model_filepath'],normalization_dims=(Project['Dimensions']['width'],Project['Dimensions']['height']))
        print(predictions)
        #
        pred = []
        for prediction in predictions:
            # x = (x_min + x_max)/2, y = (y_min + y_max)/2
            # w = x_max - x_min, h = y_max - y_min
            print("----------------------------------")
            print(prediction)
            x_min = prediction['location'][0]
            y_min = prediction['location'][1]
            x_max = prediction['location'][2]
            y_max = prediction['location'][3]
            pred.append({
                'x':x_min,
                'y':y_min,
                'w':(x_max - x_min),
                'h':(y_max - y_min),
                'label':prediction['name'],
                'conf_score': prediction['conf_score']
            })
        print(pred)
        # If not prediction then return a flash message saying there were no prediction found
        return pred


# Function to return first frame