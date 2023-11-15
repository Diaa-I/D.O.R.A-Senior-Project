from flask import Blueprint
from controllers.workspace import workspaceController

workspace = Blueprint("workspace", __name__)


# workspace.route("", methods=["POST"])(workspaceController.workspace)
workspace.route("/<project_id>/getlabels", methods=["GET"])(workspaceController.get_labels)
workspace.route("/<project_id>/trainmodel", methods=["GET"])(workspaceController.train_model)
workspace.route("/get_project_information/<project_id>", methods=["GET"])(workspaceController.get_project_information)
workspace.route("/retrieve_next_batch/<project_id>", methods=["GET"])(workspaceController.retrieve_next_batch)
workspace.route("/retrieve_previous_batch/<project_id>", methods=["GET"])(workspaceController.retrieve_previous_batch)
workspace.route("/save_annotation", methods=["POST"])(workspaceController.save_annotation)
workspace.route("/delete_annotation", methods=["POST"])(workspaceController.delete_annotation)
workspace.route("/trained_model/<project_id>", methods=["POST"])(workspaceController.trained_model)
workspace.route("/<project_id>/train_model", methods=["POST"])(workspaceController.train_model)
workspace.route("/<project_id>/check_training_process", methods=["GET"])(workspaceController.check_training_process)



