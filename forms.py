from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, AnyOf, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

file_formats = ['jpg', 'png']

class ImageUploaderForm(FlaskForm):
    image_columns = IntegerField('image_columns', validators=[InputRequired('Please, input how many columns should we make'), NumberRange(min=10, max=50)])
    image_rows = IntegerField('image_rows', validators=[InputRequired('Please, input how many rows should we make'), NumberRange(min=10, max=50)])

    user_image = FileField('user_image', validators=[FileRequired('Please, add image to process'), FileAllowed(file_formats, message='You can upload files of type png or jpg only')])

    algorithm = StringField('algorithm', validators=[InputRequired('Pleasem input algorithm to process image'), AnyOf(values=['Bubble'])])

    
    