from sqlalchemy import select

from database import Database, User
from security import PasswordService


class UserService:
    """The front-desk clerk. Signs people up and checks them at login."""

    def __init__(self, database: Database, passwords: PasswordService):
        self._database = database
        self._passwords = passwords

    def register(self, email: str, password: str) -> User | None:
        email = email.strip().lower()
        with self._database.get_session() as session:
            existing = session.scalar(select(User).where(User.email == email))
            if existing:
                return None
            user = User(
                email=email,
                password_hash=self._passwords.hash_password(password),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def authenticate(self, email: str, password: str) -> User | None:
        email = email.strip().lower()
        with self._database.get_session() as session:
            user = session.scalar(select(User).where(User.email == email))
            if user and self._passwords.verify_password(password, user.password_hash):
                return user
            return None