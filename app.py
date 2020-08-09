from flask import Flask, url_for, request, render_template
from werkzeug.utils import secure_filename

from sortigo.builder import build_animation

import os, threading
from datetime import datetime

from forms import ImageUploaderForm

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '/uploads')
app.config['SECRET_KEY'] = 'secret key'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageUploaderForm()

    if form.validate_on_submit():
        settings = dict(image_height=form.image_height, image_width=form.image_width, columns=form.image_columns, rows=form.image_rows, algorithm=form.algorithm)
        print(settings)
        image = secure_filename(form.user_image.data.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'],  str(datetime.now()) + image.filename)
        image.save(image_path)
        build_animation(image_path, settings, str(datetime.now()), '.avi')
        return 'processed'

    return render_template('step1.html', form=form)

   
@app.route('/then', methods=['GET'])
def then():
    return 'hello'



if __name__ == "__main__":
    app.run(debug=True)