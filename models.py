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

    tags = db.relationship("Tag", secondary="posts_tags",
                            backref = "posts")

class PostTag(db.Model):
    """Through Table for Posts and Tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.id"),
                        primary_key = True)

    

class Tag(db.Model):
    """Tags for Posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    name = db.Column(db.String,
                    unique=True)