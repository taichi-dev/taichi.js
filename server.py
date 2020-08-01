#!/usr/bin/env python3
import os
import sys
import shutil
import socket
import http.server
import socketserver
import qrcode.console_scripts

def main(path=None):
    def handler(*args):
        return http.server.SimpleHTTPRequestHandler(directory=path, *args)

    port = 8123
    ip = socket.gethostbyname(socket.gethostname())
    url = f'http://{ip}:{port}/'

    with socketserver.TCPServer(('', port), handler) as httpd:
        qrcode.console_scripts.main([url])
        print('listening at', url)
        httpd.serve_forever()

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
