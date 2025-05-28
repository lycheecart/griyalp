import twitchio
from twitchio.ext import commands

class Descer(commands.Component):
    def __init__(self, database):
        self.setupquery = """CREATE TABLE IF NOT EXISTS characterdescs(id INTEGER PRIMARY KEY, charactername TEXT UNIQUE, desc TEXT)"""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command(aliases=["describe"])
    async def desc(self, ctx: commands.Context) -> None:
        """Looks at a single target

        !look !l !examine
        """
        reply = ""
        msgArray = ctx.message.text.split(" ", 256) #ctx.args doesn't work
        numArgs = len(msgArray) - 1
        charname = ctx.chatter.display_name.rstrip()
        if (numArgs > 0):
            description = " ".join(msgArray[1:])
            query = """INSERT OR REPLACE INTO characterdescs (charactername, desc) VALUES (?, ?)"""
            async with self.database.acquire() as connection:
                await connection.execute(query, (charname, description))
            reply = f"desc set: {description}"
        else:
            query = "SELECT desc FROM characterdescs WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (charname))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"{charname} is nondescript."
                    else:
                        reply = f"{row[0]}"
        await ctx.reply(reply)

