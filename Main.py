import discord
import asyncio
from handlers import message_handler
from handlers import reaction_handler
from handlers import invasion_handler
import config
import time
import traceback

client = discord.Client()
MessageHandler = message_handler.MessageHandler(client)
ReactionHandler = reaction_handler.ReactionHandler(client)
InvasionHandler = invasion_handler.InvasionHandler(client)

@client.event
async def invtracker():
    await client.wait_until_ready()
    await InvasionHandler.tracker()

@client.event
async def stracker():
    await client.wait_until_ready()
    await InvasionHandler.statustracker()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    await MessageHandler.on_message(message)

@client.event
async def on_reaction_add(reaction, user):
    await ReactionHandler.on_reaction_add(reaction, user)


def Main():
    try:
        client.loop.create_task(invtracker())
        client.loop.create_task(stracker())
        client.run(config.discord_token)
    except:
        traceback.format_exc()
        time.sleep(3)


if __name__ == '__main__':
    Main()
