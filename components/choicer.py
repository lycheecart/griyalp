import twitchio
from twitchio.ext import commands
from random import choice as rchx

class Choicer(commands.Component):
    def __init__(self):
        self.setupquery = ""

    async def setupInserts(self):
        return

    @commands.command()
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def choice(self, ctx: commands.Context, *, choices:str) -> None:
        """Returns a random choice from a list

        !choice
        """
        await ctx.reply(f"{rchx(choices.split(" "))}")
