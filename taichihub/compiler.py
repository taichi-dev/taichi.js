#!/usr/bin/env python3

import subprocess
import shutil
import sys
import os


docker_image = 'taichihub'


def do_compile(target, source=None, extra=[]):
    if source is None:
        source = target

    envs = 'TI_ACTION_RECORD='

    print('Generating action record...')
    try:
        container = subprocess.check_output(['docker', 'create', '-a', 'STDOUT', '-a', 'STDERR',
                '-e', 'TI_ACTION_RECORD=/app/main.py.yml', '-e', 'TI_ARCH=cc',
                docker_image, 'python', 'main.py']).decode().strip()
        subprocess.check_call(['docker', 'cp', source, container + ':/app/main.py'])
        for e in extra:
            subprocess.check_call(['docker', 'cp', e, container + ':/app/' + os.path.basename(e)])
        try:
            output = subprocess.check_output(['docker', 'start', '-a', container],
                stderr=subprocess.STDOUT, timeout=8)
        except subprocess.CalledProcessError as e:
            print('Error while generating action record:')
            print(e.output)
            print('(END)')
            return e.output, 'failure'
        except subprocess.TimeoutExpired as e:
            print('Timeout while generating action record:')
            print(e.output)
            print('(END)')
            return e.output, 'timeout'

        print('The program output was:')
        print(output.decode())
        print('(END)')
        subprocess.check_call(['docker', 'cp', container + ':/app/main.py.yml', f'{source}.yml'])
    finally:
        subprocess.call(['docker', 'rm', container])

    print('Composing C file...')
    subprocess.check_call([sys.executable, '-m', 'taichi', 'cc_compose',
        '-e', f'{source}.yml', f'{source}.c', f'{source}.h'])

    print('Compiling via Emscripten...')
    subprocess.check_call(['emcc', '-O3', f'{source}.c', '-o', f'{target}.js'])

    with open(f'{target}.js') as f:
        s = f.read()
    # https://stackoverflow.com/questions/38769103/document-currentscript-is-null
    # AJAX loaded Javascript doesn't seems support document.currentScript.src,
    # which is being used in Emscripten generated JS stub.
    # So we do a quick hack to make AJAX happy:
    s = s.replace('var scriptDirectory=""', 'var scriptDirectory="/cache/"', 1)
    # Make sure the browser keep reloading, don't cache the WASM file:
    s = s.replace('.wasm";', '.wasm?dummy="+Date.now();', 1)
    with open(f'{target}.js', 'w') as f:
        f.write(s)

    return output, 'success'


if __name__ == '__main__':
    do_compile(sys.argv[1])
