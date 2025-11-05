# Meg and Nina
# CRUD assignment
# Database functions

import cs304dbi as dbi

addedby = 123

def find_tt(conn, tt):
    '''Checks if the tt exists in the database.'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select tt
                    from movie
                    where tt=%s''', [tt])
    return curs.fetchall()

def insert_movie(conn, tt, movie):
    '''Adds the submitted movie to the database'''
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

if __name__ == '__main__':
    dbi.conf("nh107_db")
    conn = dbi.connect()
    print(get_incomplete_movies(conn)[:5])