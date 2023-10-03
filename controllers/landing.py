from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
from database import mongo_connection

db_connection = {
    "Users": mongo_connection.Users,
    "Projects": mongo_connection.Projects
}

Users = db_connection['Users']
Projects = db_connection['Projects']


class landingController:
    def a():
        Project = Projects.find_one({})
        print(Project)
        response = jsonify({"Project_Name":Project['Name'],"Frames":Project['Frames_Size']})
        response.headers.add('Access-Control-Allow-Origin', '*')
        print(response)
        return response
        # return render_template("/views/index.html")

    def rendering():
        return render_template("/views/landing.html")

# landingController.a()