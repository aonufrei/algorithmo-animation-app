from flask import Flask, send_file, redirect, request, render_template, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from sortigo.builder import build_animation

import os, threading
from datetime import datetime

from forms import ImageUploaderForm
from werkzeug.datastructures import CombinedMultiDict


uploads_delete_timeout = 60*5


csrf = CSRFProtect()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           os.path.join('static', 'uploads'))
app.config['SECRET_KEY'] = 'secret key'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

def clean_uploads():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    for filepath in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filepath))

def check_session():
    exist = False
    
    if session['result'] != None:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], session['result']['image'])
        anim_path  = os.path.join(app.config['UPLOAD_FOLDER'], session['result']['anim'])
        
        exist = os.path.exists(image_path) and os.path.exists(anim_path)
    
    return exist

def clean_session(ses):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], ses['image']))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], ses['anim']))
    except Exception:
        pass


@app.route('/', methods=['GET'])
def got_to_home():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/home/step1', methods=['GET', 'POST'])
def file_upload():
    form = ImageUploaderForm(CombinedMultiDict((request.files, request.form)))
    validation_failed = False
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                clean_session(session['result'])
            except Exception:
                pass
            settings = dict(columns=form.image_columns.data, rows=form.image_rows.data,
                            algorithm=form.algorithm.data)

            code = datetime.now().strftime('%d%m%Y%H%M%S')
            f = form.user_image.data
            name = code + secure_filename(f.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
            f.save(image_path)
            anim = build_animation(image_path, settings, code, 'webm', app.config['UPLOAD_FOLDER'])
            session['result'] = dict(image=name, anim=anim, settings=settings)
            threading.Timer(uploads_delete_timeout, clean_session, args=[session['result']]).start()
            return redirect('/home/step2')
        else:
            validation_failed = True

    return render_template('step1.html', form=form, failed=validation_failed)


@app.route('/home/step2', methods=['GET'])
def results_view():
    if not check_session():
        return redirect('/home/step1')

    return render_template('step2.html',
                           user_image=session['result']['image'],
                           result_video=session['result']['anim'],
                           settings=session['result']['settings'],
                           timer=uploads_delete_timeout)


@app.route('/home/step2/download', methods=['GET'])
def download_file():
    path = os.path.join(app.config['UPLOAD_FOLDER'], session['result']['anim'])
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return redirect('/home/step1')




if __name__ == "__main__":
    clean_uploads()
    app.run(debug=True)
    csrf.init_app(app)
