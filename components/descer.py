import twitchio
from twitchio.ext import commands

class Descer(commands.Component):
    def __init__(self, database):
        self.setupquery = """CREATE TABLE IF NOT EXISTS characterdescs(id INTEGER PRIMARY KEY, charactername TEXT UNIQUE, desc TEXT)"""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command(aliases=["describe"])
    async def desc(self, ctx: commands.Context, *, details:str) -> None:
        """Set your description. ex: !desc This here is a bristly hobgoblin."

        !desc !describe
        """
        reply = ""
        details = details[:450]
        charname = ctx.chatter.display_name.rstrip()
        descIsBlank = (details.rstrip() == "")
        if descIsBlank: #functions as '!look me'
            query = "SELECT desc FROM characterdescs WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (charname))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"{charname} is nondescript."
                    else:
                        reply = f"[{charname}]: {row[0]}"
        else: 
            query = """INSERT OR REPLACE INTO characterdescs (charactername, desc) VALUES (?, ?)"""
            async with self.database.acquire() as connection:
                await connection.execute(query, (charname, details))
            reply = f"desc set: {details}"
        await ctx.reply(reply)

