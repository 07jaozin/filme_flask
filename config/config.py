# config.py
import os
import datetime

BASE_DIR = os.getcwd()

class Config:
    UPLOAD_FOLDER = 'static/img'
    UPLOAD_VIDEO = 'static/video'
    SECRET_KEY = 'curso_flask'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=900000)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'joaovictorvalentim.m@gmail.com'
    MAIL_PASSWORD = 'wxvi hzwz xmmu odaj'  # App Password
    MAIL_DEFAULT_SENDER = 'jvt.oliveira@gmail.com'
    
