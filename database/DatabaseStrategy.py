from abc import ABC, abstractmethod
from database.User import User
from database.ChannelSettings import ChannelSettings


class Database(ABC):
    ''' Abstract class for the database strategy pattern '''
    @abstractmethod
    def create_user(self, user_id, user_name) -> bool:
        ''' Create a new user '''

    @abstractmethod
    def read_user(self, user_id) -> User:
        ''' Read an existing user '''

    @abstractmethod
    def update_user(self, updated_user: User) -> bool:
        ''' Update an existing user '''

    @abstractmethod
    def delete_user(self, user_id) -> bool:
        ''' Delete an existing user '''

    @abstractmethod
    def user_exists(self, user_id) -> bool:
        ''' Check if an user exists'''

    # -------------------------------------------------

    @abstractmethod
    def create_channel_settings(self, channel_id, channel_name) -> bool:
        ''' Create new channel settings '''

    @abstractmethod
    def read_channel_settings(self, channel_id) -> ChannelSettings:
        ''' Reade existing channel settings '''

    @abstractmethod
    def update_channel_settings(self, updated_settings) -> bool:
        ''' Update existing channel settings '''

    @abstractmethod
    def delete_channel_settings(self, channel_id) -> bool:
        ''' Delete existing channel settings'''

    @abstractmethod
    def channel_settings_exists(self, channel_id) -> bool:
        ''' Check if channel settings exists '''

    # -------------------------------------------------

    @abstractmethod
    def close_database(self) -> bool:
        ''' Close existing database connections and write everything '''
