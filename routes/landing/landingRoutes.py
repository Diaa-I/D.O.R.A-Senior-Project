import os
from flask import Flask, flash, render_template, redirect, request, url_for, Blueprint
from flask_pymongo import PyMongo, ObjectId
from controllers.landing import landingController


landing = Blueprint("landing", __name__)


landing.route("/",methods=['GET'])(landingController.rendering)




