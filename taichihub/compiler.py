import subprocess
import tempfile
import os

from . import repo_root


def compile_code(source):
    with tempfile.TemporaryDirectory() as tmpdir:
        main_py = os.path.join(tmpdir, 'main.py')
        main_js = os.path.join(tmpdir, 'main.py.js')
        main_wasm = os.path.join(tmpdir, 'main.py.wasm')

        with open(main_py, 'w') as f:
            f.write(source)

        print('compiling', main_py)
        subprocess.check_call(['python', os.path.join(repo_root, 'compile.py'), main_py])
        print('done with', main_py)

        with open(main_js, 'r') as f:
            js_code = f.read()

        return js_code