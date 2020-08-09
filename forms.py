from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, AnyOf

class ImageUploaderForm(FlaskForm):
    image_width = IntegerField('image_width', validators=[InputRequired('Please, input image width')])
    image_height = IntegerField('image_height', validators=[InputRequired('Please, input image width')])

    image_columns = IntegerField('image_width', validators=[InputRequired('Please, input image width')])
    image_rows = IntegerField('image_width', validators=[InputRequired('Please, input image width')])

    algorithm = StringField('algorithm', validators=[InputRequired('Pleasem input algorithm to process image'), AnyOf(values=['Bubble'])])
    