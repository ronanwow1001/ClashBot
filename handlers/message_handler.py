import discord
import config
import asyncio
import re
import tldextract

class MessageHandler():
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        print(message.content)

    async def respond(self, message, response):
        if response is None or response is '':
            return
        await self.client.send_message(message.channel, response)

    def delete_message(self, message, reason=None):
        logm = 'deleting message ' + message.content + ' by user ' + message.author.name + '(' + message.author.id + ')'
        if reason is not None:
            logm += "\nReason: " + reason
        self.log_message(logm)
        self.client.delete_message(message)

    async def log_message(self, response):
        await self.client.send_message(config.logs_id, response)

    async def handle_link(self, message):
        should_delete = False
        bad_domains = []
        for word in message.content:
            if re.match(config.link_regex, word):
                sub, sld, tld = tldextract.extract(word)
                if sld + '.' + tld in config.allowed_domains:
                    continue
                bad_domains.append(sld + '.' + tld)
                should_delete = True
        if should_delete:
            if len(bad_domains) >= 2:
                self.delete_message(message, 'Contained links to ' + ' and '.join(bad_domains))
            else:
                self.delete_message(message, 'Contained link to ' + ' and '.join(bad_domains))
