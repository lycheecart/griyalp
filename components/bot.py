import twitchio
from twitchio.ext import commands
from twitchio import eventsub
import asqlite
import logging

from .secrets import Secrets
from .localprinter import LocalPrinter
from .greeter import Greeter

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
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)
            for comp in list(self._components.values()):
                if len(comp.setupquery) > 0:
                    await connection.execute(comp.setupquery)


    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

