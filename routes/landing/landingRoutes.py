import os
from flask import Flask, flash, render_template, redirect, request, url_for, Blueprint
from flask_pymongo import PyMongo, ObjectId
from controllers.landing import landingController

landing = Blueprint("landing", __name__)


landing.route("/",methods=['GET'])(landingController.rendering)



# > filepath of the video
# 	- I'll load the video, convert it into frames, save the frames into AI/train_data/images
#
# > name of the project
# 	- give me a string of the name of the project. I'll use this name as an identifier to many files created and managed by me.
#
# > array of labels
# 	- the array should be in the form of ['label1', 'label2', 'label3', 'label4', ... ] In this array each labels represents a class for example,
# 	if you're building a model to detect cats, dogs, and rocks, the label array will be ['cat', 'dog', 'rock'].

