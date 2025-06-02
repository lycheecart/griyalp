import twitchio
from twitchio.ext import commands

class Greeter(commands.Component):
    def __init__(self):
        self.setupquery = ""

    async def setupInserts(self):
        return

    @commands.command(aliases=["hello", "greetings"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def greet(self, ctx: commands.Context) -> None:
        """Greets the command invoker

        !hello, !greetings
        """
        await ctx.reply(f"Hello {ctx.chatter.mention}!")
