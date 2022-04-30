"""Blogly application."""
from crypt import methods
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ughhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.debug = True
debug = DebugToolbarExtension(app)
# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def index():
    """Redirects to list of users"""

    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/users/new')
def add_new_user():
    """Show form to add new users"""

    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def get_new_user():
    """Add new user to DB and return to list of users"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"] or None

    new_user = User(first_name = first_name, last_name = last_name, img_url = img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details of specific user by ID"""

    user = User.query.get_or_404(user_id)

    return render_template('user-details.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user_details(user_id):
    """Edit specific user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit-user-details.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_details(user_id):
    """Edit specific user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.img_url = request.form["img-url"] or None

    db.session.add(user)
    db.session.commit()
            
    return redirect('/users')

    # If I had the form fields blank, so that the current value would not be pre-filled in, how would I be able to only update the fields that had a change?

    # new_first_name = request.form["first-name"]
    # new_last_name = request.form["last-name"]
    # new_img_url = request.form["img-url"]

    # for new in [new_first_name, new_last_name, new_img_url]:
    #     if new:
                # update only the user.new items

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete specific user"""

    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')


