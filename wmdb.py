# Meg and Nina
# CRUD assignment
# (wmdb.py) Contains all database methods.

import cs304dbi as dbi

addedby = 123

def get_movie_from_tt(conn, tt):
    '''
    Get movie with matching tt
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from movie where tt = %s''', [tt])
    return curs.fetchone()

def find_tt(conn, tt):
    '''
    Checks if the tt exists in the database.
    If none, returns empty dict. Otherwise, returns result.
    Args:
        conn -> pymysql.connections.Connection
        tt -> int
    Return:
        list of movies -> dict[]
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select tt
                    from movie
                    where tt=%s''', [tt])
    return curs.fetchone()

def find_director(conn, director):
    '''
    Checks if the director id exists in the database.
    If none, returns none. Otherwise, returns director id.
    Args:
        conn -> pymysql.connections.Connection
        director -> int
    Return:
        director id -> int
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select nm
                    from person
                    where nm=%s''', [director])
    return curs.fetchone()

def get_director_name(conn, nm):
    '''
    Gets the director name from the database.
    The director nm must already exist in the database.
    Args:
        conn -> pymysql.connections.Connection
        nm -> int
    Return:
        director name -> str
    '''
    print(nm)
    if not nm:
        return 'None Specified'
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name
                    from person
                    where nm=%s''', [nm])
    return curs.fetchone()['name']

def get_addedby_name(conn, uid):
    '''
    Gets the director name from the database.
    The director nm must already exist in the database.
    Args:
        conn -> pymysql.connections.Connection
        id -> int
    Return:
        staff name -> str
    '''
    if not uid:
        return 'None Specified'
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name
                    from staff
                    where uid=%s''', [uid])
    return curs.fetchone()['name']

def insert_movie(conn, tt, title, release):
    '''
    Adds the submitted movie to the database.
    Args:
        conn -> pymysql.connections.Connection
        tt -> int
        title -> str
        release -> int
    Return:
        None
    '''
    
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into movie (tt, title, `release`, addedby) 
                    values (%s, %s, %s, %s)''', [tt, title, release, addedby])
    conn.commit()
    return

def delete_movie(conn, tt):
    '''
    Delete a movie from the database.
    Args:
        conn -> pymysql.connections.Connection
        tt -> int
    Return:
        None
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''delete from movie where tt = %s''', [tt])
    conn.commit()
    return

def get_incomplete_movies(conn):
    '''
    Get list of information about movies without a release date or director.
    Args:
        conn -> pymysql.connections.Connection
    Return:
        list of movies -> dict[]
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from movie where 'release' is NULL or director is NULL''')
    return curs.fetchall()

def update_movie(conn, tt, title, release, director, addedby):
    '''
    Updates the given movie with the submitted data.
    Args:
        conn -> pymysql.connections.Connection
        tt -> int
        title -> str
        release -> int
        director -> int
        addedby -> int
    Return:
        None
    '''
    curs = dbi.dict_cursor(conn)
    
    curs.execute('''update movie
                    set tt=%s, title=%s, `release`=%s, director=%s, addedby=%s
                    where tt=%s''', [tt, title, release, director, addedby, tt])
    conn.commit()
    return

def delete_movie(conn, tt):
    '''
    Delete a movie from the database.
    Args:
        conn -> pymysql.connections.Connection
        tt -> int
    Return:
        None
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''delete from movie where tt = %s''', [tt])
    conn.commit()
    return

if __name__ == '__main__':
    dbi.conf("md109_db")
    conn = dbi.connect()
    print(type(conn))