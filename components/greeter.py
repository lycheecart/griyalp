import twitchio
from twitchio.ext import commands

class Greeter(commands.Component):
    def __init__(self):
        self.setupquery = ""

    @commands.command(aliases=["hello", "greetings"])
    async def greet(self, ctx: commands.Context) -> None:
        """Greets the command invoker

        !hello, !greetings
        """
        await ctx.reply(f"Hello {ctx.chatter.mention}!")
