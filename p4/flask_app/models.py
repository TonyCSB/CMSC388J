from flask_login import UserMixin
from datetime import datetime

from mongoengine.fields import ReferenceField
from . import db, login_manager


@login_manager.user_loader
def load_user(email):
    return User.objects(email=email).first()


class User(db.Document, UserMixin):
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True, max_length=40, min_length=1)
    password = db.StringField(required=True)
    picture = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.email


class Review(db.Document):
    imdb_id = db.StringField(required=True, max_length=9, min_length=9)
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, max_length=500, min_length=5)
    date = db.StringField(required=True)
    movie_title = db.StringField(required=True, max_length=100, min_length=1)
    image = db.StringField()

# User.drop_collection()
# Review.drop_collection()
