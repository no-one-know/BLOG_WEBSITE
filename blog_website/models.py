from blog_website import db
from flask import current_app
from datetime import datetime,timedelta
from flask_login import UserMixin
from authlib.jose import jwt

class Logininfo(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    rel=db.relationship("Personalinfo",backref="account",cascade="all, delete-orphan")

    def get_reset_token(self):
        header={
            'alg':'HS256'
        }
        expiration_time=datetime.utcnow()+timedelta(minutes=1)
        payload={
            'exp':expiration_time.isoformat(),
            'user_id':self.id
        }
        token=jwt.encode(header=header,key=current_app.config['SECRET_KEY'],payload=payload).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        try:
            decoded_token=jwt.decode(token,key=current_app.config['SECRET_KEY'])
        except:
            return None
        if (datetime.fromisoformat(decoded_token.get('exp')))<(datetime.utcnow()):
            return None
        user_id=decoded_token.get('user_id')
        return Logininfo.query.get(user_id)

    def __repr__(self) -> str:
        return f"LoginInfo('{self.id}','{self.username}','{self.email}')"

class Personalinfo(db.Model):
    user_id=db.Column(db.String(25),db.ForeignKey('logininfo.username', ondelete='CASCADE'),primary_key=True)
    firstname=db.Column(db.String(20),nullable=True,default="--N/A--")
    lastname=db.Column(db.String(20),nullable=True,default="--N/A--")
    dob=db.Column(db.Date,nullable=False,default=datetime.utcnow().date())
    gender=db.Column(db.String(20),nullable=True,default="--N/A--")
    country=db.Column(db.String(25),nullable=True,default="--N/A--")
    picture=db.Column(db.String(50),nullable=False,default="default.jpg")
    bio=db.Column(db.Text,nullable=True,default="--N/A--")
    rel=db.relationship("Post",backref="author",cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"PersonalInfo('{self.user_id}','{self.firstname}','{self.lastname}')"

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author_name=db.Column(db.String(25),db.ForeignKey('personalinfo.user_id', ondelete='CASCADE'))
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)

    def __repr__(self):
        return f"Post('{self.author_name}','{self.title}','{self.date_posted}')"