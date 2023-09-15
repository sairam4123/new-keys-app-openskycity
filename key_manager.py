from __future__ import annotations

from db import DatabaseManager
from singleton import singleton
from typing import TYPE_CHECKING

from keys import Key

if TYPE_CHECKING:
    from keys import KeyType


@singleton
class KeysManager:
    def __init__(self) -> None:
        self.db = DatabaseManager()
        self._cached_keys: list[Key] = []

    def create_key(self, key_type: KeyType) -> Key:
        _key = Key(Key._generate_key(), key_type)
        self._cached_keys.append(_key)
        return _key

    def has_key(self, key_val: str) -> bool:
        self.db.crsr.execute(
            """
            SELECT value FROM keys
            WHERE value = ?
            """, [key_val]
        )
        return bool(self.db.crsr.fetchone())

    def get_key(self, key_val: str) -> Key:
        self.db.crsr.execute(
            """
            SELECT * FROM keys
            WHERE value = ?
            """, [key_val]
        )
        key_tup = self.db.crsr.fetchone()
        return Key.from_tuple(key_tup)

    def list_all_keys(self):
        self.db.crsr.execute("""
        SELECT * FROM keys;
        """)
        keys = self.db.crsr.fetchall()
        return [Key.from_tuple(key_tup) for key_tup in keys]

    def _save(self) -> None:
        self.db.crsr.executemany(
            """
            INSERT INTO keys
            VALUES (?, ?, ?)
            ON CONFLICT(value) DO UPDATE SET owner_name=excluded.owner_name;
            """, [key.to_tuple() for key in self._cached_keys]
        )
        self.db.commit()
        self._cached_keys.clear()

    def _mark_dirty(self, key: Key):
        self._cached_keys.append(key)
