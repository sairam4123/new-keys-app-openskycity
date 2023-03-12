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
    
    @classmethod
    def create(cls, name: str, usr_type: UserType, password: str) -> 'User':
        inst = cls()
        inst.type = usr_type
        inst.pw_hash = hash(password)
        inst.name = name
        return inst

    def add_key(self, key: 'Key'):
        key.set_owner(self)
        self.keys.append(key)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<User name={self.name!r} type={self.type!r} keys={self.keys!r}>"

class UserManager:
    _inst = None
    _inited = False

    def __new__(cls: type['UserManager']) -> 'UserManager':
        if cls._inst:
            return cls._inst
        else:
            cls._inst = object.__new__(cls)
            return cls._inst
    
    def __init__(self) -> None:
        if self._inited:
            return

        self._inited = True
    
    def login(self, user_name: str, password: str) -> bool:
        return False
    
    def has_user(self, user_name: str):
        ...
    
    def get_user(self, user_name: str):
        ...
    
    def create_user(self, name, user_type, password):
        inst = User()
        inst.type = user_type
        inst.pw_hash = hash(password)
        inst.name = name
        return inst
    