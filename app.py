# Meg and Nina
# CRUD assignment

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import secrets
import cs304dbi as dbi

app = Flask(__name__)
app.secret_key = secrets.token_hex()

# Configures DBI
print(dbi.conf('nh107_db'))

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def main():
    return render_template('main.html', page_title='Main Page')

@app.route('/insert/')
def insert():
    return render_template('insert.html')

@app.route('/select/')
def select():
    return render_template('select.html')

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
