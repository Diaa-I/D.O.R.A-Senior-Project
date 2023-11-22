import os
from flask import Flask,flash,render_template,redirect,request,url_for
from routes.landing.landingRoutes import landing
from routes.workspace.workspaceRoutes import workspace
from flask_cors import CORS

# Setup
class Service:
    def __init__(self):
        # Constructor
        self.__template_dir = os.path.abspath(os.getcwd())
        self.__static_dir = self.__template_dir
        self.__uploaded_folder = '/uploads/files/'
        self.app = self.setup()

    def setup(self):
        # setting up and configuring the flask
        self.app = Flask(__name__,template_folder=self.__template_dir, static_url_path='',static_folder=self.__static_dir)
        self.app.config['UPLOAD_FOLDER'] = self.__uploaded_folder
        # app.config['CORS_HEADERS'] = 'Content-Type'
        # cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
        self.app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        return self.app


service = Service()
app = service.app
CORS(app)

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