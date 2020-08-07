from flask import Flask, url_for, request, render_template
from werkzeug.utils import secure_filename

from sortigo.builder import build_animation

import os, threading
from datetime import datetime

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return render_template('step1.html')

        
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['user_image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename += datetime.now()
        full_image_path = APP_ROOT + url_for('static', filename='images/' + filename)
        #print(APP_ROOT)
        himg  = request.form['image_height'  ]
        wimg  = request.form['image_width'   ]
        horiz = request.form['hseparations'  ] 
        vert  = request.form['vseparations'  ]
        anim  = request.form['animation_mode']

        settings = dict(image_height=himg, image_width=wimg, columns=horiz, rows=vert, algorithm=anim)

        file.save(full_image_path)

        threading.Thread(target=build_animation, args=(full_image_path, settings, filename, 'avi'))


    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)