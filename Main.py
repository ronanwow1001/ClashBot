import discord
import asyncio
from handlers import message_handler
from handlers import reaction_handler
from handlers import invasion_handler
import config
import time
import traceback
from raven import Client as ravenClient

enable_error_reports = False
if config.sentry_dsn is not '':
    errorReporter = ravenClient(config.sentry_dsn)
    enable_error_reports = True

client = discord.Client()
MessageHandler = message_handler.MessageHandler(client)
ReactionHandler = reaction_handler.ReactionHandler(client)
InvasionHandler = invasion_handler.InvasionHandler(client)

@client.event
async def invtracker():
    try:
        await client.wait_until_ready()
        await InvasionHandler.tracker()
    except:
        if enable_error_reports:
            errorReporter.captureException()
        print(traceback.format_exc())

@client.event
async def stracker():
    try:
        await client.wait_until_ready()
        await InvasionHandler.statustracker()
    except:
        if enable_error_reports:
            errorReporter.captureException()
        print(traceback.format_exc())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('#1234')

@client.event
async def on_message(message):
    try:
        await MessageHandler.on_message(message)
    except:
        if enable_error_reports:
            errorReporter.captureException()
        print(traceback.format_exc())

@client.event
async def on_reaction_add(reaction, user):
    await ReactionHandler.on_reaction_add(reaction, user)


def Main():
    try:
        client.loop.create_task(invtracker())
        client.loop.create_task(stracker())
        client.run(config.discord_token)
    except:
        if enable_error_reports:
            errorReporter.captureException()
        print(traceback.format_exc())
        time.sleep(3)


if __name__ == '__main__':
    Main()
