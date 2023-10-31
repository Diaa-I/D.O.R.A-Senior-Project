import cv2
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
from database import mongo_connection
import bson.json_util as json_util
from flask_pymongo import ObjectId
from werkzeug.utils import secure_filename
import os, yaml , json
db_connection = {
    "Users":mongo_connection.Users,
    "Projects":mongo_connection.Projects,
    "Annotations":mongo_connection.Annotations
}

Users = db_connection['Users']
Projects = db_connection['Projects']
Annotations = db_connection['Annotations']

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}
def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def extract_frames(video_filepath, output_dir, Project) -> None:
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
        all_frames_paths = []
        # Open the video file
        cap = cv2.VideoCapture(video_filepath)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Initialize the frame count and loop over all frames
        total_project_images = 0
        count_init = total_project_images
        print(video_filepath, output_dir, Project['Name'],count_init)
        print(os.getcwd())
        print(os.path.exists(video_filepath))
        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Construct the output file path and save the frame as a JPG file
            output_path = os.path.join(output_dir, f"{total_project_images}_{Project['Name']}.jpg") # EDIT projName to a class attribute
            if not os.path.exists(output_path):
                cv2.imwrite(output_path, frame)
                all_frames_paths.append(output_path)
            else:
                print(f"{output_path} already exists")

            # Increment the frame count
            total_project_images += 1
        Projects.update_one({"_id":ObjectId(Project['_id'])}, {"$set": {"Directory_of_File": output_dir, "Frames_Size": total_project_images - count_init}})
        print(f"Extracted {total_project_images - count_init} frames from {video_filepath}")
        # Release the video capture object
        cap.release()


class landingController:
    def all_projects():
        all_projects = []
        for project in Projects.find():
            all_projects.append(json.loads(json_util.dumps(project)))
        response = jsonify({"Projects":all_projects})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def upload_video(project_name):
        Project = Projects.find_one({"Name":project_name})
        print(Project)
        # Checking whether a video was uploaded that satisfies the conditions was uploaded
        print(request.files)
        print(request.files['video'])
        if 'video' not in request.files:
            flash("No file was uploaded, Upload a video that satisfies the conditions")
            return "NO"
            # return redirect(url_for("landing.rendering"))

        # Storing the video in a temporary variable for ease of use
        file = request.files['video']

        # Checking whether a video was selected that satisfies the conditions was uploaded
        if file.filename == '':
            flash("No selected file,Upload a video that satisfies the conditions")
            return "NOT DONE"
        if file and allowed_file(file.filename):
            os.mkdir(f'frontend/public/images/{Project["Name"]}')
            os.mkdir(f'frontend/public/images/{Project["Name"]}/video')
            file_path = os.path.join(f'frontend/public/images/{Project["Name"]}/video', secure_filename(file.filename))
            file.save(file_path)
            extract_frames(file_path,f'frontend/public/images/{Project["Name"]}', Project)
            return "DONE"
        else:
            flash("Upload a video that satisfies the conditions")
            return 'NO'
            # return redirect(url_for("landing.rendering"))

    def create_project():
        # model_path, yaml_path
        # name, frames_size, directory_of_file (img), labels
    #-----------------------------------------------------------
        # Images uploaded into two places, training and public for displaying
        # Create folder for each project in public/images/Filename , without spaces in filename
        # Make model + yaml files
        # Make a new record in Projects Collection
        # Calculate how many frames



        # Images (Dataset) add them to two places, public images and in AI/train_data/images
        # checking if the request sent was a post request
        if request.method == "POST":

            # Make Model and YAML files
            newProject = request.json['project']
            print(newProject)
            index_to_labels = {i: newProject['labels'][i] for i in range(len(newProject['labels']))}
            file_path_yaml = os.path.join('AI/yolov5m/data/', f'{newProject["name"]}.yaml')
            print(file_path_yaml)

            # If no file already exits, create one and fill it with the labels
            if not os.path.exists(file_path_yaml):
                with open(file_path_yaml, 'w+') as f:
                    myDataYaml = {'path': "../train_data", "train": "images/train", "val": "images/val",
                                  "names": index_to_labels.copy()}
                    yaml.dump(myDataYaml, f, sort_keys=False)

                    print(f'{file_path_yaml} created.')
            else:
                print(f'{file_path_yaml} already exists.')

            # Data from web app to add DB
            # Calculate how many frames, later compare how many written in frames size and how many files
            project_obj = {
                "Name": newProject['name'],
                "Frames_Size": '',
                "Directory_of_File": '',
                "Labels": newProject['labels'].split(','),
                "model_filepath": "AI/yolov5m/runs/train/exp4/weights/best.pt",
                "yaml_filepath": file_path_yaml,
            }
            # Add to Database
            Projects.insert_one(project_obj)
            return project_obj['Name']



    def rendering():
        return render_template("/views/landing.html")

# landingController.a()