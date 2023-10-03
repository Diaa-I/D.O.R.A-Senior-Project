import os
from flask import Flask,flash,render_template,redirect,request,url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from database import mongo_connection
from bson.objectid import ObjectId
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
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With");
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


