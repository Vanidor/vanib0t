from datetime import datetime
from TwitchThreadMessage import TwitchThreadMessage


class TwitchThread():
    def __init__(self, thread_id: str, thread_starting_datetime: datetime, thread_starting_message_id: str, thread_author: str, thread_starting_message: str):
        self.id = thread_id
        self.starting_datetime = thread_starting_datetime
        self.author = thread_author
        self.__messages = list()

        self.add_message(
            message_id=thread_starting_message_id,
            message_author=thread_author,
            message_content=thread_starting_message
        )

    def add_message(self, message_id: str, message_author: str, message_content: str):
        message = TwitchThreadMessage(
            message_id=message_id,
            message_author=message_author,
            message_content=message_content)
        self.__messages.append(message)

    def get_messages(self):
        return self.__messages
