import logging as log
import sqlite3
import time
from DatabaseStrategy import Database
from User import User
from ChannelSettings import ChannelSettings


class SqliteDb(Database):
    def __init__(self, database_name: str):
        log.basicConfig(
            level=log.DEBUG
        )
        self.database_name = database_name

        self.user_table_name = "Users"
        self.user_table = f"""
            CREATE TABLE IF NOT EXISTS {self.user_table_name}
            (user_id INTEGER NOT NULL PRIMARY KEY, 
            display_name NOT NULL,
            last_seen,
            last_command,
            is_admin_user,
            is_chatgpt_user)"""

        log.debug("User table SQL query: %s", self.user_table)

        self.settings_table_name = "ChannelSettings"
        self.settings_table = f"""
            CREATE TABLE IF NOT EXISTS {self.settings_table_name}
            (channel_id INTEGER NOT NULL PRIMARY KEY,
            display_name NOT NULL,
            feature_chatgpt,
            feature_fishh,
            feature_streamschedule)"""

        log.debug("Settings table SQL query: %s", self.settings_table)

        self.message_table_name = "ChannelMessages"
        self.message_table = f"""
            CREATE TABLE IF NOT EXISTS {self.message_table_name}
            (
            user_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            message_timestamp NOT NULL,
            message_content TEXT NOT NULL,
            FOREIGN KEY (channel_id) REFERENCES {self.settings_table_name}(channel_id)            
            )
            """

        self.db_connection = sqlite3.connect(f"{self.database_name}.db")
        self.db_cursor = self.db_connection.cursor()

        # user table
        try:
            self.db_cursor.execute(self.user_table)
            log.debug("Table with name %s created", self.user_table_name)

        except Exception as exc:
            print(exc)
            log.error("Error while creating %s table: %s (%s)", self.user_table_name, exc, type(exc))

        # channel settings table
        try:
            self.db_cursor.execute(self.settings_table)
            log.debug("Table with name %s created", self.settings_table_name)

        except Exception as exc:
            print(exc)
            log.error("Error while creating %s table: %s (%s)", self.settings_table_name, exc, type(exc))

        # message table
        try:
            self.db_cursor.execute(self.message_table)
            log.debug("Table with name %s created", self.message_table_name)

        except Exception as exc:
            print(exc)
            log.error("Error while creating %s table: %s (%s)", self.message_table_name, exc, type(exc))

    def create_user(self, user_id, user_name):
        sql_query = f"""
            INSERT INTO {self.user_table_name} VALUES 
            ("{user_id}", "{user_name}", "{time.time()}", Null, {False}, {True})"""
        log.debug("Creating new user with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.IntegrityError:
            log.info("Couldn't create user %s with id %s, user already exists!", user_name, user_id)


    def read_user(self, user_id):
        sql_query = f"""
            SELECT *
            FROM {self.user_table_name}
            WHERE user_id = {user_id}"""
        log.debug("Reading user with SQL query %s", sql_query)
        result = self.db_cursor.execute(sql_query)
        fetchedResult = result.fetchone()
        if fetchedResult is not None:
            log.debug("Read user %s", fetchedResult)
            user_obj = User(
                user_id=fetchedResult[0],
                display_name=fetchedResult[1],
                last_seen=fetchedResult[2],
                last_command=fetchedResult[3],
                is_admin_user=fetchedResult[4],
                is_chatgpt_user=fetchedResult[5]
            )
        else:
            log.info("Couldn't find user with id %s", user_id)
            user_obj = None
        return user_obj

    def update_user(self, updated_user: User):
        if updated_user.last_command is None:
            updated_user.last_command = "Null"
        sql_query = f"""
            UPDATE {self.user_table_name}
            SET
                user_id = "{updated_user.user_id}",
                display_name = "{updated_user.display_name}",
                last_seen = "{updated_user.last_seen}",
                last_command = {updated_user.last_command},
                is_admin_user = {updated_user.is_admin_user},
                is_chatgpt_user = {updated_user.is_chatgpt_user}
            WHERE
                user_id = {updated_user.user_id}
            """
        log.debug("Updating user with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.OperationalError as exc:
            log.info("Couldn't update user %s (%s) with id: %s (%s)", updated_user.display_name, updated_user.user_id, exc, type(exc))

    def delete_user(self, user_id):
        sql_query = f"""
            DELETE FROM {self.user_table_name}
            WHERE user_id = {user_id}
            """
        log.debug("Deleting user with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.OperationalError as exc:
            log.info("Couldn't delete user with id %s: %s (%s)", user_id, exc, type(exc))
    # -------------------------------------------------

    def create_channel_settings(self, channel_id, channel_name):
        sql_query = f"""
            INSERT INTO {self.settings_table_name} VALUES
            ("{channel_id}", "{channel_name}", {True}, {True}, {False})
            """
        log.debug("Creating new channel settings with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.IntegrityError:
            log.info("Couldn't create channel settings for %s with id %s, channel settings already exists!", channel_name, channel_id)


    def read_channel_settings(self, channel_id):
        sql_query = f"""
            SELECT *
            FROM {self.settings_table_name}
            WHERE channel_id = {channel_id}"""
        log.debug("Reading channel settings with SQL query %s", sql_query)
        result = self.db_cursor.execute(sql_query)
        fetched_result = result.fetchone()
        if fetched_result is not None:
            log.debug("Read channel settings %s", fetched_result)
            channel_settings_obj = ChannelSettings(
                channel_id=fetched_result[0],
                display_name=fetched_result[1],
                feature_chatgpt=fetched_result[2],
                feature_fishh=fetched_result[3],
                feature_streamschedule=fetched_result[4]
            )
        else:
            log.info("Couldn't find channel settings with id %s", channel_id)
            channel_settings_obj = None
        return channel_settings_obj

    def update_channel_settings(self, updated_settings: ChannelSettings):
        sql_query = f"""
            UPDATE {self.settings_table_name}
            SET 
                channel_id = "{updated_settings.channel_id}",
                display_name = "{updated_settings.display_name}",
                feature_chatgpt = "{updated_settings.feature_chatgpt}",
                feature_fishh = "{updated_settings.feature_fishh}",
                feature_streamschedule = "{updated_settings.feature_streamschedule}"
            """
        log.debug("Updating channel settings with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.OperationalError as exc:
            log.info("Couldn't update channel settings for %s with id %s: %s (%s)", updated_settings.display_name, updated_settings.channel_id, exc, type(exc))

    def delete_channel_settings(self, channel_id):
        sql_query = f"""
            DELETE FROM {self.settings_table_name}
            WHERE channel_id = {channel_id}
            """
        log.debug("Deleting channel settings with SQL query %s", sql_query)
        try:
            self.db_cursor.execute(sql_query)
            self.db_connection.commit()
        except sqlite3.OperationalError as exc:
            log.info("Couldn't delete channel settings with id %s: %s (%s)", channel_id, exc, type(exc))


    def close_database(self) -> bool:
        return None