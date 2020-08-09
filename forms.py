from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FileField
from wtforms.validators import InputRequired, AnyOf, NumberRange

class ImageUploaderForm(FlaskForm):
    image_width = IntegerField('image_width', validators=[InputRequired('Please, input image width')])
    image_height = IntegerField('image_height', validators=[InputRequired('Please, input image width')])

    image_columns = IntegerField('image_columns', validators=[InputRequired('Please, input image width'), NumberRange(min=10, max=50)])
    image_rows = IntegerField('image_columns', validators=[InputRequired('Please, input image width'), NumberRange(min=10, max=50)])

    user_image = FileField('user_image', validators=[InputRequired('Please, add image to process')])

    algorithm = StringField('algorithm', validators=[InputRequired('Pleasem input algorithm to process image'), AnyOf(values=['Bubble'])])

    
    