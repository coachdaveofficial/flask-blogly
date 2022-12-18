"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()



db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(), nullable=True, default='')

    posts = db.relationship("Post", cascade="all,delete", backref="User")


    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Tag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all,delete",
        backref="tags",
    )

class PostTag(db.Model):
    """Post and Tag Join"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

