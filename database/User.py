from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database.Base import Base


class User(Base):
    ''' Class representing the information of a user '''
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(length=30))
    last_seen: Mapped[datetime]
    is_admin_user: Mapped[bool]
    is_chatgpt_user: Mapped[bool]
