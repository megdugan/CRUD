import cs304dbi as dbi

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