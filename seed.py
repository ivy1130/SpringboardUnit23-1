"""Seed file to make sample data for pets db."""

from models import User, db, Post, Tag
from app import app
from datetime import datetime

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
ivy = User(first_name = 'Ivy', last_name = 'Liu', img_url = 'https://images.theconversation.com/files/443350/original/file-20220131-15-1ndq1m6.jpg?ixlib=rb-1.1.0&rect=0%2C0%2C3354%2C2464&q=45&auto=format&w=926&fit=clip')
hannah = User(first_name = 'Hannah', last_name = 'Meacham')
sophie = User(first_name = 'Sophie', last_name = 'Lutz')

post = Post(title = 'first test post', content = 'I hope this is working', created_at = datetime.now(), user_id = 1)

tag = Tag(name = 'woo')

# Add new objects to session, so they'll persist
db.session.add_all([ivy, hannah, sophie])
db.session.add(post)
db.session.add(tag)

# Commit--otherwise, this never gets saved!
db.session.commit()