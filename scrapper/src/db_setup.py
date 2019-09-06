import sqlite3
conn = sqlite3.connect('data/crawled_web.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE movies
             (id text, url text, title text, tag text)''')
			 
c.execute('''CREATE TABLE songs
             (id text, song text)''')			 

conn.commit()
conn.close()