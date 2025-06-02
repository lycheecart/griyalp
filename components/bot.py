import twitchio
from twitchio.ext import commands
from twitchio import eventsub
import asqlite
import logging

from .secrets import Secrets
from .localprinter import LocalPrinter
from .greeter import Greeter
from .sigils import SigilChatter
from .choicer import Choicer
from .emotesuggester import EmoteSuggester
from .coolstory import CoolStory
from .descer import Descer
from .looker import Looker
from .dieroller import DieRoller

SECRETS = Secrets()
LOGGER: logging.Logger = logging.getLogger("Bot")

class Bot(commands.Bot):
    def __init__(self, *, token_database: asqlite.Pool) -> None:
        self.token_database = token_database
        super().__init__(
            client_id     = SECRETS.CLIENT_ID,
            client_secret = SECRETS.CLIENT_SECRET,
            bot_id   = SECRETS.BOT_ID,
            owner_id = SECRETS.OWNER_ID,
            prefix="!",
        )

    async def setup_hook(self) -> None:
        subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=SECRETS.OWNER_ID, user_id=SECRETS.BOT_ID)
        await self.subscribe_websocket(payload=subscription)

        subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=SECRETS.OWNER_ID)
        await self.subscribe_websocket(payload=subscription)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        #super() will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        async with self.token_database.acquire() as connection:
            rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        await self.add_component(LocalPrinter())
        await self.add_component(Greeter())
        await self.add_component(SigilChatter(self.token_database))
        await self.add_component(Choicer())
        await self.add_component(EmoteSuggester(self.token_database))
        await self.add_component(CoolStory())
        await self.add_component(DieRoller())
        await self.add_component(Descer(self.token_database))
        await self.add_component(Looker(self.token_database))
        await self.add_component(Helper(self)) #helper has to be loaded last
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)
            for comp in list(self._components.values()):
                if len(comp.setupquery) > 0:
                    await connection.execute(comp.setupquery)
        for comp in list(self._components.values()):
            await comp.setupInserts()

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

class Helper(commands.Component):
    def __init__(self, bot:Bot):
        self.setupquery = ""
        self.bot = bot

    async def setupInserts(self):
        return

    @commands.command(name="commands",aliases=["!commands", "!command"])
    @commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
    async def help_commands(self, ctx: commands.Context) -> None:
        """List the loaded commands

        !commands
        """
        helpstr = "!choice !emote !greet !sigil !coolstory !desc !look !roll"
        await ctx.reply(f"{helpstr}")


    @commands.group(name="help",invoke_fallback=False)
    async def help(self, ctx:commands.Context) -> None:
        """Command help

        !help
        """
        helpstr = "usage's !help <command_name> (without brackets). commands are listed with !commands"
        await ctx.reply(f"{helpstr}")

    @help.command(name="choice", aliases=["!choice"])
    async def help_choice(self, ctx: commands.Context) -> None:
        """Choose from the args (delimited by the space char ' ') ex: !choice a b c

        !help !choice, !help choice
        """
        helpstr = "Choose from the args (delimited by the space char ' ') ex: !choice a b c"
        await ctx.reply(f"{helpstr}")

    @help.command(name="emote", aliases=["!emote"])
    async def help_emote(self, ctx: commands.Context) -> None:
        """Suggest an emote for /me. ex: !emote; /me dances

        !help !emote, !help emote
        """
        helpstr = "Suggest an emote for /me. ex: !emote; /me dances"
        await ctx.reply(f"{helpstr}")

    @help.command(name="greet", aliases=["!greet"])
    async def help_greet(self, ctx: commands.Context) -> None:
        """The bot'll say hi to the command invoker

        !help !greet, !help greet
        """
        helpstr = "The bot'll say hi to the command invoker"
        await ctx.reply(f"{helpstr}")

    @help.command(name="sigil", aliases=["!glyph", "glyph", "!sigil"])
    async def help_greet(self, ctx: commands.Context) -> None:
        """Get a random sigil, or, glyph,

        !help !sigil, !help sigil
        """
        helpstr = "Get a random sigil, or, glyph,"
        await ctx.reply(f"{helpstr}")

    @help.command(name="coolstory", aliases=["!coolstory", "story", "!story"])
    async def help_greet(self, ctx: commands.Context) -> None:
        """The bot tells a cool story

        !coolstory !story
        """
        helpstr = "The bot tells a cool story."
        await ctx.reply(f"{helpstr}")

    @help.command(name="desc", aliases=["!desc", "describe", "!describe"])
    async def help_desc(self, ctx: commands.Context) -> None:
        """Set your description. ex: !desc This here is a bristly hobgoblin."

        !desc !describe
        """
        helpstr = "Set your description. ex: !desc This here is a bristly hobgoblin."
        await ctx.reply(f"{helpstr}")

    @help.command(name="look", aliases=["!look", "l", "!l"])
    async def help_look(self, ctx: commands.Context) -> None:
        """Look at a single character and see their appearance. ex: !look griyalp"

        !look !l
        """
        helpstr = "Look at a single character and see their appearance. ex: !look griyalp"
        await ctx.reply(f"{helpstr}")

    @help.command(name="roll", aliases=["!roll", "dieroll", "!dieroll"])
    async def help_look(self, ctx: commands.Context) -> None:
        """Roll XdY or XdYp or XdYe: ex !roll 5d6e

        !roll !dieroll
        """
        helpstr = "Roll XdY or XdYp or XdYe. ex !roll 5d6e"
        await ctx.reply(f"{helpstr}")
