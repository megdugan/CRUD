# Meg and Nina
# CRUD assignment
# Database functions

import cs304dbi as dbi

addedby = 123

def find_tt(conn, tt):
    '''
    Checks if the tt exists in the database.
    If none, returns empty dict. Otherwise, returns result.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select tt
                    from movie
                    where tt=%s''', [tt])
    return curs.fetchall()

def insert_movie(conn, tt, movie):
    '''Adds the submitted movie to the database.'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into movie (tt, title, addedby) 
                    values (%s, %s, %s)''', [tt, movie, addedby])
    conn.commit()
    return

def get_incomplete_movies(conn):
    '''
    Get list of information about movies without a release date or director
    Args:
        None
    Return:
        list of movies -> dict[]
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from movie where 'release' is NULL or director is NULL''')
    return curs.fetchall()

def update(conn, tt, release, director):
    '''Updates the given movie with the submitted data.'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''update movie
                    set `release`=%s, director=%s
                    where tt=%s''', [release, director, tt])
    conn.commit()
    return

if __name__ == '__main__':
    dbi.conf("md109_db")
    conn = dbi.connect()
    print(find_tt(conn, 123))
    print(get_incomplete_movies(conn)[:5])