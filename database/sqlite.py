from ChannelSettings import ChannelSettings
from User import User
from Message import Message

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

engine = create_engine("sqlite:///test.db", echo=False)
Message.metadata.create_all(engine)
User.metadata.create_all(engine)
ChannelSettings.metadata.create_all(engine)

with Session(engine) as session:
    vanidor_user = User(
        user_id=14202186,
        display_name="Vanidor",
        last_seen=datetime.now(),
        is_admin_user=True,
        is_chatgpt_user=True
    )
    statement = select(User).where(User.user_id.is_(vanidor_user.user_id))
    result = session.scalars(statement).one()
    if result is None:
        session.add(vanidor_user)
    else:
        print("User already exists.")

    vanidor_channel_settings = ChannelSettings(
        channel_id=14202186,
        display_name="Vanidor",
        feature_chatgpt=True,
        feature_fishh=True,
        feature_streamschedule=True
    )
    statement = select(ChannelSettings).where(ChannelSettings.channel_id.is_(vanidor_channel_settings.channel_id))
    result = session.scalars(statement).one()
    if result is None:
        session.add(ChannelSettings)
    else:
        print("Settings already exists.")

    try:
        session.commit()
    except IntegrityError:
        print("Can't commit")