import asyncio

from src.bot.handlers import bot


if __name__ == '__main__':
    asyncio.run(bot.polling())
