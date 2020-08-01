#!/usr/bin/env python3
import os
import sys

program = 'program'

print('Composing C file...')
os.system(f'python3 -m taichi cc_compose -e {program}.yml {program}.c')
print('Compiling via Emscripten...')
os.system(f'emcc {program}.c -o {program}.js')
