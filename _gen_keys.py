import sqlite3


conn = sqlite3.connect("keys.db")
crsr = conn.cursor()

# crsr.execute('ALTER users MODIFY keys varchar')

# keys table
crsr.execute("""
CREATE TABLE IF NOT EXISTS keys (
    value char(30) PRIMARY KEY NOT NULL UNIQUE,
    type int(1),
    owner_name varchar
)
""")

# users table
crsr.execute("""
CREATE TABLE IF NOT EXISTS users (
    name varchar PRIMARY KEY NOT NULL UNIQUE,
    password_hash varchar,
    type int(1),
    keys varchar
)
""")


conn.commit()
conn.close()