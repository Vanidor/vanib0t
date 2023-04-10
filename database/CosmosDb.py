import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import time
from database.DatabaseStrategy import Database
from database.User import User
from database.ChannelSettings import ChannelSettings


class CosmosDb(Database):
    def __init__(self, host: str, master_key: str):
        self.DATABASE_ID = "vanib0t"
        self.USER_CONTAINER_ID = "Users"
        self.SETTINGS_CONTAINER_ID = "Settings"

        self.client = cosmos_client.CosmosClient(
            host, {"masterKey": master_key},
            user_agent=self.DATABASE_ID,
            user_agent_overwrite=True)

        # database
        try:
            self.db = self.client.create_database(id=self.DATABASE_ID)
            print('Database with id \'{0}\' created'.format(self.DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            self.db = self.client.get_database_client(self.DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(
                self.DATABASE_ID))

        # user container
        try:
            self.user_container = self.db.create_container(
                id=self.USER_CONTAINER_ID, partition_key=PartitionKey(path='/id'))
            print('Container with id \'{0}\' created'.format(
                self.USER_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            self.user_container = self.db.get_container_client(
                self.USER_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(
                self.USER_CONTAINER_ID))

        # settings container
        try:
            self.settings_container = self.db.create_container(
                id=self.SETTINGS_CONTAINER_ID, partition_key=PartitionKey(path='/id'))
            print('Container with id \'{0}\' created'.format(
                self.SETTINGS_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            self.settings_container = self.db.get_container_client(
                self.SETTINGS_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(
                self.SETTINGS_CONTAINER_ID))

    def create_user(self, user_id, user_name):
        new_user = User(
            user_id=user_id,
            display_name=user_name,
            last_seen=time.time(),
            last_command=None,
            is_admin_user=False,
            is_chatgpt_user=True
        )
        user_dict = new_user.toDict()
        result = self.user_container.create_item(body=user_dict)
        if len(result) > 0:
            return True
        else:
            return False

    def read_user(self, user_id):
        user = self.user_container.read_item(
            item=user_id, partition_key=user_id)
        user_obj = User(
            user_id=user["id"],
            display_name=user["display_name"],
            last_seen=user["last_seen"],
            last_command=user["last_command"],
            is_admin_user=user["is_admin_user"],
            is_chatgpt_user=user["is_chatgpt_user"]
        )
        return user_obj

    def update_user(self, updated_user):
        user_dict = updated_user.toDict()
        self.user_container.upsert_item(body=user_dict)

    def delete_user(self, user_id):
        self.user_container.delete_item(item=user_id, partition_key=user_id)

    # -------------------------------------------------

    def create_channel_settings(self, channel_id, channel_name):
        new_channel_settings = ChannelSettings(
            channel_id=channel_id,
            display_name=channel_name,
            feature_chatgpt=True,
            feature_fishh=True,
            feature_streamschedule=False
        )
        self.settings_container.create_item(body=str(new_channel_settings))

    def read_channel_settings(self, channel_id):
        item = self.settings_container.read_item(
            item=channel_id, partition_key=channel_id)
        return item

    def update_channel_settings(self, updated_settings):
        self.settings_container.upsert_item(body=updated_settings)

    def delete_channel_settings(self, channel_id):
        self.settings_container.delete_item(
            item=channel_id, partition_key=channel_id)
