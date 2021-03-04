import datetime

class discord_msg:
    def __init__(self, mydict):
        self.timestamp = datetime.datetime(mydict['timestamp'])
        self.content = mydict['content']
