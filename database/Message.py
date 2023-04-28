from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from Base import Base

class Message(Base):
    ''' Class representing a twitch chat message '''
    __tablename__ = "message"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(primary_key=True)
    message_timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    message_content: Mapped[str] = mapped_column(String())
