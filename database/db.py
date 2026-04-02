import sqlite3

conn = sqlite3.connect("database/users.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        name TEXT
    )
""")

cursor.execute("INSERT INTO users(name) VALUES('Shabik')")
cursor.execute("INSERT INTO users(name) VALUES('Nathan')")
cursor.execute("INSERT INTO users(name) VALUES('Krirk')")
cursor.execute("INSERT INTO users(name) VALUES('Mikael')")
cursor.execute("INSERT INTO users(name) VALUES('Anderson')")
cursor.execute("INSERT INTO users(name) VALUES('Peter')")

conn.commit()
conn.close()
