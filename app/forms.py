from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
import sqlalchemy as sa
from app import db
from app.models import User

neighbourhoods_list = ['Charlottenburg-Wilmersdorf', 'Friedrichshain', 'Kreuzberg', 'Mitte', 'Neuköln', 
                       'Pankow', 'Prenzlauer Berg', 'Tempelhof-Schöneberg', 'Wedding']

transit_list = ["U1","U2","U3","U4","U5","U6","U7","U8","U9","--",
                "S1","S2","S3","S4","S5","S6","S7","S8","S9","Ringbahn"]

beer_rating_list = [1,2,3,4,5]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=140)]) 
    transit = SelectField("Transit", choices=transit_list, validators=[DataRequired()])
    neighbourhood = SelectField("Neighbourhood", choices=neighbourhoods_list, validators=[DataRequired()])
    beer_rating = SelectField("Beer Rating", choices=beer_rating_list, validators=[DataRequired()])
    guinness = BooleanField("Guinness")
    smoking = BooleanField("Smoking")
    music = StringField("Music")
    map_embed = StringField("Map Embed")
    body = TextAreaField("Body", validators=[DataRequired()])
    image_data = FileField("Image Data", validators=[Optional()])
    image_filename = StringField("Image name", validators=[Optional()])
    visible = BooleanField("Visible", default="checked")
    submit = SubmitField("Submit")