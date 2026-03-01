import sqlite3

conn = sqlite3.connect("starwars.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT id, name FROM characters LIMIT 10").fetchall()
for row in rows:
    print(row)

conn.close()