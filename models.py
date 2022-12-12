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
    created_at = db.Column(db.String(), nullable=True, default= now.strftime("%d/%m/%Y %H:%M:%S"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # owner = db.relationship('User')



