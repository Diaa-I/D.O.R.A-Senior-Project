from flask import Flask,flash,render_template,redirect,request,url_for,Blueprint
from controllers.workspace import workspaceController

workspace = Blueprint("workspace", __name__)


workspace.route("", methods=["POST"])(workspaceController.workspace)
workspace.route("/getlabels", methods=["GET"])(workspaceController.get_labels)
workspace.route("/get_project_information", methods=["GET"])(workspaceController.get_project_information)
workspace.route("/retrieve_next_batch", methods=["GET"])(workspaceController.retrieve_next_batch)
workspace.route("/retrieve_previous_batch", methods=["GET"])(workspaceController.retrieve_previous_batch)
workspace.route("/save_annotation", methods=["POST"])(workspaceController.save_annotation)



