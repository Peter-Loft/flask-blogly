"""Seed file to make sample data for pets db."""

from models import db, User
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
whiskey = User(first_name='Whiskey', last_name="dog")
bowser = User(first_name='Bowser', last_name="dog", 
    image_url="https://pbs.twimg.com/profile_images/949787136030539782/LnRrYf6e_400x400.jpg")
spike = User(first_name='Spike', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()