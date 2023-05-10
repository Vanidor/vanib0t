from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database.Base import Base


class FishCommand(Base):
    ''' Class representing the information of a user '''
    __tablename__ = "fish_command"

    channel_id: Mapped[int] = mapped_column(primary_key=True)
    emote_name: Mapped[str] = mapped_column(String())
    probability: Mapped[float] = mapped_column(Float(precision=3))
