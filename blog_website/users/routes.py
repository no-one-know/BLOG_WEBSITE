from flask import Blueprint

users=Blueprint('users',__name__)

from flask import render_template,redirect,request,url_for,flash,abort
import os
from flask_login import current_user,login_required,login_user,logout_user
from blog_website.models import Logininfo,Personalinfo,Post
from blog_website.users.forms import signin_form,signup_form,reset_password_form,forgot_password_form,update_form
from blog_website import bcrypt,db,login_manager
from blog_website.users.utils import send_reset_email,save_picture

@login_manager.user_loader 
def load_user(user_id):
    return Logininfo.query.get(int(user_id))

@users.route("/signin",methods=['post','get'])
def signin():
    form=signin_form()
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    if form.validate_on_submit():
        user=Logininfo.query.filter_by(email=form.email.data).first()
        if not user:
            flash("You have entered incorrect email address.Please try again!")
            return redirect(url_for('users.signin'))
        if not bcrypt.check_password_hash(user.password,form.password.data):
            flash("You have entered incorrect password.Please try again!")
            return redirect(url_for('users.signin'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for('main.home',page_num=1))
    return render_template("signin.html",title="SignIn",form=form)

@users.route("/signup",methods=['post','get'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    form=signup_form()
    if form.validate_on_submit():
        user=Logininfo.query.filter_by(username=form.username.data).first()
        if user:
            flash("This Username is taken.Please use different!")
            return redirect(url_for('users.signup'))
        user=Logininfo.query.filter_by(email=form.email.data).first()
        if user:
            flash("This Email is taken.Please use different!")
            return redirect(url_for('users.signup'))
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=Logininfo(username=form.username.data,email=form.email.data,password=hashed_password)
        user_info=Personalinfo(account=user)
        db.session.add(user)
        db.session.add(user_info)
        db.session.commit()
        flash("Your Account has been created successfully!Please Login to explore the world inside...")
        return redirect(url_for('main.success'))
    return render_template("signup.html",title="SignUp",form=form)

@users.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('users.signin'))

@users.route("/account")
@login_required
def account():
    current_profile=Personalinfo.query.get(current_user.username)
    image_file=url_for('static',filename='profile_pics/'+current_profile.picture)
    return render_template("account.html",title="Account",image_file=image_file,current_profile=current_profile)

@users.route("/user/<string:username>/<int:page>")
@login_required
def user_posts(username,page):
    posts=Post.query.filter_by(author_name=username).order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template("user_posts.html",title=username+" Posts",posts=posts,username=username)

@users.route("/forgot_password",methods=['get','post'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    form=forgot_password_form()
    if form.validate_on_submit():
        user=Logininfo.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Account with email "+form.email.data+" does not exist.Please create an account first.")
            return redirect(url_for('users.signup'))
        send_reset_email(user)
        flash("An mail has been sent to your email with instruction to reset your password.")
        return redirect(url_for('users.signin'))
    return render_template("forgot_password.html",title="Forgot Password",form=form)

@users.route("/reset_password/<token>",methods=['get','post'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home',page_num=1))
    user=Logininfo.verify_reset_token(token)
    if user is None:
        flash("The email sent is invalid or expired.")
        return redirect(url_for('users.forgot_password'))
    form=reset_password_form()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user.password=hashed_password
        db.session.commit()
        flash("Your password has been reset successfully! Sign in now...")
        return redirect(url_for('users.signin'))
    return render_template("reset_password.html",title="Reset Password",form=form,id=user.id)

@users.route("/update",methods=['get','post'])
@login_required
def update():
    current_profile=Personalinfo.query.filter_by(user_id=current_user.username).first()
    form=update_form()
    if form.validate_on_submit():
        if current_user.username==form.username.data:
            pass
        else:
            user=Logininfo.query.filter_by(username=form.username.data).first()
            if user:
                flash("This username is already taken!Choose different")
                return redirect(url_for('users.update'))
            else:
                items=Post.query.filter_by(author_name=current_user.username).all()
                for item in items:
                    item.author_name=form.username.data
                current_user.username=form.username.data
                current_profile.user_id=form.username.data
        
        if current_user.email==form.email.data:
            pass
        else:
            user=Logininfo.query.filter_by(email=form.email.data).first()
            if user:
                flash("This email is already taken!Choose different")
                return redirect(url_for('users.update'))
            else:
                current_user.email=form.email.data
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            if current_profile.picture!='default.jpg':
                file_path=os.getcwd()+"/blog_website/static/profile_pics/"+current_profile.picture
                if os.path.isfile(file_path):
                    os.remove(file_path)
            current_profile.picture=picture_file
        if form.firstname.data:
            current_profile.firstname=form.firstname.data
        else:
            current_profile.firstname="--N/A--"
        if form.lastname.data:
            current_profile.lastname=form.lastname.data
        else:
            current_profile.lastname="--N/A--"
        if form.country.data:
            current_profile.country=form.country.data
        else:
            current_profile.country="--N/A--"
        if form.bio.data:
            current_profile.bio=form.bio.data
        else:
            current_profile.bio="--N/A--"
        current_profile.dob=form.dob.data
        current_profile.gender=form.gender.data          
        db.session.commit()
        flash("Your account information has been updated successfully.","success")
        return redirect(url_for('users.account'))
    form.username.data=current_profile.user_id
    form.email.data=current_profile.account.email
    form.firstname.data=current_profile.firstname
    form.lastname.data=current_profile.lastname
    form.dob.data=current_profile.dob
    form.bio.data=current_profile.bio
    form.gender.data=current_profile.gender
    form.country.data=current_profile.country 
    return render_template("update_info.html",form=form,current_profile=current_profile)

@users.route("/delete_account/<int:id>",methods=['post'])
@login_required
def delete_account(id):
    user=Logininfo.query.get(id)
    info=Personalinfo.query.filter_by(user_id=user.username).first()
    pic=info.picture
    if pic!='default.jpg':
        file_path=os.getcwd()+"/blog_website/static/profile_pics/"+pic
        if os.path.isfile(file_path):
            os.remove(file_path)
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted permanently.SignUp to Continue...")
    return redirect(url_for('users.signup'))
