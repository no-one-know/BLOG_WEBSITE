import os
path='sqlite:///'+os.getcwd()

class Config:
    SECRET_KEY='0c0fa473989cd4d32b4d392bad1b28'
    WTF_CSRF_SECRET_KEY = '1c9fa173969ct4d32r4d392bad1b69'
    SQLALCHEMY_DATABASE_URI=os.path.join(path,'database.db')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')