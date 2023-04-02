class TwitchThreadMessage():
    def __init__(self, message_id: str, message_author: str, message_content: str):
        self.message_id = message_id
        self.message_author = message_author
        self.message_content = message_content
