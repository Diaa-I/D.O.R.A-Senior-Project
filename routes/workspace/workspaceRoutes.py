import os
from flask import Flask,flash,render_template,redirect,request,url_for,Blueprint
from flask_pymongo import PyMongo, ObjectId
from controllers.workspace import workspaceController

workspace = Blueprint("workspace", __name__)


workspace.route("", methods=["POST"])(workspaceController.workspace)
workspace.route("/getlabels", methods=["GET"])(workspaceController.get_labels)



