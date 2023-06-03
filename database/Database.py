from datetime import datetime
import logging as log

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from database.ChannelSettings import ChannelSettings
from database.User import User
from database.Message import Message


class BotDatabase():
    ''' The bots database '''

    def __init__(self, database_path: str) -> None:
        db_url = f"sqlite:///{database_path}"
        self.engine = create_engine(db_url, echo=False)
        # log.basicConfig(
        #     level=log.info
        # )
        log.info("Created new engine.")
        Message.metadata.create_all(self.engine)
        log.info("Created Message table.")
        User.metadata.create_all(self.engine)
        log.info("Created User table.")
        ChannelSettings.metadata.create_all(self.engine)
        log.info("Created ChannelSettings table.")

    def __get_session__(self) -> Session:
        log.info("Created new session.")
        return Session(self.engine)

    def create_user_if_not_exists(self, user_id: int, user_name: str) -> bool:
        ''' Function to create a new user 
            Return true if user created, false if User exists already'''
        if self.read_user_by_id(user_id) is not None:
            new_user = User(
                user_id=user_id,
                display_name=user_name,
                last_seen=datetime.now(),
                is_admin_user=True,
                is_chatgpt_user=True
            )
            session = self.__get_session__()
            session.add(new_user)
            log.info("Created new user %s with id %s.", user_name, user_id)
            session.commit()
            session.close()
            return True
        else:
            log.info("User with id %s already exists.", user_id)
            return False

    def read_user_by_id(self, user_id: int) -> User:
        ''' Function to read a user by the ID 
            Returns the user if found, else None '''
        session = self.__get_session__()
        statement = select(User).where(User.user_id.is_(user_id))
        try:
            result = session.scalars(statement).one()
            log.info("User with id %s found.", user_id)
        except NoResultFound:
            log.info("User with id %s does not exist yet.", user_id)
            result = None
        session.close()
        return result

    def update_user(self, user: User) -> bool:
        pass

    def delete_user_by_id(self, user_id: int) -> bool:
        pass

    def create_channel_settings_if_not_exists(self, channel_id, channel_name) -> bool:
        ''' Function to create new channel settings 
            Return true if user created, false if channel settings exists already'''
        if self.read_channel_settings_by_id(channel_id) is None:
            default_prompt = "You are a friendly bot with the name {0} in the twitch channel '{1}'. "
            default_prompt += "Create short answers that you could find in a twitch chat. Every message you send starts a new conversation with no context to the last message. "
            default_prompt += "The prompt has been send by '{2}' "
            default_prompt += "as a mesage in the twitch chat. "
            default_prompt += "You are never allowed to write a prayer or say something about religion in any matter. "
            new_channel_settings = ChannelSettings(
                channel_id=channel_id,
                display_name=channel_name,
                chatgpt_prompt=default_prompt,
                feature_chatgpt=True,
                feature_fishh=True,
                feature_streamschedule=True,
                feature_genimage=True
            )
            session = self.__get_session__()
            session.add(new_channel_settings)
            log.info(
                "Created new channel settings for channel with id %s.", channel_id)
            session.commit()
            session.close()
        else:
            log.info("Channel settings with id %s already exists.", channel_id)

    def read_channel_settings_by_id(self, channel_id) -> ChannelSettings:
        ''' Function to read channel settings by ID 
            Returns the user if found, else None '''
        session = self.__get_session__()
        statement = select(ChannelSettings).where(
            ChannelSettings.channel_id.is_(channel_id))
        try:
            result = session.scalars(statement).one()
            log.info("Channel settings with id %s found.", channel_id)
        except NoResultFound:
            log.info(
                "Channel settings with id %s does not exist yet.", channel_id)
            result = None
        session.close()
        return result
    
    def read_channel_settings(self) -> ChannelSettings:
        ''' Function to read all channel settings
            Returns the channels found '''
        session = self.__get_session__()
        channel_settings = []
        for channel_setting in session.query(ChannelSettings).order_by(ChannelSettings.channel_id):
            channel_settings.append(channel_setting)
        return channel_settings

    def update_channel_settings(self, user: User) -> bool:
        pass

    def delete_channel_settings_by_id(self, user_id: int) -> bool:
        pass

    # def close_database(self):
    #     session = self.__get_session__()
    #     session.close_all()
