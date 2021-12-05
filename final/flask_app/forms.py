from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import EqualTo, InputRequired
from wtforms import StringField, SubmitField, PasswordField, FieldList
from flask_pagedown.fields import PageDownField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
)

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=42)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_pwd = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class GiftRequestForm(FlaskForm):
    gifts = FieldList(StringField("gifts"), min_entries=1)
    firstname = StringField("firstname", validators=[InputRequired()])
    lastname = StringField("lastname", validators=[InputRequired()])
    address1 = StringField("address1", validators=[InputRequired()])
    address2 = StringField("address2", validators=[InputRequired()])
    country = StringField("country", validators=[InputRequired()])
    state = StringField("state", validators=[InputRequired()])
    zip = StringField("zip", validators=[InputRequired()])

class UpdateTrackingForm(FlaskForm):
    tracking = StringField("Tracking #", validators=[InputRequired()])
    submit = SubmitField("Update")

class CommentForm(FlaskForm):
    pagedown = PageDownField("Comment on the gift")
    submit = SubmitField("Submit")