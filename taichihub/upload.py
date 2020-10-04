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


random.seed(time.time())

def myhash(source):
    sha = hashlib.sha1()
    sha.update(source.encode())
    return base64.b32encode(sha.digest()).decode().replace('=', '1')


def get_cache_id(source):
    return '0.' + myhash(source)


def get_cache_path(source):
    cachedir = os.path.join(app.root_path, 'cache')
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    cacheid = get_cache_id(source)
    return cacheid, os.path.join(cachedir, cacheid)


@app.route('/compile', methods=['POST'])
def compile_():
    print('[IP] Got an compile request from:', request.remote_addr)
    source = str(request.form['code'])
    result = compile_code(source)
    return result


@app.route('/load', methods=['GET'])
def load():
    name = str(request.args['name'])
    entry = db.arts.find_one({'name': name})
    if entry is None:
        return {'status': 'notfound'}

    entry = dict(entry.items())
    ret = {'status': 'found'}
    for k, v in entry.items():
        if k[0] != '_':
            ret[k] = v
    return ret


@app.route('/')
def browse():
    shaders = []
    for shader in db.arts.find():
        shaders.append(shader)
    return render_template('browse.html', shaders=shaders)


@app.route('/p/<name>')
def view(name):
    return render_template('index.html', shader_name=name)


@app.route('/save', methods=['POST'])
def save():
    userid = request.remote_addr
    name = str(request.form['name'])
    code = str(request.form['code'])
    title = str(request.form['title'])
    cacheid, cache_path = get_cache_path(code)
    if not os.path.exists(cache_path + '.js'):
        return {'status': 'notfound'}

    record = db.arts.find_one({'name': name})
    if record is not None:
        if record['userid'] != userid:
            return {'status': 'conflict'}

    mtime = time.asctime()
    record = {'name': name, 'cacheid': cacheid, 'userid': userid,
              'title': title, 'code': code, 'mtime': mtime}

    if db.arts.find_one_and_update({'name': name}, {'$set': record}) is None:
        db.arts.insert_one(record)

    ret = {'status': 'saved'}
    return ret


@app.cli.command('edit-db')
def edit_db():
    '''Edit user database.'''

    import IPython
    IPython.embed()


def compile_code(source):
    from .compiler import do_compile

    cacheid, dst = get_cache_path(source)

    script = f'/cache/{cacheid}.js'
    if os.path.exists(dst + '.js'):
        return {'status': 'cached', 'cacheid': cacheid, 'script': script}

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
            ret['cacheid'] = cacheid
            ret['script'] = script
        return ret
