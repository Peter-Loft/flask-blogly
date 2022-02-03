"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "THIS DOESNT MATTER"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get("/")
def homepage():
    """Start page, redirects to /users"""

    return redirect("/users")


@app.get("/users")
def users_list():
    """Displays list of all users"""

    return render_template("users_list.html")


@app.get("/users/new")
def add_user_form():
    """Form for adding a new user"""

    return render_template("add_user.html")


@app.post("/users/new")
def add_user():
    """Creates new user and saves to database"""

    user_data = request.form
    if not user_data.get("fname"):
        flash("First name required")
        return redirect("/users/new")

    user = User(
        first_name=user_data.get("fname"),
        last_name=user_data.get("lname"),
        image_url=user_data.get("image_url"),
    )
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.get("/users/<user_id>")
def user_details(user_id):
    """Details about a specific user"""

    # More SQLAlchemy stuff to get user from table
    # and then pass that info to the *user=user
    return render_template("user_details.html")
