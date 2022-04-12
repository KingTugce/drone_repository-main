from flask import Blueprint, render_template
from flask_login import login_required

"""
Note that in the above code some arfs are speced the Blueprint object
The first arg, 'site' is the Blueprint's name,
which is used by Flask's routing mechanism.
The second arg is __name__, is the Blueprint's import name,
which Flask uses to locate the Blueprint's resource
"""

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/') 
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

#--------routes below----------

@site.route('/about')
def about():
    return 'The About Page - COMMING SOON!!'

@site.route('/blog')
def blog():
    return '<h1> Here is the future Blog page! <h1>'

@site.route('/blog/<string:blog_id>')
def blogpost(blog_id):
    return 'This is blog post number: ' + blog_id

#-------- user names ----------
@site.route('/user/<string:user_name>')
def user_name(user_name):
    return render_template('user.html', user_name=user_name)

@site.route('/allusers')  # path on the web browser
def all_users():
    all_users = ['kevin', 'alex', 'bob', 'atila']
    return render_template('all_users.html', all_users=all_users) # path in working files