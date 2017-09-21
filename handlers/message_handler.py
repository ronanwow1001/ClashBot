import discord
import config
import asyncio
import re
import tldextract
import urlextract


class MessageHandler():
    def __init__(self, client):
        self.client = client
        self.extractor = urlextract.URLExtract()

    async def on_message(self, message):
        if message.author.bot:
            return
        if await self.handle_link(message):
            return

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
            bad_domains = self.extractor.find_urls(message.content)
            for allowed in config.allowed_domains:
                while allowed in bad_domains:
                    bad_domains.remove(allowed)
                if len(bad_domains) >= 1:
                    should_delete = True
        if should_delete:
            if len(bad_domains) >= 2:
                await self.delete_message(message, 'Contained links to ' + '` and `'.join(bad_domains))
            else:
                await self.delete_message(message, 'Contained link to ' + '` and `'.join(bad_domains))
            return True
        return False
