# config.py
import os
import datetime

BASE_DIR = os.getcwd()

class Config:
    UPLOAD_FOLDER = 'static/img'
    UPLOAD_VIDEO = 'static/video'
    SECRET_KEY = 'curso_flask'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=900000)
