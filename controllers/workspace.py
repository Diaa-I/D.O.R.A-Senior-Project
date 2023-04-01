import os
from flask import Flask,flash,render_template,redirect,request,url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class workspaceController:


    def workspace():
        if request.method == "GET":
            return "<h1>HEllo</h1>"
        if request.method == "POST":
            if 'video' not in request.files:
                flash("No file was uploaded, Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

            file = request.files['video']
            print(file)
            if file.filename == '':
                flash("No selected file,Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

            if file and allowed_file(file.filename):
                file_path = os.path.join('uploads/files', secure_filename(file.filename))
                file.save(file_path)
                # here they are anas
                project_name = request.form['project_name']
                labels = request.form['labels'].split(",")
                file_path = file_path

                return render_template("/views/workspace.html", filename=file.filename, labels=labels)
            else:
                flash("Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))

# > filepath of the video
# 	- I'll load the video, convert it into frames, save the frames into AI/train_data/images
#
# > name of the project
# 	- give me a string of the name of the project. I'll use this name as an identifier to many files created and managed by me.
#
# > array of labels
# 	- the array should be in the form of ['label1', 'label2', 'label3', 'label4', ... ] In this array each labels represents a class for example,
# 	if you're building a model to detect cats, dogs, and rocks, the label array will be ['cat', 'dog', 'rock'].
