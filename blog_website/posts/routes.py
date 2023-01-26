from flask import Blueprint

posts=Blueprint('posts',__name__)

from flask import render_template,redirect,flash,url_for,abort
from blog_website.models import Personalinfo,Logininfo,Post
from flask_login import current_user,login_required
from blog_website.posts.forms import post_form
from blog_website.users.forms import update_form,update_post_form
from blog_website.users.utils import save_picture
from blog_website import db

@posts.route("/create_post",methods=['get','post'])
@login_required
def create_post():
    form=post_form()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author_name=current_user.username)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!")
        return redirect(url_for('main.home',page_num=1))
    return render_template("create_post.html",title="New Post",form=form)


@posts.route("/post/<post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template("post.html",post=post)

@posts.route("/post/<post_id>/update",methods=['get','post'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author_name!=current_user.username:
        abort(403)
    form=update_post_form()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your post has been successfully updated!")
        return redirect(url_for('posts.post',post_id=post.id))
    form.title.data=post.title
    form.content.data=post.content
    return render_template("update_post.html",post=post,form=form)

@posts.route("/post/<post_id>/delete",methods=['get','post'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author_name!=current_user.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been successfully deleted!")
    return redirect(url_for('main.home',page_num=1))
