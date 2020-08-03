#!/usr/bin/env python3
import os
import sys

program = sys.argv[1]

print('Generating action record...')
os.system(f'TI_ACTION_RECORD={program}.yml TI_ARCH=cc python3 {program}')
print('Composing C file...')
os.system(f'python3 -m taichi cc_compose -e {program}.yml {program}.c')
print('Compiling via Emscripten...')
os.system(f'emcc -O3 {program}.c -o {program}.js')
