import os

package_root = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.join(package_root, '..')


from flask import Flask, request, render_template, Markup
from .compiler import compile_code

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    code = request.form['code']
    result = compile_code(str(code))
    return '<code>%s</code>' % Markup.escape(result)