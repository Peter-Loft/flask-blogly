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

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.get("/users/new")
def add_user_form():
    """Form for adding a new user"""

    return render_template("add_user.html")


@app.post("/users/new")
def add_user():
    """Creates new user and saves to database"""

    user_data = dict(request.form)
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


# CR: May be some place in the code where there is a link that puts
# a None value in for a URL or user_id (user's details page)
@app.get("/users/<int:user_id>")
def user_details(user_id):
    """Details about a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.get("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Gets user via user_id and provides from to edit details"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Processes changing user details"""

    user_data = dict(request.form)

    user = User.query.get_or_404(user_id)
    user.first_name = user_data.get("fname")
    user.last_name = user_data.get("lname")
    user.image_url = user_data.get("image_url")
    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a user"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/users")
