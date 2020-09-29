from . import app
from flask import render_template, send_from_directory
import string
import random
import time
import os


def get_random_string(n=5):
    #choices = string.ascii_letters + string.digits
    choices = string.digits
    return ''.join(random.choice(choices) for i in range(n)) + choices[time.time_ns() % len(choices)]


@app.route('/new')
def new():
    name = get_random_string()
    return f'<script>window.location.href = "/p/{name}";</script>'


@app.route('/help')
def help_():
    return render_template('help.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/taichi.js')
def taichi_js():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'taichi.js')


@app.route('/hubview.js')
def hubview_js():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'hubview.js')

@app.route('/cloth.jpg')
def cloth_jpg():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'cloth.jpg')
