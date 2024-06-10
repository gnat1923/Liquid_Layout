from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=140)]) 
    transit = StringField("Transit", validators=[DataRequired(), Length(min=1, max=140)])
    neighbourhood = StringField("Neighbourhood", validators=[DataRequired(), Length(min=1, max=140)])
    beer_rating = IntegerField("Beer Rating", validators=[DataRequired()])
    guinness = BooleanField("Guinness")
    smoking = BooleanField("Smoking")
    music = StringField("Music")
    body = TextAreaField("Body", validators=[DataRequired(), Length(min=1, max=1084)])
    submit = SubmitField("Submit")