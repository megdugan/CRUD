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

# Main / welcome page
@app.route('/')
def main():
    return render_template('main.html', page_title='Main Page')

# Gives the insert form on a GET and processes the insertion on a POST 
# (and then redirects to the /update/nnn page
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
        
        # Checks that all values are entered
        if tt == "":
            flash('Please enter a tt value.')
            return render_template('insert.html')
        if title == "":
            flash('Please enter a title.')
            return render_template('insert.html')
        if release == "":
            flash('Please enter a release year.')
            return render_template('insert.html')

        conn = dbi.connect()
        if wmdb.find_tt(conn, tt) == None:
            # The tt is available, so add the movie to the database
            wmdb.insert_movie(conn, tt, title, release)
            return redirect(url_for('update', tt=tt))
        else:
            # The tt is available, so flash a message and reset the form.
            flash('The movie id ' + str(tt) + ' was unavailable. Please try again.')
            return render_template('insert.html')

# On GET shows a menu of movies with incomplete information, either null value 
# for either release or director and on POST redirects to the /update/nnn page 
# for that movie
@app.route('/select/', methods=['POST', 'GET'])
def select():
    conn = dbi.connect()
    if request.method == 'GET':
        # Send a blank form
        incomplete_movies = db.get_incomplete_movies(conn)
        return render_template('select.html', movies=incomplete_movies)
    else:
        # Method is POST, form has been filled out
        # Redirect to update incomplete movie form
        tt = request.form.get('menu-tt')
        return redirect(url_for('update', tt=tt))

# Shows a form for updating a particular movie, with the TT of the movie 
# in the URL on GET and on POST does the update and shows the form again
@app.route('/update/<tt>', methods=['POST', 'GET'])
def update(tt):
    conn = dbi.connect()
    movie = db.get_movie_from_tt(conn, tt)
    dname = db.get_director_name(conn, movie['director'])
    abname = db.get_addedby_name(conn, movie['addedby'])
    if request.method == 'GET':
        # Send the update form
        return render_template('update.html', movie = movie, director = dname, staff = abname)
    else:
        button = request.form.get('submit')
        if button == 'update':
            # Method is post, and button is update, form has been filled out
            # Update movie and flash success message
            title = request.form.get('movie-title')
            
            # get movie id (tt)
            try:
                tt = int(request.form.get('movie-tt')) # Form gets string, cast tt as integer
                if tt < 1:
                    raise Exception
            except Exception: # if tt is not an integer, do not update movie
                flash('Movie ID must be an integer greater than 0. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)
            
            # get addedby id
            try:
                addedby = int(request.form.get('movie-addedby')) # Form gets string, cast addedby as integer
                if addedby < 1:
                    raise Exception # if addedby is not an integer, do not update movie
            except Exception:
                flash('Added by must be an integer greater than 0. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)
            
            # get release
            release = request.form.get('movie-release')
            if release != '' and (not release.isdigit() or not len(release)) == 4: # if year is not 4-digit integer, do not update movie
                flash('Release must be a 4-digit year. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)
            # get director
            director = request.form.get('movie-director')

            # Check for unallowed movie updates

            # If tt is updated, ensure the value is available
            if movie['tt'] != tt and wmdb.find_tt(conn, tt) != None:
                # Flash a message if not available
                flash('The movie id ' + str(tt) + ' was unavailable. Please try again.')
                return redirect(url_for('update', tt=tt))

            # If director is updated, ensure the director exists
            if movie['director'] != director and db.find_director(conn, director) == None:
                flash('Director not in database. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)

            # Ensure title is not none
            if title == 'None':
                flash('Title cannot be None. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)
            
            # Ensure tt is not none
            if tt == 'None': 
                flash('TT cannot be None. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)

            # Catch blank / None type responses to form and convert from strings
            if release == 'None':
                release = None
            if director == 'None':
                director = None
            if addedby == 'None':
                addedby = None

            # Finally, check that the movie's fields were updated at all
            if title == movie['title'] and tt == movie['tt'] and release == movie['release'] and addedby == movie['addedby'] and director == movie['director']:
                flash('No fields were edited. Did not update movie.')
                return render_template('update.html', movie = movie, director = dname, staff = abname)
            
            # Otherwise, update movie and flash 
            print(f"director {director}")
            dname = db.get_director_name(conn, director)
            abname = db.get_addedby_name(conn, addedby)
            db.update_movie(conn, tt, title, release, director, addedby)
            flash(f'{title} was successfully updated.')
            return render_template('update.html', movie = movie, director = dname, staff = abname)
        if button == 'delete':
            movie = db.delete_movie(conn, tt)
            flash(f'Movie {title} has been deleted.')
            incomplete_movies = db.get_incomplete_movies(conn)
            return render_template('select.html', movies=incomplete_movies)

if __name__ == '__main__':
    import sys, os
    dbi.conf('nh107_db')
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
