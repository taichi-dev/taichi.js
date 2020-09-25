from flask import Flask, request, render_template, send_from_directory
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


def get_cache_dir():
    cachedir = os.path.join(app.root_path, 'cache')
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)
    return cachedir


@app.route('/upload', methods=['POST'])
def upload():
    #return 'N/A'
    code = request.form['code']
    result = compile_code(get_cache_dir(), str(code))
    return result


@app.route('/cache/<file>')
def cache(file):
    assert file.startswith('0.') and (file.endswith('js') or file.endswith('wasm'))
    return send_from_directory(os.path.join(app.root_path, 'cache'), file)


@app.route('/taichi.js')
def taichi_js():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taichi.js')
