from __future__ import annotations

__all__ = [
    'UserManager'
]

from singleton import singleton
from db import DatabaseManager

from typing import TYPE_CHECKING, Optional
from users import User
from hash_fn import hash_password, hash_password_old

if TYPE_CHECKING:
    from users import UserType

@singleton
class UserManager:
    
    def __init__(self) -> None:
        self.db: DatabaseManager = DatabaseManager()
        self.cached_users: list[User] = []
        self.logged_user: Optional[User] = None

    def _mark_dirty(self, user: User):
        self.cached_users.append(user)

    def login(self, user_name: str, password: str) -> bool:
        hashed_pass = hash_password(password)
        old_hash = hash_password_old(password)

        if not self.has_user(user_name):
            return False
        
        if (user := self.get_user(user_name)):
            if user.pw_hash == hashed_pass:
                self.logged_user = user
                return True
            elif user.pw_hash == old_hash:
                self.logged_user = user
                self.migrate_user(user, new_hashed_password=hashed_pass)
                return True
        
        return False
    
    def logout(self) -> bool:
        if self.logged_user is None:
            return False
        self.logged_user = None
        return True
    
    def migrate_user(self, user: User, **kwargs):
        hash_pw = kwargs.get('new_hashed_password')
        if hash_pw:
            user.pw_hash = hash_pw
            self.cached_users.append(user)
        # Add extra migration code

    def has_user(self, user_name: str) -> bool:
        if self.cached_users:
            users = [user for user in self.cached_users if user.name == user_name]
            return bool(users)
        
        self.db.crsr.execute("""
            SELECT name FROM users
            WHERE name = ?
        """, [user_name])
        return bool(self.db.crsr.fetchone())
    
    def get_user(self, user_name: str) -> User:
        if self.cached_users:
            users = [user for user in self.cached_users if user.name == user_name]
            if len(users):
                return users[0]
        
        self.db.crsr.execute("""
            SELECT * FROM users
            WHERE name = ?
        """, [user_name])
        usr_tup = self.db.crsr.fetchone()
        if not usr_tup:
            return User()
        return User.from_tuple(usr_tup)
    
    def create_user(self, name: str, user_type: UserType, password: str):
        inst = User(name=name, _type=user_type)
        inst.pw_hash = hash_password(password)
        self.cached_users.append(inst)
        return inst
    
    def list_all_users(self) -> list[User]:
        self.db.crsr.execute("""
        SELECT * FROM users;
        """)
        users = self.db.crsr.fetchall()
        return [User.from_tuple(usr_tup) for usr_tup in users]

    def _save(self):
        self.db.crsr.executemany("""
        INSERT INTO users
        VALUES (?, ?, ?, ?)
        ON CONFLICT 
            DO UPDATE
                SET 
                    keys=excluded.keys,
                    password_hash=excluded.password_hash
        """, [user.to_tuple() for user in self.cached_users])

        self.db.commit()
        self.cached_users.clear()