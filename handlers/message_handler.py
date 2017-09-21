import discord
import config
import asyncio
import re
import tldextract
import urlextract
import traceback
import handlers.db_handler as db


class MessageHandler():
    def __init__(self, client):
        self.client = client
        self.extractor = urlextract.URLExtract()

    async def on_message(self, message):
        if message.author.bot:
            return
        if await self.handle_link(message):
            return
        await self.handle_react(message)

    async def respond(self, message, response):
        if response is None or response is '':
            return
        await self.client.send_message(message.channel, response)

    async def delete_message(self, message, reason=None):
        logm = 'deleting message \n```' + message.content + '``` by user `' + message.author.name + '` (`' + message.author.id + '`)'
        if reason is not None:
            logm += "\nReason: " + reason
        await self.log_message(logm)
        await self.client.delete_message(message)

    async def log_message(self, response):
        await self.client.send_message(self.client.get_channel(config.logs_id), response)

    async def handle_link(self, message):
        should_delete = False
        bad_domains = []
        if self.extractor.has_urls(message.content):
            for word in message.content.split():
                sub, sld, tld = tldextract.extract(word)
                if sld + '.' + tld in config.allowed_domains:
                    continue
                bad_domains.append(sld + '.' + tld)
                should_delete = True
        if should_delete:
            db.add_link_infraction(message.author.id)
            if len(bad_domains) >= 2:
                await self.delete_message(message, 'Contained links to ' + '` and `'.join(bad_domains) + '\nThe user now has `' + str(db.get_link_infractions(message.author.id)) + '` URL infractions.')
            else:
                await self.delete_message(message, 'Contained link to ' + '` and `'.join(bad_domains) + '\nThe user now has `' + str(db.get_link_infractions(message.author.id)) + '` URL infractions.')
            return True
        return False

    async def handle_react(self, message):
        if message.content.startswith(config.exclude_react_starting_character):
            print('excluded message "'+ message.content + '" from reactions')
            return
        try:
            for key, value in config.reaction_channels.items():
                if message.channel.id == key:
                    for emoji in value:
                        await self.client.add_reaction(message, emoji)
                    db.add_link_infraction(message.author.id)
        except:
            print(traceback.format_exc())
