import asyncio

import discord
import orjson
import uvloop

from helpers.logger import Logger

with open('config.json', 'rb') as f:
    config = orjson.loads(f.read())

logger = Logger('purger')

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Purger(discord.Client):
    def __init__(self):
        super().__init__(
            chunk_guilds_at_startup=False, request_guilds=False, self_bot=True
        )

    async def on_ready(self):
        logger.info(f'Online | {self.user.name} ({self.user.id})')

    async def purge_messages(self, message):
        if message.content == config['message']:
            async for msg in message.channel.history(limit=None):
                if msg.author == self.user:
                    try:
                        await msg.delete()
                        logger.success(
                            f'Deleted | {msg.content} ({msg.id}) @ {self.get_channel_name(msg.channel)} ({msg.channel.id})'
                        )
                    except Exception:
                        logger.error(
                            f'Failed to delete | {msg.content} ({msg.id}) @ {self.get_channel_name(msg.channel)} ({msg.channel.id})'
                        )

        await asyncio.sleep(300)

        try:
            await message.delete()
            logger.success(
                f'Deleted | {message.content} ({message.id}) @ {self.get_channel_name(message.channel)} ({message.channel.id})'
            )
            await asyncio.sleep(5)
        except Exception:
            logger.error(
                f'Failed to delete | {message.content} ({message.id}) @ {self.get_channel_name(message.channel)} ({message.channel.id})'
            )
            await asyncio.sleep(10)
            try:
                await message.delete()
                logger.success(
                    f'Deleted | {message.content} ({message.id}) @ {self.get_channel_name(message.channel)} ({message.channel.id})'
                )
            except Exception:
                logger.error(
                    f'Failed to delete again | {message.content} ({message.id}) @ {self.get_channel_name(message.channel)} ({message.channel.id})'
                )

    def get_channel_name(self, channel):
        if isinstance(channel, discord.DMChannel):
            return channel.recipient.name
        elif isinstance(channel, (discord.GroupChannel, discord.TextChannel)):
            return channel.name
        else:
            return 'Unknown'

    async def on_message(self, message):
        if message.author == self.user:
            await self.purge_messages(message)


if __name__ == '__main__':
    bot = Purger()
    bot.run(config['token'], log_handler=None, log_level=None, reconnect=True)
