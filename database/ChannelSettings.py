from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from Base import Base


class ChannelSettings(Base):
    ''' Class representing channel settings '''
    __tablename__ = "channel_settings"

    channel_id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(length=30))
    chatgpt_prompt: Mapped[str] = mapped_column(String())
    feature_chatgpt: Mapped[bool]
    feature_fishh: Mapped[bool]
    feature_streamschedule: Mapped[bool]
