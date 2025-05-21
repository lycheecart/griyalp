import os

class Secrets():
    def __init__(self):
        self.CLIENT_ID = os.getenv("CLIENT_ID") # client id from twitch dev console
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET") #client secret from twitch dev console
        self.BOT_ID = os.getenv("BOT_ID") #twitch account id of bot user
        self.OWNER_ID = os.getenv("OWNER_ID") #twitch account id of bot owner
