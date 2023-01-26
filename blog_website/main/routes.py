from flask import Blueprint

main=Blueprint('main',__name__)

from flask import render_template,redirect,url_for
from flask_login import current_user,login_required
from blog_website.models import Post

@main.route("/")
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    return render_template("index.html",title="Welcome")

@main.route("/success")
def success():
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    return render_template("greeting.html",title="Success")

@main.route("/home/<int:page_num>")
@login_required
def home(page_num):
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page_num)
    return render_template("home.html",title="Home",posts=posts)