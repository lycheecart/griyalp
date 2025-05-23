import twitchio
from twitchio.ext import commands

class EmoteSuggester(commands.Component):
    def __init__(self, database):
        self.setupquery = """CREATE TABLE IF NOT EXISTS emotes(id INTEGER PRIMARY KEY, emote TEXT UNIQUE)"""
        self.database = database

    async def setupInserts(self):
        emotes = [
            "bark",
            "beckon",
            "beg",
            "boggle the mind",
            "bow",
            "burp ",
            "cheer",
            "chuckle",
            "cry",
            "curtsy",
            "drool",
            "flip the bird",
            "frown",
            "giggle",
            "grin",
            "growl",
            "hug",
            "laugh",
            "lean",
            "melt",
            "meow",
            "moo",
            "mutter",
            "nod",
            "pat",
            "point",
            "poke",
            "punt",
            "salute",
            "scream",
            "shake",
            "smile",
            "smirk",
            "sneer",
            "snort",
            "sob",
            "stare",
            "stomp",
            "strut",
            "thank",
            "tip your hat",
            "wave",
            "whine",
            "whistle",
            "wiggle",
            "wince",
            "yell like tarzan"
        ]
        query = "INSERT INTO emotes (emote) VALUES (?) ON CONFLICT(emote) DO NOTHING"
        async with self.database.acquire() as connection:
            for emote in emotes:
                await connection.execute(query, (emote))
        return

    @commands.command()
    async def emote(self, ctx: commands.Context) -> None:
        """Suggests an action for /me <emotes>

        !emote
        """
        q = "SELECT emote FROM emotes ORDER BY RANDOM() LIMIT 1;"
        async with self.database.acquire() as connection:
            row: [sqlite3.Row] = await connection.fetchone(q)
        await ctx.reply(f"It's a good time to {row[0]}.")
