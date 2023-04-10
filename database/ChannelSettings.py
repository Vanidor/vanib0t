class ChannelSettings():
    ''' Class representing channel settings '''
    channel_id: str
    display_name: str
    feature_chatgpt: int
    feature_fishh: str
    feature_streamschedule: bool

    def __init__(self,
                 channel_id,
                 display_name,
                 feature_chatgpt,
                 feature_fishh,
                 feature_streamschedule):
        self.channel_id = channel_id
        self.display_name = display_name
        self.feature_chatgpt = feature_chatgpt
        self.feature_fishh = feature_fishh
        self.feature_streamschedule = feature_streamschedule
        self.__scheme_version = "1.0.0.0"

    def __str__(self) -> str:
        channel_json = {
            "id": self.channel_id,
            "display_name": self.display_name,
            "features": {
                "chatgpt": self.feature_chatgpt,
                "fishh": self.feature_fishh,
                "stream": self.feature_streamschedule
            },
            "___scheme_version": self.__scheme_version
        }
        return str(channel_json)
