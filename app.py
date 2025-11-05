# Meg and Nina
# CRUD assignment

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import secrets
import wmdb
import cs304dbi as dbi
import wmdb as db

app = Flask(__name__)
app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def main():
    return render_template('main.html', page_title='Main Page')

@app.route('/insert/', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        # Send a blank form
        return render_template('insert.html')
    else:
        # Method has to be POST, so the form has been filled out
        tt = request.form.get('movie-tt')
        title = request.form.get('movie-title')
        release = request.form.get('movie-release')

        conn = dbi.connect()
        if len(wmdb.find_tt(conn, tt)) == 0:
            # The tt is available, so add the movie to the database
            wmdb.insert_movie(conn, tt, title, release)
            return redirect(url_for('update', tt=tt))
        else:
            # The tt is available, so flash a message and reset the form.
            flash('The movie id ' + str(tt) + ' was unavailable. Please try again.')
            return redirect(url_for('insert'))


@app.route('/select/', methods=['POST', 'GET'])
def select():
    conn = dbi.connect()
    if request.method == 'GET':
        # Send a blank form
        incomplete_movies = db.get_incomplete_movies(conn)
        return render_template('select.html', movies=incomplete_movies)
    else:
        # Method has to be POST, so the form has been filled out
        tt = request.form.get('menu-tt')
        return redirect(url_for('update', tt=tt))

@app.route('/update/<tt>')
def update(tt):
    conn = dbi.connect()
    movie = db.get_movie_from_tt(conn, tt)
    return render_template('update.html', movie = movie[0])

if __name__ == '__main__':
    import sys, os
    dbi.conf('md109_db')
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
