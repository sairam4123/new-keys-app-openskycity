import sqlite3

from keys import KeyType, Key

conn = sqlite3.connect("keys.db")
crsr = conn.cursor()

crsr.execute("""
CREATE TABLE IF NOT EXISTS keys (
    value char(30) PRIMARY KEY NOT NULL UNIQUE,
    type int(1)
)
""")


# create 5 premium keys
keys = [Key.create(KeyType.PREMIUM) for _ in range(5)]
print(keys)

# create 5 special sandbox keys
keys_ss = [Key.create(KeyType.SPECIAL_SANDBOX) for _ in range(5)]
print(keys)

crsr.executemany("""
INSERT INTO keys
VALUES (?, ?)
""", [(key.value, key.type) for key in keys + keys_ss])

conn.commit()
conn.close()