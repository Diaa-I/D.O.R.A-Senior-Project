from flask import Blueprint
from controllers.landing import landingController


landing = Blueprint("landing", __name__)


landing.route("/",methods=['GET'])(landingController.rendering)
landing.route("/all_projects",methods=['GET'])(landingController.all_projects)
landing.route("/delete_project/<project_id>",methods=['GET'])(landingController.delete_project)
landing.route("/create_project",methods=['POST'])(landingController.create_project)
landing.route("/upload_video/<project_name>",methods=['POST'])(landingController.upload_video)



