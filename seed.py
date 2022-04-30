"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
ivy = User(first_name = 'Ivy', last_name = 'Liu')
hannah = User(first_name = 'Hannah', last_name = 'Meacham')
sophie = User(first_name = 'Sophie', last_name = 'Lutz')

# Add new objects to session, so they'll persist
db.session.add(ivy)
db.session.add(hannah)
db.session.add(sophie)

# Commit--otherwise, this never gets saved!
db.session.commit()