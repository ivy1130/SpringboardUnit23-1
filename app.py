"""Blogly application."""
from crypt import methods
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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

##############################################################################
# USERS ROUTE

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('user-list.html', users = users)

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
    # posts = db.session.query(Post.id, Post.title).filter_by(user_id = user_id).all()

    return render_template('user-details.html', user = user, posts = user.posts)

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

##############################################################################
# POSTS ROUTE

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new-post.html', user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Add new post to DB and redirect to user details"""
    title = request.form["post-title"]
    content = request.form["post-content"]
    tag_ids = request.form.getlist("tags")

    new_post = Post(title = title, content = content, created_at = datetime.now(), user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        new_post.tags.append(tag)
    
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post"""
    post = Post.query.get_or_404(post_id)

    return render_template('post-details.html', post = post, user = post.user, tags = post.tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit-post-details.html', post = post, user = post.user, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Update post based on edits"""
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form["post-title"]
    post.content = request.form["post-content"]
    post.tags.clear()
    tag_ids = request.form.getlist("tags")

    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        post.tags.append(tag)

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

##############################################################################
# TAGS ROUTE

@app.route('/tags')
def show_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()

    return render_template('tag-list.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-details.html', tag = tag, posts = tag.posts)

@app.route('/tags/new')
def show_new_tag_form():
    """Show form to add new tags"""

    return render_template('new-tag.html')

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    """Process add form, adds tag, and redirect to tag list."""
    name = request.form["tag-name"]

    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag-details.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_details(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["tag-name"]

    db.session.add(tag)
    db.session.commit()
            
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')