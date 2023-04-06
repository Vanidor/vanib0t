import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

class CosmosDbHelper:
    def __init__(self, host: str, master_key: str):
        self.DATABASE_ID = "vanib0t"
        self.USER_CONTAINER_ID = "Users"
        self.SETTINGS_CONTAINER_ID = "Settings"

        self.client = cosmos_client.CosmosClient(host, {'masterKey': master_key}, user_agent=self.DATABASE_ID, user_agent_overwrite=True)

        # database
        try:
            self.db = self.client.create_database(id=self.DATABASE_ID)
            print('Database with id \'{0}\' created'.format(self.DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            self.db = self.client.get_database_client(self.DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(self.DATABASE_ID))

        # user container
        try:
            self.users_container = self.db.create_container(id=self.USER_CONTAINER_ID, partition_key=PartitionKey(path='/id'))
            print('Container with id \'{0}\' created'.format(self.USER_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            self.user_container = self.db.get_container_client(self.USER_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(self.USER_CONTAINER_ID))

        # settings container
        try:
            self.settings_container = self.db.create_container(id=self.SETTINGS_CONTAINER_ID, partition_key=PartitionKey(path='/id'))
            print('Container with id \'{0}\' created'.format(self.SETTINGS_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            self.settings_container = self.db.get_container_client(self.SETTINGS_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(self.SETTINGS_CONTAINER_ID))

    # -------------------------------------------------

    def ___get_user_stub(self, user_id, user_name):
        user_stub = {
            'id': user_id,
            'display_name': user_name,
            'last_seen': datetime.datetime.now().timestamp(),
            'last_command': None,
            'is_admin_user': False,
            'is_chatgpt_user': True,
            "___scheme_version": "1.0.0.0"
        }
        return user_stub    

    def ___get_settings_stub(self, user_id, user_name):
        settings_stub = {
            "id": user_id,
            "user_name": user_name,
            "features": {
                "chatgpt": True,
                "fishh": False,
                "stream": False
            },
            "___scheme_version": "1.0.0.0"
        }
        return settings_stub

    # -------------------------------------------------

    def create_user(self, user_id, user_name):
        user = self.___get_user_stub(
            id=user_id,
            display_name=user_name
        )
        self.user_container.create_item(body=user)

    def read_user(self, user_id):
        item = self.user_container.read_item(item=user_id, partition_key=user_id)
        return item

    def update_user(self, new_user):
        self.user_container.upsert_item(body=new_user)

    def delete_user(self, user_id):
        self.user_container.delete_item(item=user_id, partition_key=user_id)

    # -------------------------------------------------

    def create_settings(self, user_id, user_name):
        user = self.___get_settings_stub(
            id=user_id,
            display_name=user_name
        )
        self.settings_container.create_item(body=user)

    def read_settings(self, user_id):
        item = self.settings_container.read_item(item=user_id, partition_key=user_id)
        return item

    def update_settings(self, new_settings):
        self.settings_container.upsert_item(body=new_settings)

    def delete_settings(self, user_id):
        self.settings_container.delete_item(item=user_id, partition_key=user_id)