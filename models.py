"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                    nullable=False)

    last_name = db.Column(db.String(50),
                    nullable=False)

    img_url = db.Column(db.Text)

    posts = db.relationship('Post', backref = 'user', cascade='all, delete-orphan')

    def __repr__(self):
        u = self
        return f"<User id = {u.id} First Name = {u.first_name} Last Name = {u.last_name} Img URL = {u.img_url}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                    nullable = False)
    
    
    content = db.Column(db.Text,
                    nullable = False)
    
    created_at = db.Column(db.DateTime,
                    nullable = False)
    
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'), 
                    nullable = False)
    
    tags = db.relationship(
        'Tag', secondary="post_tags", backref="posts")

    def __repr__(self):
        p = self
        return f"<Post id = {p.id} Title = {p.title} Content = {p.content} Created at = {p.created_at} User id = {p.user_id}>"

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text,
                    unique = True,
                    nullable = False)
    
    def __repr__(self):
        t = self
        return f"<Tag id = {t.id} Name = {t.name}>"

    post_tags = db.relationship('PostTag', cascade = 'all, delete-orphan')

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)