import requests
import os
from flask import Flask,flash,render_template,redirect,request,url_for
from flask_pymongo import PyMongo, ObjectId
# Setup
class Service:
    def __init__(self):
        # Constructor
        self.__template_dir = os.path.abspath(os.getcwd())
        self.__static_dir = self.__template_dir + "/public/"
        self.__uploaded_folder = '/upload/files/'
        self.app = self.setup()
        self.mongo = self.connectToDB()

    def connectToDB(self):
        # connection to db via PyMongo
        self.mongo = PyMongo(self.app, uri="mongodb://localhost:27017/movies-flask")
        return self.mongo

    def setup(self):
        # setting up and configuring the flask
        self.app = Flask(__name__,template_folder=self.__template_dir, static_url_path='',static_folder=self.__static_dir)
        self.app.config['UPLOAD_FOLDER'] = self.__uploaded_folder
        self.app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        return self.app


service = Service()
app = service.app
mongo = service.mongo


ALLOWED_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'avi', 'mkv', 'webm'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def rendering():
    return render_template("/views/landing.html")


@app.route("/workspace",methods=["GET","POST"])
def workspace():
    if request.method == "POST":
        print("Hello")

        if 'video' not in request.files:
            flash("No file was uploaded, Upload a video that satisfies the conditions")
            return redirect(url_for("rendering"))
        file = request.files['video']

        if file.filename == '':
            flash("No selected file,Upload a video that satisfies the conditions")
            return redirect(url_for("rendering"))

        if file and allowed_file(file.filename):
            print(file)
        else:
            flash("Upload a video that satisfies the conditions")
            return redirect(url_for("rendering"))

    return render_template("/views/workspace.html")


if __name__=="__main__":
    app.run(debug=True)