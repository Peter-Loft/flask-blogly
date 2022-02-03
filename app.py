"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post

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


# ============================================================
# USER ROUTES
# ============================================================


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

    user_data = request.form

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


# ============================================================
# POST ROUTES
# ============================================================


@app.get("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """Form for creating new post"""

    user = User.query.get_or_404(user_id)
    return render_template("add_post.html", user=user)


@app.post("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Logic for creating new post, redirects"""
    
    form_data = request.form

    post = Post(
        title=form_data.get("title"),
        content=form_data.get("content"),
        user_id = user_id
    )
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def post_details(post_id):
    """Details about a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)
