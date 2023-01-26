# BLOG_WEBSITE
This is a blogging website made using python flask framework. The website provides the functionality of <b>SignUP</b> for new users and <b>SignIn</b> for the existing users. Once you are logged in, the user can <b>Create Post</b>, <b>Update Post</b>, <b>Update Account Info</b>, <b>Delete Post</b>, <b>Delete Account</b>.

If you clone this website then for creating database use the following command:-
<ol>
  <li>from blog_website import create_app,db</li>
  <li>app=create_app()</li>
  <li>app.app_context().push()</li>
  <li>db.create_all()</li>
</ol>

Following is the list and link of technologies used while creating application:-
<ul>
  <li><a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a></li>
  <li><a href="https://docs.sqlalchemy.org/en/14/">Sqlalchemy</a></li>
  <li>Sqlite Database</li>
  <li><a href="https://jinja.palletsprojects.com/en/3.1.x/">Jinja Templating</a></li>
  <li><a href="https://wtforms.readthedocs.io/en/3.0.x/">WTForms</a></li>
  <li>HTML</li>
  <li>CSS</li>
  <li>Bootstrap classes</li>
  <li><a href="https://flask-login.readthedocs.io/en/latest/">Flask-login </a>for managing user sessions</li>
  <li><a href="https://pythonhosted.org/Flask-Mail/">Flak-Mail </a>for sending reset password links</li>
  <li><a href="https://docs.authlib.org/en/latest/">Authlib </a>library for generating authentication token</li>
</ul>
