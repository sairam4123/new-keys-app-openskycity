from __future__ import annotations

__all__ = [
    'User', 'UserType'
]

import json

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from keys import Key

class UserType(IntEnum):
    BASIC = 1
    DEVELOPER = 2

class User:
    def __init__(
        self,
        name: str = "", 
        _type: UserType = UserType.BASIC, 
        password_hash: str = "",
    ) -> None:
        self.id = 0
        self.name = name
        self.type = _type
        self.pw_hash = password_hash
        self.keys: list[Key] = []

    def _update(self):
        from user_manager import UserManager
        um = UserManager()
        um._mark_dirty(self)

    def add_key(self, key: 'Key'):
        key.set_owner(self)
        self.keys.append(key)
        self._update()
    
    def to_tuple(self):
        return (
            self.name, 
            self.pw_hash, 
            self.type, 
            json.dumps([key.value for key in self.keys])
        )

    @classmethod
    def from_tuple(cls, usr_tup):
        inst = cls()
        inst.name = usr_tup[0]
        inst.pw_hash = usr_tup[1]
        inst.type = UserType(usr_tup[2])
        keys_val = json.loads(usr_tup[3])
        inst.keys = []
        
        from key_manager import KeysManager
        km = KeysManager()
        for val in keys_val:
            inst.keys.append(km.get_key(val))

        return inst
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<User name={self.name!r} type={self.type!r} keys={self.keys!r}>"
