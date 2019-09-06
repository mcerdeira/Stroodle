import sqlite3

conn = sqlite3.connect('data/crawled_web.db')
_cursor = conn.cursor()

def exec_inserts(inserts):
        for params in inserts:
                #print("SQL: " + str((params[1])))
                _cursor.execute(params[0], (params[1]))

        conn.commit()                                

def clean_up():
        sql = "DELETE FROM songs where song = 'Total Album Time:'"
        _cursor.execute(sql)
        conn.commit() 

def insert_movie(params):
        sql = "INSERT INTO movies VALUES (?, ?, ?, ?)"
        return (sql, (params))
        #_cursor.execute(sql, (params))
        #conn.commit()

def insert_song(params):
        sql = "INSERT INTO songs VALUES (?, ?)"
        return (sql, (params))
        #_cursor.execute(sql, (params))
        #conn.commit()

def get_intial_url_load():
        sql = "SELECT max(id) as id FROM movies"
        rows = _cursor.execute(sql)
        return rows.fetchall()

def close_all():
        conn.commit()
        conn.close()