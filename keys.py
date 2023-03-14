
from __future__ import annotations

__all__ = [
    'KeyType',
    'Key'
]

import string
import random
from enum import IntEnum
from typing import TYPE_CHECKING

from typing import Optional
if TYPE_CHECKING:
    from users import User



class KeyType(IntEnum):
    PREMIUM = 1
    SPECIAL_SANDBOX = 2


class Key:
    def __init__(
        self, 
        value: Optional[str] = None, 
        _type: KeyType = KeyType.PREMIUM, 
        owner: Optional[User] = None,
    ) -> None:
        self.value = value
        self.type = _type
        self.owner = owner
    
    def _update(self):
        from key_manager import KeysManager
        km = KeysManager()
        km._mark_dirty(self)
    
    @staticmethod
    def _generate_key(word_count=5, chr_count=5):
        chars = string.ascii_uppercase + string.digits
        key = ""
        for _ in range(word_count):
            for _ in range(chr_count):
                key += random.choice(chars)
            key += '-'
        return key.rstrip('-')
    
    @classmethod
    def from_tuple(cls, key_tup):
        inst = cls()
        inst.value = key_tup[0]
        inst.type = KeyType(key_tup[1])
        return inst

    def to_tuple(self):
        return (self.value, self.type, self.owner.name if self.owner else None)

    def set_owner(self, user: User):
        self.owner = user
        self._update()

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"<Key value={self.value!r} type={self.type!r}>"
