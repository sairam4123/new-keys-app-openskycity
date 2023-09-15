from singleton import singleton

import sqlite3


@singleton
class DatabaseManager:

    def __init__(self) -> None:
        self.crsr: sqlite3.Cursor

    @classmethod
    def from_file(cls, file: str):
        conn = sqlite3.connect(file)
        crsr = conn.cursor()
        inst = cls()
        inst.crsr = crsr
        return inst

    def generate_tables(self):
        import _tables
        _tables.generate(self.crsr)

    def commit(self):
        self.crsr.connection.commit()
    
    def save(self):
        self.commit()

    def close(self):
        conn = self.crsr.connection
        conn.commit()
        conn.close()
