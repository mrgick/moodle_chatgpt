from telethon import TelegramClient
import asyncio
from .settings import settings
import logging

logger = logging.getLogger(__name__)
client = TelegramClient("anon", settings.API_ID, settings.API_HASH)


async def get_gigachat_message(prompt="1 2 3 4 6 7 8 9 Какая цифра пропущена?"):
    async with client:
        logger.info(prompt)
        await client.start()
        await client.send_message(settings.CHANNEL, f"@gigachat_bot {prompt}")
        await asyncio.sleep(1)
        message = "@gigachat_bot"
        while "Запрос принят" in message or "@gigachat_bot" in message:
            async for m in client.iter_messages(settings.CHANNEL, limit=1):
                message = m.text
            await asyncio.sleep(1)
        logger.info(message)
        return message


if __name__ == "__main__":
    asyncio.run(get_gigachat_message())
