#!/usr/bin/env python3

import subprocess
import tempfile
import random
import string
import shutil
import time
import sys
import os


def do_compile(target, source=None):
    if source is None:
        source = target

    print('Generating action record...')
    env = dict(os.environ)
    env.update({'TI_ACTION_RECORD': f'{target}.yml', 'TI_ARCH': 'cc'})
    try:
        output = subprocess.check_output([sys.executable, '-m', 'taichi', 'run', source],
            env=env, stderr=subprocess.STDOUT, timeout=8)
    except subprocess.CalledProcessError as e:
        print('Error while generating action record:')
        print(e.output)
        print('(END)')
        os.unlink(f'{target}.yml')
        return e.output, 'failure'
    except subprocess.TimeoutExpired as e:
        print('Timeout while generating action record:')
        print(e.output)
        print('(END)')
        os.unlink(f'{target}.yml')
        return e.output + '\n(Time limit exceed)', 'timeout'

    print('Composing C file...')
    subprocess.check_call([sys.executable, '-m', 'taichi', 'cc_compose',
        '-e', f'{target}.yml', f'{target}.c', f'{target}.h'])

    print('Compiling via Emscripten...')
    subprocess.check_call(['emcc', '-O3', f'{target}.c', '-o', f'{target}.js'])

    # https://stackoverflow.com/questions/38769103/document-currentscript-is-null
    # AJAX loaded Javascript doesn't seems support document.currentScript.src,
    # which is being used in Emscripten generated JS stub.
    # So we do a quick hack to make AJAX happy:
    with open(f'{target}.js') as f:
        s = f.read()
    s = s.replace('var scriptDirectory=""', 'var scriptDirectory="/cache/"', 1)
    with open(f'{target}.js', 'w') as f:
        f.write(s)

    os.unlink(f'{target}.yml')
    os.unlink(f'{target}.h')
    os.unlink(f'{target}.c')

    return output, 'success'


random.seed(time.time_ns())

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def compile_code(cachedir, source):
    cacheid = '0.' + get_random_string(10)

    with tempfile.TemporaryDirectory() as tmpdir:
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


if __name__ == '__main__':
    do_compile(sys.argv[1])
