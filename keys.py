
__all__ = [
    'KeyType',
    'Key'
]

import string
import random
from enum import IntEnum
from typing import TYPE_CHECKING
from singleton import singleton

if TYPE_CHECKING:
    from users import User


class KeyType(IntEnum):
    PREMIUM = 1
    SPECIAL_SANDBOX = 2

class Key:
    def __init__(
        self, 
        value: str = None, 
        _type: KeyType = KeyType.PREMIUM, 
        owner: 'User' = None,
    ) -> None:
        self.value = value
        self.type = _type
        self.owner = owner
    
    @staticmethod
    def _generate_key(word_count=5, chr_count=5):
        chars = string.ascii_uppercase + string.digits
        key = ""
        for _ in range(word_count):
            for _ in range(chr_count):
                key += random.choice(chars)
            key += '-'
        return key.rstrip('-')

    def serialize(self):
        return {'value': self.value, 'type': self.type}
    
    def set_owner(self, user: 'User'):
        self.owner = user

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<Key value={self.value!r} type={self.type!r}>"

@singleton
class KeysManager:
    def create_key(self, key_type: KeyType):
        inst = Key()
        inst.type = key_type
        inst.value = Key._generate_key()
        return inst
    
    def has_key(self, key_val: str) -> bool:
        ...

    def get_key(self, key_val: str) -> Key:
        ...
