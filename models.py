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

    posts = db.relationship('Post', cascade="all, delete")

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
    
    user = db.relationship('User')
    # user = db.relationship('User', backref = 'posts')

    def __repr__(self):
        p = self
        return f"<Post id = {p.id} Title = {p.title} Content = {p.content} Created at = {p.created_at}> User id = {p.user_id}"