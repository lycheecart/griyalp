import twitchio
from twitchio.ext import commands

class Looker(commands.Component):
    def __init__(self, database):
        self.setupquery = ""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command(aliases=["l", "examine"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def look(self, ctx: commands.Context, *, lookTarget:str = "") -> None:
        """Looks at a single target

        !look !l !examine
        """
        reply = ""
        lookTarget = lookTarget[:25] #max username length
        lookTarget = lookTarget.lower().rstrip()
        if (" " in lookTarget or lookTarget == ""):
            reply = f"{ctx.chatter.mention} looks around."
        else:
            if lookTarget.lower().rstrip() == "me":
                lookTarget = ctx.chatter.display_name.lower().rstrip()
            query = "SELECT desc FROM characterdescs WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (lookTarget))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"{lookTarget} is nondescript."
                    else:
                        reply = f"[{lookTarget}]: {row[0]}"
        await ctx.reply(reply)
