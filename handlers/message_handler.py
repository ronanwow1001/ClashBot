import discord
import config
import asyncio
import re
import tldextract
import urlextract
import traceback
import handlers.db_handler as db
import handlers.command_handler as CommandHandler

class MessageHandler():
    def __init__(self, client):
        self.client = client
        self.extractor = urlextract.URLExtract()
        self.command_handler = CommandHandler.CommandHandler(client)

    # Return true to tell it to not handle anything after
    async def on_message(self, message):
        if message.author.bot:
            return False
        if await self.handle_link(message):
            return True
        await self.handle_react(message)
        if await self.command_handler.on_message(message):
            return True
        return False

    async def respond(self, message, response):
        if response is None or response is '':
            return
        await self.client.send_message(message.channel, response)

    async def delete_message(self, message, reason=None):
        logm = 'deleting message \n```' + message.content + '``` by <@' + message.author.id + '> (`' + message.author.id + '`)'
        if reason is not None:
            logm += "\nReason: " + reason
        await self.log_message(logm)
        await self.client.delete_message(message)

    async def log_message(self, response):
        await self.client.send_message(self.client.get_channel(config.logs_id), response)

    async def handle_link(self, message):
        should_delete = False
        bad_domains = []

        # Check to see if there are URLs at all
        if self.extractor.has_urls(message.content.replace('`', '')):
            for word in message.content.split():
                print(word)
                word = word.replace('`', '')
                print(word)
                # set a variable so nested foreach's can choose to not delete message
                should_stop = False
                if not self.extractor.has_urls(word):
                    continue
                sub, sld, tld = tldextract.extract(word)
                if sld.lower() + '.' + tld.lower() in config.allowed_domains:
                    continue
                for chid, lst in config.allowed_channel_domains.items():
                    if chid == message.channel.id and sld.lower() + '.' + tld.lower() in lst:
                        should_stop = True
                if should_stop:
                    continue
                bad_domains.append(sld + '.' + tld)
                should_delete = True
        for role in message.author.roles:
            if role.name.lower() in config.links_allowed_roles:
                should_delete = False
        if should_delete:
            db.add_link_infraction(message.author.id)
            if db.get_link_infractions(message.author.id) == 1:
                links_plural = ""
            else:
                links_plural = "s"
            linkembed = discord.Embed(
            title="LINK INFRACTION",
            type='rich',
            description="We've deleted your message in the Altis Discord because it contained a link to {}, please see the allowed domains below".format(', '.join(bad_domains)),
            colour=discord.Colour.red()
            )
            linkembed.add_field(name='Current Infractions', value="{} infraction{}".format(db.get_link_infractions(message.author.id), links_plural))
            linkembed.add_field(name='Allowed Domains', value="projectalt.is\nprojectaltis.com")
            linkembed.add_field(name='Allowed in #ToonHQ', value="youtube.com\nyoutu.be")
            if len(bad_domains) >= 2:
                await self.delete_message(message,
                                          'Contained links to `' + '` and `'.join(bad_domains) + '`\nThe user now has `'
                                          + str(db.get_link_infractions(message.author.id)) + '` URL infractions.'
                                          )
                await self.client.send_message(message.author, embed=linkembed)
                                               #'We deleted your message in the Altis Discord becaused it contained links to `'
                                               #+ '` and `'.join(bad_domains) + '`. Please remember that only links to '
                                               #+ ' and '.join(config.allowed_domains) + ' are allowed in the Altis discord.'
                                               #)
            else:
                await self.delete_message(message,
                                          'Contained link to ' + '` and `'.join(bad_domains) + '\nThe user now has `'
                                          + str(db.get_link_infractions(message.author.id)) + '` URL infractions.'
                                          )
                await self.client.send_message(message.author, embed=linkembed)
                                               #'We deleted your message in the Altis Discord because it contained a link to '
                                               #+ '` and `'.join(bad_domains) + '. Please remember that only links to '
                                               #+ 'projectaltis.com and projectalt.is are allowed in the Altis discord.'
                                               #)
            return True
        return False

    async def handle_react(self, message):
        try:
            for key, value in config.reaction_channels.items():
                if message.channel.id == key:
                    for emoji in value:
                        await self.client.add_reaction(message, emoji)
                    db.add_link_infraction(message.author.id)
        except:
            print(traceback.format_exc())
