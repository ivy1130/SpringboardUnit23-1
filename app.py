"""Blogly application."""
from crypt import methods
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

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
def show_new_user_form():
    """Show form to add new users"""

    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
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
    posts = db.session.query(Post.id, Post.title).filter_by(user_id = user_id).all()

    return render_template('user-details.html', user = user, posts = posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show form to edit user information"""

    user = User.query.get_or_404(user_id)

    return render_template('edit-user-details.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_details(user_id):
    """Update user details from edits"""

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

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show new post form"""
    user = User.query.get_or_404(user_id)

    return render_template('new-post.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Add new post to DB and redirect to user details"""
    # user = User.query.get_or_404(user_id)

    title = request.form["post-title"]
    content = request.form["post-content"]

    new_post = Post(title = title, content = content, created_at = datetime.now(), user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post"""
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post = post, user = post.user)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post = post, user = post.user)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Update post based on edits"""
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form["post-title"]
    post.content = request.form["post-content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete specific post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')