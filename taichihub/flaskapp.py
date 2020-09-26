import logging
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


@app.route('/upload', methods=['POST'])
def upload():
    print('Got a request from: ', request.remote_addr)
    code = request.form['code']
    result = compile_code(app, str(code))
    return result


@app.route('/cache/<file>')
def cache(file):
    if file == 'default_scene.js':
        return send_from_directory(os.path.join(app.root_path, 'static'), 'default_scene.js')
    if file == 'default_scene.wasm':
        return send_from_directory(os.path.join(app.root_path, 'static'), 'default_scene.wasm')
    assert file.startswith('0.') and (file.endswith('js') or file.endswith('wasm')), file
    return send_from_directory(os.path.join(app.root_path, 'cache'), file)


@app.route('/taichi.js')
def taichi_js():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taichi.js')
