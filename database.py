# from flask_pymongo import PyMongo, ObjectId
import pymongo
# class Configs:
#     db_connection = ''
#     def __init__(self,app):
#         Configs.db_connection = self.connectToDB(app)
#     def connectToDB(self,app):
#         # connection to db via PyMongo
#         # Later every user will have his own id to use the API with
#         # and this will be called from somewhere else
#         return PyMongo(app, uri="mongodb://localhost:27017/DORA").db
#
#     def get_connection(self):
#         return Configs.db_connection
mongo_connection = pymongo.MongoClient(host="mongodb://localhost:27017/")['DORA']
