import twitchio
from twitchio.ext import commands

class LocalPrinter(commands.Component):
    def __init__(self):
        self.setupquery = ""

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

