from flask import Flask, url_for, send_file, redirect, request, render_template, session
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


@app.route('/', methods=['GET'])
def got_to_home():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/home/step1', methods=['GET', 'POST'])
def file_upload():
    form = ImageUploaderForm(CombinedMultiDict((request.files, request.form)), meta={'csrf': False})

    if request.method == 'POST':
        if form.validate_on_submit():
            settings = dict(columns=form.image_columns.data, rows=form.image_rows.data,
                            algorithm=form.algorithm.data)

            code = datetime.now().strftime('%d%m%Y%H%M%S')
            f = form.user_image.data
            name = code + secure_filename(f.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
            f.save(image_path)
            anim = build_animation(image_path, settings, code, 'mp4', app.config['UPLOAD_FOLDER'])
            session['result'] = dict(image=name, anim=anim, settings=settings)
            return redirect('/home/step2')

    return render_template('step1.html', form=form)


@app.route('/home/step2', methods=['GET'])
def results_view():
    return render_template('step2.html',
                           user_image=session['result']['image'],
                           result_video=session['result']['anim'],
                           settings=session['result']['settings'])


@app.route('/home/step2/download', methods=['GET'])
def download_file():
    path = os.path.join(app.config['UPLOAD_FOLDER'], session['result']['anim'])
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
