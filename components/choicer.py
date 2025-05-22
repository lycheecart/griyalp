import twitchio
from twitchio.ext import commands
from random import choice as rchx

class Choicer(commands.Component):
    def __init__(self):
        self.setupquery = ""

    async def setupInserts(self):
        return

    @commands.command()
    async def choice(self, ctx: commands.Context) -> None:
        """Returns a random choice from a list

        !choice
        """
        choices = ctx.message.text.split(" ", 52)[1:] #ctx.args doesn't work 
        await ctx.reply(f"{rchx(choices)}")
