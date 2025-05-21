#!/usr/bin/python

import asyncio
import logging
import sqlite3

import asqlite
import twitchio
from twitchio.ext import commands
from twitchio import eventsub

from components.bot import Bot

LOGGER: logging.Logger = logging.getLogger("Bot")

def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, Bot(token_database=tdb) as bot:
            await bot.setup_database()
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()
