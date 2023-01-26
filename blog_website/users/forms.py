from flask_wtf import FlaskForm
import os
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,EmailField,BooleanField,DateField,TextAreaField,SelectField
from wtforms.validators import DataRequired,EqualTo,Email,ValidationError
from blog_website.models import Logininfo,Personalinfo
from flask import redirect,flash,url_for

class signup_form(FlaskForm):
    username=StringField('Username',validators=[DataRequired()],render_kw={"placeholder":"Username"})
    email=EmailField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    password=PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Password"})
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder":"Confirm Password"})
    submit=SubmitField('Sign Up')

class signin_form(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()],render_kw={"placeholder":"Email"})
    password=PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Password"})
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign In')

class update_form(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=EmailField('Email',validators=[DataRequired(),Email()])
    firstname=StringField('Firstname')
    lastname=StringField('Lastname')
    gender=SelectField('Gender',choices=['Male','Female','Not Disclosed'])
    dob=DateField('DOB')
    country=StringField('Country')
    bio=TextAreaField('Bio')
    picture=FileField('Upload Profile Picture',validators=[FileAllowed(['jpg','png','jpeg','gif','bmp'])])
    submit=SubmitField('Commit Updates') 

class update_post_form(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Update Post')

class forgot_password_form(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Get reset link')

class reset_password_form(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset Password')
