from . import app
from flask import request, send_from_directory, render_template
import tempfile
import hashlib
import base64
import string
import random
import shutil
import json
import time
import pymongo
import os


mongo = pymongo.MongoClient('localhost')
db = mongo.hubdb


@app.route('/cache/<file>')
def cache(file):
    assert file.startswith('0.'), file
    return send_from_directory(os.path.join(app.root_path, 'cache'), file)


@app.cli.command('clean-cache')
def clean_cache():
    '''Clean compiled JS/WASM cache.'''

    shutil.rmtree(os.path.join(app.root_path, 'cache'))
    print('cache cleaned!')


random.seed(time.time_ns())

def myhash(source):
    sha = hashlib.sha1()
    sha.update(source.encode())
    return base64.b32encode(sha.digest()).decode().replace('=', '1')


def get_cache_id(source):
    return '0.' + myhash(source)


def get_save_id(name):
    assert all(i in string.ascii_letters + string.digits for i in name), name
    return '1.' + name


def get_user_id(addr):
    return addr


def get_cache_path(source):
    cachedir = os.path.join(app.root_path, 'cache')
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    cacheid = get_cache_id(source)
    return cacheid, os.path.join(cachedir, cacheid)


def get_saved_path(name):
    savedir = os.path.join(app.root_path, 'saved')
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    saveid = get_save_id(name)
    return saveid, os.path.join(savedir, saveid)


@app.route('/compile', methods=['POST'])
def compile_():
    print('[IP] Got an compile request from:', request.remote_addr)
    source = str(request.form['code'])
    result = compile_code(source)
    return result


@app.route('/load', methods=['GET'])
def load():
    name = str(request.args['name'])
    saveid, save_path = get_saved_path(name)

    entry = db.arts.find_one({'name': name})
    if entry is None:
        print('Saved entry not found for', name, 'at:', save_path)
        ret = {'status': 'notfound'}
        return ret

    entry = dict(entry.items())
    ret = {'status': 'found'}
    del entry['_id']
    ret.update(entry)
    return ret


@app.route('/')
def browse():
    listfile = os.path.join(app.root_path, 'saved', 'entries.lst')
    shaders = []
    for shader in db.arts.find():
        shaders.append(shader)
    return render_template('browse.html', shaders=shaders)


@app.route('/p/<name>')
def view(name):
    return render_template('index.html', shader_name=name)


def record_save_entry(entry):
    db.arts.insert_one(entry)


@app.route('/save', methods=['POST'])
def save():
    userid = get_user_id(request.remote_addr)
    name = str(request.form['name'])
    code = str(request.form['code'])
    title = str(request.form['title'])
    cacheid, cache_path = get_cache_path(code)
    if not os.path.exists(cache_path):
        print('Cache entry not found at:', cache_path)
        ret = {'status': 'notfound'}
        return ret

    print('Saving to an existing entry')

    record = {'name': name, 'cacheid': cacheid, 'userid': userid, 'title': title, 'mtime': time.asctime()}
    print('Saving record for user =', userid, 'and name =', name)
    db.arts.insert_one(record)

    ret = {'status': 'saved'}
    return ret


@app.cli.command('clean-arts')
def clean_arts():
    '''Clean user artworks (caution!).'''

    db.drop_collection('arts')
    print('database cleaned!')


def compile_code(source):
    from .compiler import do_compile

    print('Compiling code:')
    print(source)
    print('(END)')

    cacheid, dst = get_cache_path(source)

    script = f'/cache/{cacheid}.js'
    if os.path.exists(dst + '.js'):
        print('Using cached result in:', dst)
        ret = {'status': 'cached', 'cacheid': cacheid, 'script': script}
        return ret

    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, 'main.py')
        ext = [os.path.join(app.root_path, 'static', 'hub.py')]

        with open(src, 'w') as f:
            f.write(source)

        print('compiling', src, 'to', dst)
        output, status = do_compile(dst, src, ext)
        print('done with', src, 'to', dst)

        output = output.decode()
        ret = {'status': status, 'output': output}
        if status == 'success':
            with open(dst, 'w') as f:
                f.write(source)
        if status == 'success':
            ret['cacheid'] = cacheid
            ret['script'] = script
        return ret
