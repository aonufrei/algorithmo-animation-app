from flask import Flask, url_for, request, render_template, session
from werkzeug.utils import secure_filename

from sortigo.builder import build_animation

import os
from datetime import datetime

from forms import ImageUploaderForm
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           os.path.join('static', 'uploads'))
app.config['SECRET_KEY'] = 'secret key'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageUploaderForm(CombinedMultiDict((request.files, request.form)), meta={'csrf': False})

    if request.method == 'POST':
        if form.validate_on_submit():
            settings = dict(image_height=form.image_height.data, image_width=form.image_width.data,
                            columns=form.image_columns.data, rows=form.image_rows.data,
                            algorithm=form.algorithm.data)

            code = datetime.now().strftime('%d%m%Y%H%M%S')
            f = form.user_image.data
            name = code + secure_filename(f.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
            f.save(image_path)
            anim = build_animation(image_path, settings, code, 'avi', app.config['UPLOAD_FOLDER'])
            session['result'] = dict(image=name, anim=anim, settings=settings)
            return 'processed'
        else:
            print(form.errors)
            print('validation failed')

    return render_template('step1.html', form=form)


@app.route('/then', methods=['GET'])
def then():
    return 'hello'


if __name__ == "__main__":
    app.run(debug=True)
