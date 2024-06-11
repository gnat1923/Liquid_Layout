from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
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
    map_embed = StringField("Map Embed")
    body = TextAreaField("Body", validators=[DataRequired()])
    image_data = FileField("Image Data", validators=[Optional()])
    image_filename = StringField("Image name", validators=[Optional()])
    visible = BooleanField("Visible", default="checked")
    submit = SubmitField("Submit")