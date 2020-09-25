from flask import Flask, request, render_template, Markup
from .compiler import compile_code
import os

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/upload', methods=['POST'])
def upload():
    code = request.form['code']
    result = compile_code(str(code))
    return '<code>%s</code>' % Markup.escape(result)
