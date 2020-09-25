import socket
import shutil
import sys
import os


if __name__ == '__main__':
    if sys.argv[1] == 'compile':
        from .compiler import do_compile
        do_compile(sys.argv[2])

    elif sys.argv[1] == 'server':
        from .flaskapp import app
        app.run(host=socket.gethostname(), port=int(sys.argv[2]), debug=True)

    elif sys.argv[1] == 'clean':
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'cache'))
