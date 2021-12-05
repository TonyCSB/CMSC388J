from flask_login import UserMixin
from mongoengine.fields import BooleanField, ListField, StringField, ReferenceField
from . import db, login_manager
from . import config
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return str(self.id)

class GiftRequest(db.Document):
    requester = ReferenceField(User, required=True)
    gifts = ListField(StringField(required=True))
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    address1 = StringField(require=True)
    address2 = StringField()
    country = StringField(require=True)
    state = StringField(require=True)
    zip = StringField(require=True)
    matched = BooleanField(require=True)

class MatchedGift(db.Document):
    giftReceiver = ReferenceField(User, required=True)
    giftSender = ReferenceField(User, required=True)
    gift = ReferenceField(GiftRequest, required=True)
    status =  StringField(required=True)
    giftName = StringField()
    tracking = StringField()
    comment = StringField()
