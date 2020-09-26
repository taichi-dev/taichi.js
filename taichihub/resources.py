from . import app
from flask import render_template, send_from_directory
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/taichi.js')
def taichi_js():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taichi.js')
