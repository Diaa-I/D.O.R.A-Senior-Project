import os
from flask import Flask,flash,render_template,redirect,request,url_for
from flask_pymongo import PyMongo, ObjectId
from models.annotation_class import Annotation
from models.file_class import File
from routes.landing.landingRoutes import landing
from routes.workspace.workspaceRoutes import workspace

# Setup
class Service:
    def __init__(self):
        # Constructor
        self.__template_dir = os.path.abspath(os.getcwd())
        self.__static_dir = self.__template_dir
        self.__uploaded_folder = '/uploads/files/'
        self.app = self.setup()
# 0        self.mongo = self.connectToDB()

    def connectToDB(self):
        # connection to db via PyMongo
        self.mongo = PyMongo(self.app, uri="mongodb://localhost:27017/DORA")
        return self.mongo

    def setup(self):
        # setting up and configuring the flask
        self.app = Flask(__name__,template_folder=self.__template_dir, static_url_path='',static_folder=self.__static_dir)
        self.app.config['UPLOAD_FOLDER'] = self.__uploaded_folder
        self.app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        return self.app


service = Service()
app = service.app


# # Routes to annotations
# app.register_blueprint(landing, url_prefix='/annotations')
# Routes to workspace
app.register_blueprint(workspace, url_prefix='/workspace')
# Routes to landing page
app.register_blueprint(landing, url_prefix='/')



# Error handling class
# --------------------------------------------------------
# Error Handling



if __name__=="__main__":
    app.run(debug=True,threaded=True)