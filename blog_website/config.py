import os
from decouple import config

path='sqlite:///'+os.getcwd()

class Config:
    SECRET_KEY=config('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = config('WTF_CSRF_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.path.join(path,'database.db')
    MAIL_SERVER=config('MAIL_SERVER')
    MAIL_PORT=config('MAIL_PORT',cast=int)
    MAIL_USE_TLS=config('MAIL_USE_TLS',cast=bool)
    MAIL_USERNAME=config('MAIL_USERNAME')
    MAIL_PASSWORD=config('MAIL_PASSWORD')