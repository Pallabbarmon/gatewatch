from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    """Scrambles passwords and checks them. Never keeps the real password."""

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash_password(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify_password(self, plain_password: str, stored_hash: str) -> bool:
        try:
            return self._hasher.verify(stored_hash, plain_password)
        except VerifyMismatchError:
            return False