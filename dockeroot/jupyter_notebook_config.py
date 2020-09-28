# Configuration file for jupyter-notebook.

c.JupyterApp.answer_yes = True
c.NotebookApp.allow_password_change = False
c.NotebookApp.allow_remote_access = True
c.NotebookApp.answer_yes = True
c.NotebookApp.autoreload = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.nbserver_extensions = {}
c.NotebookApp.notebook_dir = '/app'
c.NotebookApp.open_browser = False
c.NotebookApp.password_required = False
c.NotebookApp.port = 8080
c.NotebookApp.port_retries = 0
c.NotebookApp.quit_button = False
c.NotebookApp.rate_limit_window = 3
c.NotebookApp.token = ''
c.FileContentsManager.delete_to_trash = False

import os

os.environ['TI_GUI_BACKEND'] = 'ipython'
