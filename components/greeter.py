import twitchio
from twitchio.ext import commands

class Greeter(commands.Component):
    def __init__(self, database):
        self.setupquery = ""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command(aliases=["hello", "greetings"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def greet(self, ctx: commands.Context) -> None:
        """Greets the command invoker

        !greet !hello !greetings
        """
        beginning = ""
        chartitle = ""
        charhon = ""
        ending = ""
        ending += "!"
        async with self.database.acquire() as connection:
            async with connection.cursor() as cursor:
                charname = ctx.chatter.display_name.rstrip()
                query = "SELECT title, honorific FROM charactertitles WHERE lower(charactername) = (?)"
                await cursor.execute(query, (charname))
                row: [sqlite3.Row] = await cursor.fetchone()
                if row is None:
                    reply = f"Hello {ctx.chatter.display_name}!"
                else:
                    if row[0] is not None:
                        chartitle = row[0]
                        beginning = f"{chartitle} "
                    if row[1] is not None:
                        charhon = row[1]
                        ending = f" {charhon}!"
                reply = f"Hello {beginning}{ctx.chatter.display_name}{ending}"
        await ctx.reply(reply)
