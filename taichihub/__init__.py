from flask import Flask

app = Flask(__name__)

from . import resources
from . import upload
