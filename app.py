"""Blogly application."""

from flask import Flask, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
# db.create_all()


@app.get("/")
def users_list():
    return render_template("users_list.html")


@app.get("/add_user")
def add_user():
    return render_template("add_user.html")
