import sqlite3
conn = sqlite3.connect('database/database.db')
c = conn.cursor()
c.execute("delete from user where 1=1;")
conn.commit()
conn.close()