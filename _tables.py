# crsr.execute('ALTER users MODIFY keys varchar')

def generate(crsr):
    # keys table
    crsr.execute("""
    CREATE TABLE IF NOT EXISTS keys (
        value char(30) PRIMARY KEY NOT NULL UNIQUE,
        type int(1),
        owner_name varchar DEFAULT ''
    )
    """)

    # users table
    crsr.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name varchar PRIMARY KEY NOT NULL UNIQUE,
        password_hash varchar,
        type int(1),
        keys varchar DEFAULT '[]'
    )
    """)
