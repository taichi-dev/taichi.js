#!/usr/bin/env python3

import subprocess
import tempfile
import sys
import os


def do_compile(program):
    print('Generating action record...')
    env = dict(os.environ)
    env.update({'TI_ACTION_RECORD': f'{program}.yml', 'TI_ARCH': 'cc'})
    subprocess.check_call([sys.executable, program], env=env)
    print('Composing C file...')
    subprocess.check_output([sys.executable, '-m', 'taichi', 'cc_compose', '-e', f'{program}.yml', f'{program}.c', f'{program}.h'])
    print('Compiling via Emscripten...')
    subprocess.check_call(['emcc', '-O3', f'{program}.c', '-o', f'{program}.js'])


def compile_code(source):
    with tempfile.TemporaryDirectory() as tmpdir:
        main_py = os.path.join(tmpdir, 'main.py')
        main_js = os.path.join(tmpdir, 'main.py.js')
        main_wasm = os.path.join(tmpdir, 'main.py.wasm')

        with open(main_py, 'w') as f:
            f.write(source)

        print('compiling', main_py)
        do_compile(main_py)
        print('done with', main_py)

        with open(main_js, 'r') as f:
            js_code = f.read()

        return js_code


if __name__ == '__main__':
    do_compile(sys.argv[1])
