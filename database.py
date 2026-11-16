from datetime import datetime, timezone

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    """One person's card in the filing room."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Database:
    """Opens the filing room and hands out clerks."""

    def __init__(self, url: str = "sqlite:///gatewatch.db"):
        self._engine = create_engine(url)
        self._session_factory = sessionmaker(bind=self._engine)

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def get_session(self):
        return self._session_factory()