import os
from flask import Flask,flash,render_template,redirect,request,url_for

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
                labels = request.form['labels'].split(",")
                return render_template("/views/workspace.html", filename=file.filename, labels=labels)
            else:
                flash("Upload a video that satisfies the conditions")
                return redirect(url_for("landing.rendering"))
