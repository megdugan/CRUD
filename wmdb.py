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