"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
# db.create_all()

@app.get("/")
def homepage():
    return redirect("/users")

@app.get("/users")
def users_list():
    return render_template("users_list.html")

@app.get("/users/new")
def add_user_form():
    return render_template("add_user.html")

@app.post("/users/new")
def add_user():
    # Need to add code to capture new fields
    # and perform SQLAlchemy stuff
    return redirect("/users")

@app.get("/add_user")
def add_user():
    return render_template("add_user.html")

@app.get("/users/<user_id>")
def user_details(user_id):
    # More SQLAlchemy stuff to get user from table
    # and then pass that info to the *user=user
    return render_template("user_details.html")

