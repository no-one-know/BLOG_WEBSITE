from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blog_website.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.signin'
login_manager.login_message_category='info'
mail=Mail()

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from blog_website.users.routes import users
    from blog_website.posts.routes import posts
    from blog_website.main.routes import main
    from blog_website.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
