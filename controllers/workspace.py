import os
from flask import Flask,flash,render_template,redirect,request,url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from database import mongo_connection
from bson.objectid import ObjectId
import json
# import pymongo
# from pymongo import MongoClient

# from AI.controller.dataManager import ProjectManager
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}

db_connection = {
    "Users":mongo_connection.Users,
    "Projects":mongo_connection.Projects
}

Users = db_connection['Users']
Projects = db_connection['Projects']
print(Users.find_one())
print(Projects.find_one())


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To be changed to WorkspaceController
class workspaceController:
    project_name = ""
    def get_labels():
        # function to get labels that were entered by the user
        labels = []
        # Labels are stored in a file, once the form is submitted in the landing page
        with open('uploads\\files\\labels.txt','r') as label_file:
            labels.append(label_file.readline().strip().split(","))
        # the labels are returned to be used on the front end
        response = jsonify({"labels":labels[0]})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    def get_project_information():
        Project = Projects.find_one({})
        print(Project)
        response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size']})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
        print(response)
        return response

    def get_next_frames():
    #     Function to get the Next set of frames (to be annotated)
    #     Using the project_id we retieve it from the database, Directory_of_File\Frame_number loop * numberOfRetrievals
    #
        pass
    def get_old_frames():
    #     Function to get the previous set of frames or frame (That were already annotated even if skipped)
        pass
    # print(app.Project.find_one_or_404({"_id":"651aed7e0fa9d4b9db48be1b"}))


    def workspace():
        # checking if the request sent was a post request
        if request.method == "POST":
            # Checking whether a video was uploaded that satisfies the conditions was uploaded
            if 'video' not in request.files:
                flash("No file was uploaded, Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

            # Storing the video in a temporary variable for ease of use
            file = request.files['video']

            # Checking whether a video was selected that satisfies the conditions was uploaded
            if file.filename == '':
                flash("No selected file,Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))


            if file and allowed_file(file.filename):
                file_path = os.path.join('uploads/files', secure_filename(file.filename))
                file.save(file_path)

                project_name = request.form['project_name']
                # labels = request.form['labels'].split(",")
                # file_path = file_path
                # DM_obj = DataManager('',project_name)

                path = os.getcwd()
                # DM_obj.extractFrames(file_path,path+'/AI/train_data/images')

                # here is where the labels are stored in a file
                with open("./uploads/files/labels.txt",'w+') as label_file:
                    label_file.writelines(request.form['labels'])
                # returning the SPA page
                return send_from_directory(path+'/frontend/build/',"index.html")
                # return render_template("/views/workspace.html", filename=file.filename, labels=labels)
            else:
                flash("Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))




    def save_annotation():
        print(request.json)
        print("WRITINIASNPDINASD")
        response = jsonify({"data":request.json})
        response.headers.add('Access-Control-Allow-Origin', '*')
        with open('annotations.txt', 'w') as convert_file:
            convert_file.write(json.dumps(request.json))

        return response

    def retrieve_next_batch():
        # Because we are using file directories then we get all the files locations, but if GridFS then we check if portions
        # We can write the defaults if not present
        args = request.args
        startings_from = args.get('starting_from')
        retrievals_size =args.get('retrieval_size')
        print(startings_from,retrievals_size)

        Project = Projects.find_one({})
        image_dir = Project['Directory_of_File']
        # CHANGE IT TO CONTAIN ALL TYPES OF PHOTOS ALSO SAY THE TYPES IN REPORT
        for file in os.listdir(image_dir):
            if file.endswith(".jpg"):
                dir_list = '/images/'+ file
                break
        dir_list =  dir_list
        print(dir_list)
        # dir_list[0] = './'+ Project['Directory_of_File'] + dir_list[0]
        response = jsonify({"Project_Name": Project['Name'], "Frames": Project['Frames_Size'],"Image_Dir":dir_list})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def retrieve_previous_batch(starting_from=None, retrieval_size=10):
        Project = Projects.find_one({})
        image_dir = Project['Directory_of_File']
        for file in os.listdir(image_dir):
            # CHANGE IT TO CONTAIN ALL TYPES OF PHOTOS ALSO SAY THE TYPES IN REPORT
            if file.endswith(".jpg"):
                dir_list = file
                break
        dir_list = '/images/' + dir_list

        f = open("annotations.txt", "r")
        try:
            data_file = json.load(f)
        except json.JSONDecodeError:
            f.close()
            response = jsonify({ "Frames": Project['Frames_Size'], "Image_Dir": dir_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            with open('annotations.txt', 'w') as convert_file:
                convert_file.write('')




            response = jsonify({"Annotations": data_file, "Frames": Project['Frames_Size'], "Image_Dir": dir_list})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

    def insert_annotation_into_db(data):
        # MongoDB connection (where it's hosted), THIS NEEDS TO BE A GLOBAL VARIABLE
        client = MongoClient('mongodb://localhost:27017/')
        db = client['your_database']
        collection = db['annotations']

        # Define the schema
        schema = {
            'annotation_img': {'$type':'string'},   # the associated image name.
            'label_id': {'$type':'int'},    # the label numerical id.
            'x_center': {'$type': 'double'},   # the x-coord of the center of the bounding box, relative to the width of the image.
            'y_center': {'$type': 'double'},    # the y-coord of the center of the bounding box, relative to the height of the image.
            'width': {'$type': 'double'},       # the width of the bounding box, relative to the width of the image.
            'height': {'$type': 'double'},      # the height of the bounding box, relative to the height of the image.
        }

        # Create the validator using the schema
        validator = {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['annotation_img', 'label_id', 'x', 'y', 'width', 'height'],
                'properties': schema
            }
        }

        # Set the validator for the collection
        db.command({
            'collMod': 'annotations',
            'validator': validator
        })

        # Sample data to insert (where x and y should be floats)
        # data = {
        #     'annotation_img': "1233.PNG",
        #     'label_id': 4,
        #     'x': 0.345,
        #     'y': 0.55,
        #     'width': 0.20,
        #     'height': 0.35,
        # }
        try:
            result = collection.insert_one(data)
            print('Data inserted successfully.')
        except pymongo.errors.WriteError as e:
            print('Error: Data validation failed.')
            print('Validation Error:', e)


