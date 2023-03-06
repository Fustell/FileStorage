import os

SECRET_KEY = os.getenv("SECRET_KEY","undefined")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI","undefined")
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER","usersFiles")
