import sqlite3

conn = sqlite3.connect("starwars.db")

with open("migration.sql", "r", encoding="utf-8") as f:
    sql = f.read()

conn.executescript(sql)
conn.close()

print("Миграция выполнена")