import twitchio
from twitchio.ext import commands

class Titler(commands.Component):
    def __init__(self, database):
        self.setupquery = """CREATE TABLE IF NOT EXISTS charactertitles(id INTEGER PRIMARY KEY, charactername TEXT UNIQUE, title TEXT, honorific TEXT)"""
        self.database = database

    async def setupInserts(self):
        return

    @commands.command()
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def title(self, ctx: commands.Context, *, titleText:str="") -> None:
        """Set your prefix- title to Ms, Mr, Lady, Lord, and more. ex !title Señora

        !title
        """
        reply = ""
        titleText = titleText[:450]
        charname = ctx.chatter.display_name.rstrip()
        argless = (titleText.rstrip() == "")
        if argless: #as !greet
            charname = ctx.chatter.display_name.rstrip()
            chartitle = ""
            charhon = ""
            ending = ""
            ending += "!"
            query = "SELECT title, honorific FROM charactertitles WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (charname))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"Hello {ctx.chatter.display_name}!"
                    else:
                        if row[0] is not None:
                            chartitle = row[0]
                        if row[1] is not None:
                            charhon = row[1]
                            ending = f" {charhon}!"
                    reply = f"Hello {chartitle} {ctx.chatter.display_name}{ending}"
        else: 
            query = """
            INSERT INTO charactertitles (charactername, title)
            VALUES (?, ?)
            ON CONFLICT(charactername)
            DO UPDATE SET
                title = excluded.title
            """
            async with self.database.acquire() as connection:
                await connection.execute(query, (charname, titleText))
            reply = f"title set: {titleText} {charname}"
        await ctx.reply(reply)

    @commands.command(aliases=["hon"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def honorific(self, ctx: commands.Context, *, honText:str="") -> None:
        """Set your honorific suffix eg san, sahab. ex !honorific the great and terrible 

        !honorific
        """
        reply = ""
        honText = honText[:450]
        charname = ctx.chatter.display_name.rstrip()
        argless = (honText.rstrip() == "")
        if argless: #as !greet
            charname = ctx.chatter.display_name.rstrip()
            chartitle = ""
            charhon = ""
            ending = ""
            ending += "!"
            query = "SELECT title, honorific FROM charactertitles WHERE lower(charactername) = (?)"
            async with self.database.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, (charname))
                    row: [sqlite3.Row] = await cursor.fetchone()
                    if row is None:
                        reply = f"Hello {ctx.chatter.display_name}!"
                    else:
                        if row[0] is not None:
                            chartitle = row[0]
                        if row[1] is not None:
                            charhon = row[1]
                            ending = f" {charhon}!"
                    reply = f"Hello {chartitle} {ctx.chatter.display_name}{ending}"
        else: 
            query = """
            INSERT INTO charactertitles (charactername, honorific)
            VALUES (?, ?)
            ON CONFLICT(charactername)
            DO UPDATE SET
                honorific = excluded.honorific
            """
            async with self.database.acquire() as connection:
                await connection.execute(query, (charname, honText))
            reply = f"honorific set: {charname} {honText}"
        await ctx.reply(reply)

    @commands.command(aliases=["unhon", "unhonorific"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def untitle(self, ctx: commands.Context) -> None:
        """Delete your titles and honorifics

        !untitle !unhonorific !unhon
        """
        charname = ctx.chatter.display_name.rstrip()
        query = "DELETE FROM charactertitles WHERE charactername = (?)"
        async with self.database.acquire() as connection:
            await connection.execute(query, (charname))
        await ctx.reply(f"Titles cleared.")
