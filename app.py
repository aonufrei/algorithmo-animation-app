from flask import Flask, url_for, request, redirect, render_template
from werkzeug.utils import secure_filename
from sortigo import processor
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

        
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['user_image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(APP_ROOT)
        file.save(APP_ROOT + url_for('static', filename="images/") + filename)
        processor.Separator(APP_ROOT + url_for('static', filename='images/' + filename))

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)