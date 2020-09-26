from . import app
from flask import request, send_from_directory
import tempfile
import time
import string
import random
import shutil
import os


@app.route('/upload', methods=['POST'])
def upload():
    print('Got a request from: ', request.remote_addr)
    code = request.form['code']
    result = compile_code(str(code))
    return result


@app.route('/cache/<file>')
def cache(file):
    if file == 'default_scene.js':
        return send_from_directory(os.path.join(app.root_path, 'static'), 'default_scene.js')
    if file == 'default_scene.wasm':
        return send_from_directory(os.path.join(app.root_path, 'static'), 'default_scene.wasm')
    assert file.startswith('0.') and (file.endswith('js') or file.endswith('wasm')), file
    return send_from_directory(os.path.join(app.root_path, 'cache'), file)


@app.cli.command('clean-cache')
def clean_cache():
    '''Clean compiled JS/WASM cache.'''

    shutil.rmtree(os.path.join(app.root_path, 'cache'))
    print('cache cleaned!')


random.seed(time.time_ns())

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def compile_code(source):
    from .compiler import do_compile

    print('Compiling code:')
    print(source)
    print('(END)')

    cachedir = os.path.join(app.root_path, 'cache')
    if not os.path.exists(cachedir):
        os.mkdir(cachedir)

    cacheid = '0.' + get_random_string(10)

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chmod(tmpdir, 0o777)

        src = os.path.join(tmpdir, 'main.py')
        dst = os.path.join(cachedir, f'{cacheid}')

        with open(src, 'w') as f:
            f.write(source)

        print('compiling', src, 'to', dst)
        output, status = do_compile(dst, src)
        print('done with', src, 'to', dst)

        output = output.decode()
        ret = {'status': status, 'output': output}
        if status == 'success':
            ret['cacheid'] = cacheid
            ret['javascript'] = f'/cache/{cacheid}.js'
        return ret
