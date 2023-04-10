class User():
    ''' Class representing the information of a user '''
    user_id: str
    display_name: str
    last_seen: int
    last_command: str
    is_admin_user: bool
    is_chatgpt_user: bool
    __scheme_version: str

    def __init__(self,
                 user_id,
                 display_name,
                 last_seen,
                 last_command,
                 is_admin_user,
                 is_chatgpt_user):
        self.user_id = user_id
        self.display_name = display_name
        self.last_seen = last_seen
        self.last_command = last_command
        self.is_admin_user = is_admin_user
        self.is_chatgpt_user = is_chatgpt_user
        self.__scheme_version = "1.0.0.0"

    def toDict(self):
        user_dict = {
            "id": self.user_id,
            "display_name": self.display_name,
            "last_seen": self.last_seen,
            "last_command": self.last_command,
            "is_admin_user": self.is_admin_user,
            "is_chatgpt_user": self.is_chatgpt_user,
            "___scheme_version": self.__scheme_version
        }
        return user_dict
