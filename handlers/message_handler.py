import discord
import config
import asyncio
import re
import tldextract
import urlextract
import traceback
import handlers.db_handler as db
import handlers.command_handler as CommandHandler
import blacklist

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
        if await self.bad_word_checker(message):
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
            description="We've deleted your message in the Altis Discord because it contained a link to {}, please see the allowed domains below.".format(', '.join(bad_domains)),
            colour=discord.Colour.red()
            )
            linkembed.add_field(name='Current Infractions', value="{} infraction{}".format(db.get_link_infractions(message.author.id), links_plural))
            linkembed.add_field(name='Allowed Domains', value="projectalt.is\nprojectaltis.com")
            linkembed.add_field(name='Allowed in #ToonHQ', value="youtube.com\nyoutu.be")

            linkembedstaff = discord.Embed(
            title="LINK INFRACTION",
            type='rich',
            description="I've deleted a message in the Altis Discord because it contained a link to {}, please see the allowed domains below.".format(', '.join(bad_domains)),
            colour=discord.Colour.red()
            )
            linkembedstaff.add_field(name='User', value="@{}".format(message.author))
            linkembedstaff.add_field(name='Link', value="```{}```".format(', '.join(bad_domains)))
            linkembedstaff.add_field(name='Current Infractions', value="{} infraction{}".format(db.get_link_infractions(message.author.id), links_plural))
            linkembedstaff.add_field(name='Allowed Domains', value="projectalt.is\nprojectaltis.com")
            linkembedstaff.add_field(name='Allowed in #ToonHQ', value="youtube.com\nyoutu.be")
            if len(bad_domains) >= 2:
                await self.client.send_message(discord.Object(id=config.logs_id), embed=linkembedstaff)
                await self.client.delete_message(message)
                await self.client.send_message(message.author, embed=linkembed)
            else:
                await self.client.send_message(discord.Object(id=config.logs_id), embed=linkembedstaff)
                await self.client.delete_message(message)
                await self.client.send_message(message.author, embed=linkembed)
            return True
        return False

    async def bad_word_checker(self, message):
        bad_word = False #Auto the message to not having a swear word, innocent till proven guilty right?
        bw_chat_message = message.content.split(" ")#Splits messages into a list so we can check every word.
        #Comparing each word against the blacklist
        for msg in bw_chat_message: #Loop through words in chat message
            word_clean = ''.join(i for i in msg.lower() if  i in 'qwertyuiopasdfghjklzxcvbnm123456789')
            for bw in blacklist.bad_words:
                if word_clean == bw:
                    bad_word = True

        if bad_word == True:
            await self.client.delete_message(message)
            db.add_bot_warning(message.content)
            db.add_warning(message.author.id, "BOT - ID: {}".format(db.newid))

        #Warning message
        infractions = db.get_warning_count(message.author.id)
        if infractions == 1:
            warnings_plural = ""
        else:
            warnings_plural = "s"
        bwembed = discord.Embed(
        title="WARNING",
        type='rich',
        description="Our bot has detected you swearing!\nPlease remember no NFSW language is allowed in the Project Altis discord.\n\nIf this was a mistake please DM <@379820496759554049> and quote ID: {}\n".format(db.newid),
        colour=discord.Colour.red()
        )
        bwembed.add_field(name='Message', value="```{}```".format(message.content))
        bwembed.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))

        bwembedstaff = discord.Embed(
        title="WARNING",
        type='rich',
        description="Delete message from {}\nID: {}\n".format(message.author, db.newid),
        colour=discord.Colour.green()
        )
        bwembedstaff.add_field(name='Message', value="```{}```".format(message.content))
        bwembedstaff.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))

        #Send messages, log to database and delete the message
        if bad_word == True:
            await self.client.send_message(message.author, embed=bwembed)
            await self.client.send_message(discord.Object(id=config.logs_id), embed=bwembedstaff)




    async def handle_react(self, message):
        try:
            for key, value in config.reaction_channels.items():
                if message.channel.id == key:
                    for emoji in value:
                        await self.client.add_reaction(message, emoji)
                    db.add_link_infraction(message.author.id)
        except:
            print(traceback.format_exc())
