import os
from flask import Flask, flash, render_template, redirect, request, url_for, Blueprint
from flask_pymongo import PyMongo, ObjectId
from controllers.landing import landingController


landing = Blueprint("landing", __name__)


landing.route("/",methods=['POST'])(landingController.rendering)
landing.route("/all_projects",methods=['GET'])(landingController.all_projects)
landing.route("/delete_project/<project_id>",methods=['GET'])(landingController.delete_project)
landing.route("/create_project",methods=['POST'])(landingController.create_project)
landing.route("/upload_video/<project_name>",methods=['POST'])(landingController.upload_video)



