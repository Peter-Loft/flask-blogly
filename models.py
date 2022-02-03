"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50))
    image_url = db.Column(db.String(100))


class Post(db.Model):
    """Post for Blog"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String(2000),
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
                        
    author = db.relationship('User', backref='posts')
