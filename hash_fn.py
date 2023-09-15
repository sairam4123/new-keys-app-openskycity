from hashlib import md5

__all__ = ['hash_password', 'hash_password_old']

def hash_password(pw: str) -> str:
    return (md5((pw + '$').encode()).hexdigest())

def hash_password_old(pw: str) -> str:
    return pw + '$'