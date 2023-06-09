import asyncio
import discord
import orjson
from helpers.logger import Logger

with open('config.json', 'rb') as f:
    config = orjson.loads(f.read())

log = Logger('purger')


bot = discord.Client(
    self_bot=True,
    chunk_guilds_at_startup=False,
    request_guilds=False,
)


@bot.event
async def on_ready():
    log.info(f'Online | {bot.user.name}#{bot.user.discriminator} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    if message.content == config['message']:
        async for msg in message.channel.history(limit=None):
            if msg.author == bot.user:
                try:
                    await msg.delete()
                    log.success(f'Deleted | {msg.content} ({msg.id}) @ {get_channel_name(msg.channel)} ({msg.channel.id})')
                except Exception:
                    log.error(f'Failed to delete | {msg.content} ({msg.id}) @ {get_channel_name(msg.channel)} ({msg.channel.id})')

    await asyncio.sleep(300)
    try:
        await message.delete()
        log.success(f'Deleted | {message.content} ({message.id}) @ {get_channel_name(message.channel)} ({message.channel.id})')
        await asyncio.sleep(5)
    except Exception:
        log.error(f'Failed to delete | {message.content} ({message.id}) @ {get_channel_name(message.channel)} ({message.channel.id})')
        await asyncio.sleep(10)
        try:
            await message.delete()
            log.success(f'Deleted | {message.content} ({message.id}) @ {get_channel_name(message.channel)} ({message.channel.id})')
        except Exception:
            log.error(f'Failed to delete again | {message.content} ({message.id}) @ {get_channel_name(message.channel)} ({message.channel.id})')


def get_channel_name(channel):
    if isinstance(channel, discord.DMChannel):
        return f'{channel.recipient.name}#{channel.recipient.discriminator}'
    elif isinstance(channel, (discord.GroupChannel, discord.TextChannel)):
        return channel.name
    else:
        return 'Unknown'


bot.run(config['token'], log_level=None, reconnect=True, log_handler=None)
