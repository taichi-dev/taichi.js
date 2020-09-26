from . import app
from flask import request, send_from_directory
import tempfile
import hashlib
import base64
import time
import string
import random
import shutil
import os


@app.route('/cache/<file>')
def cache(file):
    assert file.startswith('0.'), file
    assert file.endswith('.js') or file.endswith('.wasm') or file.endswith('.py'), file
    try:
        beg = file.index('_')
        end = file[beg + 1:].index('_') + beg + 2
        file = file[:beg] + file[end:]
    except ValueError:
        pass
    return send_from_directory(os.path.join(app.root_path, 'cache'), file)


@app.cli.command('clean-cache')
def clean_cache():
    '''Clean compiled JS/WASM cache.'''

    shutil.rmtree(os.path.join(app.root_path, 'cache'))
    print('cache cleaned!')


random.seed(time.time_ns())

def get_cache_id(source):
    sha = hashlib.sha1()
    sha.update(source.encode('utf-8'))
    return base64.b32encode(sha.digest()).decode()


def get_cache_path(source):
    cachedir = os.path.join(app.root_path, 'cache')
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    cacheid = '0.' + get_cache_id(source)
    return cacheid, os.path.join(cachedir, cacheid)


@app.route('/compile', methods=['POST'])
def compile_():
    print('Got an compile request from: ', request.remote_addr)
    source = str(request.form['code'])
    result = compile_code(source)
    return result


@app.route('/save', methods=['POST'])
def save():
    print('Got a request from: ', request.remote_addr)
    source = str(request.form['code'])
    cache_py = get_cache_path(source)[1] + '.py'
    with open(cache_py, 'w') as f:
        f.write(source)
    return result


def compile_code(source):
    from .compiler import do_compile

    print('Compiling code:')
    print(source)
    print('(END)')

    cacheid, dst = get_cache_path(source)

    script = f'/cache/{cacheid}.js'
    if os.path.exists(dst + '.js'):
        print('Using cached result in:', dst)
        ret = {'status': 'cached', 'script': script}
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
            ret['script'] = script
        return ret
