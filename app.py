from flask import Flask, url_for, request, redirect, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)