import twitchio
from twitchio.ext import commands

class Looker(commands.Component):
    def __init__(self, database):
        self.setupquery = ""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command(aliases=["l", "examine"])
    async def look(self, ctx: commands.Context) -> None:
        """Looks at a single target

        !look !l !examine
        """
        reply = ""
        msgArray = ctx.message.text.split(" ", 100) #ctx.args doesn't work
        numArgs = len(msgArray) - 1
        if (numArgs == 1):
            charname = "".join(msgArray[1:]).rstrip() 
            if charname.lower().strip() == "me":
                charname = ctx.chatter.display_name.lower().rstrip()
            query = "SELECT desc FROM characterdescs WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (charname.lower()))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"{charname} is nondescript."
                    else:
                        reply = f"{row[0]}"
        else:
            reply = f"{ctx.chatter.mention} looks around."
        await ctx.reply(reply)
