import discord
import config
import asyncio
import re
import json
import tldextract
import urlextract
import traceback
import requests
import subprocess
import handlers.db_handler as db
from ratelimit import rate_limited
import typehelper
import blacklist
from handlers.warning_check import WarningCheck
from handlers.kicks_check import KickCheck
from handlers.bans_check import BanCheck

class CommandHandler():
    def __init__(self, client):
        self.client = client

    def _delete_first_word(self, phrase: str) -> str:
        s = phrase.split()
        s.pop(0)
        return " ".join(s)

    def _delete_first_two_words(self, phrase: str) -> str:
        s = phrase.split()
        s.pop(0)
        s.pop(0)
        return " ".join(s)

    def _delete_first_three_words(self, phrase: str) -> str:
        s = phrase.split()
        s.pop(0)
        s.pop(0)
        s.pop(0)
        return " ".join(s)

    def _delete_first_four_words(self, phrase: str) -> str:
        s = phrase.split()
        s.pop(0)
        s.pop(0)
        s.pop(0)
        s.pop(0)
        return " ".join(s)

    # Return true to tell it to not handle anything after
    async def on_message(self, message):
        if message.author.bot:
            return False
        if message.author.id == '189833080092098560':
            return False
        if message.content.lower() == config.command_prefix + 'stats':
            await self.command_stats(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'unban'):
            await self.command_unban(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'ban'):
            await self.command_ban(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'kick'):
            await self.command_kick(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'warn'):
            await self.command_warn(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'limit'):
            await self.command_limit(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'unlimit'):
            await self.command_unlimit(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'artlimit'):
            await self.command_artlimit(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'artunlimit'):
            await self.command_artunlimit(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'user'):
            await self.command_user(message)
            return True
        if message.content.lower() == config.command_prefix + 'help':
            await self.command_help(message)
            return True
        if message.content.lower() == config.command_prefix + 'ip':
            await self.command_ip(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'id'):
            await self.command_bot(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'reboot'):
            await self.command_reboot(message)
            return True

    @rate_limited(2, 5)
    async def command_stats(self, message):
        if len(message.mentions) > 1:
            await self.client.send_message(message.channel, 'Please only mention one user!')
            return
        user = typehelper.Member(message.mentions[0] if len(message.mentions) == 1 else message.author)
        upvotes = db.get_suggestion_upvotes(user.id)
        downvotes = db.get_suggestion_downvotes(user.id)
        statsembed123 = discord.Embed(
        title="Stats for {}".format(user),
        type='rich',
        description="{} had received approximately".format(user),
        colour=discord.Colour.magenta()
        )
        statsembed123.add_field(name='Upvotes', value=upvotes)
        statsembed123.add_field(name='Downvotes', value=downvotes)
        await self.client.send_message(message.channel, embed=statsembed123)

    @rate_limited(2, 5)
    async def command_ip(self, message):
        ip_help = """
<@{0.author.id}>
Once you log on through the launcher, it may come up with an IP whitelisting error.
To fix this, do the following:
```
1. Go to https://corpclash.com
2. Log into the website using the account you needed to whitelist on
3. Click your account name in the top left corner
4. Search near the bottom of the page for the "Trusted IP's" section
5. Find your IP address and click accept!
```
If you see any IP's there which you don't recognise, please change your account password.
You're also welcome to disable the feature, however, we recommend you keep it enabled to keep the evil cogs out!
To find your IP address, click here to use Google's IP checker: https://goo.gl/search/ip
If you're having trouble locating the "Trusted IP's" section of the website, please refer to the following image: https://imgur.com/a/35LuQ
""".format(message)

        await self.client.send_message(discord.Object(id=config.toonhq_id), ip_help)

    @rate_limited(2, 7)
    async def command_help(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return

        embd = discord.Embed(
            title="Commands",
            type='rich',
            description="List of commands and their usage",
            colour=discord.Colour.purple()
        )
        embd.add_field(name='Type (<type>)', value="```Use 1 if you're attaching any rule in the <reason> field.``` ```Use 2 if you're attaching a typed explanation in the <reason>field.```".format(config.command_prefix))
        embd.add_field(name='Warn', value="```{}warn <@user's_id> <type> <reason>``` ```Warn a user with either <type>.```".format(config.command_prefix))
        embd.add_field(name='Kick', value="```{}kick <@user's_id> <type> <reason>``` ```Kick a user with either <type>.```".format(config.command_prefix))
        embd.add_field(name='Ban', value="```{}ban <@user's_id> <type> <#_days> <reason>``` ```Ban a user with either <type>, deleting the last <#_days> of their messages in the server.```".format(config.command_prefix))
        embd.add_field(name='Infraction Lookup', value="```{}id <id>``` ```Displays the data documented for the identified case.```".format(config.command_prefix))
        embd.add_field(name='User Information', value="```{}user <user's id>``` ```Displays any user's information.```".format(config.command_prefix))

        await self.client.send_message(discord.Object(id=config.logs_id), embed=embd)

    async def command_reboot(self, message):
        if message.author.id not in config.admins:
            return
        gitprocess = subprocess.check_output(['git', 'pull'])
        await self.client.send_message(message.author, 'Git pull output: \n```\n' + str(gitprocess) + '\n```\nGoing down for a reboot!')
        import os
        # assuming we're in the immortal auto-restart hypervisor (https://immortal.run)
        os._exit(0)

    @rate_limited(10, 3)
    async def command_kick(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        if len(message.content.split()) < 3:
            await self.client.send_message(message.channel, 'Please specify the type!')
            return
        if len(message.content.split()) < 4:
            await self.client.send_message(message.channel, 'Please include a reason!')
            return
        msgType = int(self._delete_first_two_words(message.content)[0])
        response = self._delete_first_three_words(message.content)
        if (msgType == 1):
            if (isinstance(response, int) == True):
                if (response <= len(config.rules)):
                    msgType = msgType
                else:
                    msgType = 2
            resp = int(response) - 1

        db.add_kick(user.id, response)
        await KickCheck(self.client).check_kicks(user.id)
        infractions = db.get_kicks_count(user.id)

        if infractions == 1:
            kicks_plural = ""
        else:
            kicks_plural = "s"

        if msgType > 1:
            kickedembed = discord.Embed(
            title="NOTICE",
            type='rich',
            description="You have been kicked from the Corporate Clash discord.\nPlease read the rules: <#{}>".format(config.rules_id),
            colour=discord.Colour.red()
            )
            kickedembed.add_field(name='Reason', value=response)
            kickedembed.add_field(name='Total Kicks', value="{}".format(str(infractions)))

            kickedstaff = discord.Embed(
            title="Kicked",
            type='rich',
            description="Done! {} has been kicked from the server".format(user),
            colour=discord.Colour.green()
            )
            kickedstaff.add_field(name='Reason', value='```{}```'.format(response))
            kickedstaff.add_field(name='Total Kicks', value="{} kick{}!".format(str(infractions), kicks_plural))
            kickedstaff.add_field(name='User ID', value="```{}```".format(user.id))
        else:
            kickedembed = discord.Embed(
            title="NOTICE",
            type='rich',
            description='You have been kicked from the Corporate Clash discord because you\'ve broken rule {}, this rule corresponds to "{}"'.format(response, config.rules[resp]),
            colour=discord.Colour.red()
            )
            kickedembed.add_field(name='Reason', value="Rule {}".format(response))
            kickedembed.add_field(name='Total Kicks', value="{}".format(str(infractions)))

            kickedstaff = discord.Embed(
            title="Kicked",
            type='rich',
            description="Done! {} has been kicked from the server".format(user),
            colour=discord.Colour.green()
            )
            kickedstaff.add_field(name='Reason', value='```{}```'.format(config.rules[resp]))
            kickedstaff.add_field(name='Total Kicks', value="{} kick{}!".format(str(infractions), kicks_plural))
            kickedstaff.add_field(name='User ID', value="```{}```".format(user.id))
        await self.client.send_message(discord.Object(id=config.logs_id), embed=kickedstaff)
        try:
            await self.client.send_message(user, embed=kickedembed)
            await self.client.kick(user)
        except:
            await self.client.kick(user)

    @rate_limited(10, 3)
    async def command_ban(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        if len(message.content.split()) < 3:
            await self.client.send_message(message.channel, 'Please specify the type!')
            return
        if len(message.content.split()) < 4:
            await self.client.send_message(message.channel, 'Please specify the number of days worth of messages to delete from the user in the server!')
            return
        if len(message.content.split()) < 5:
            await self.client.send_message(message.channel, 'Please include a reason!')
            return
        msgType = int(self._delete_first_two_words(message.content)[0])
        d_delete = int(self._delete_first_three_words(message.content)[0])
        response = self._delete_first_four_words(message.content)

        if (d_delete <= 0):
            d_delete = 0
        elif (d_delete >= 7):
            d_delete = 7
        else:
            d_delete = d_delete

        if (msgType == 1):
            if (isinstance(response, int) == True):
                if (response <= len(config.rules)):
                    msgType = msgType
                else:
                    msgType = 2
            resp = int(response) - 1

        db.add_ban(user.id, response)
        await BanCheck(self.client).check_bans(user.id)
        infractions = db.get_bans_count(user.id)

        if infractions == 1:
            bans_plural = ""
        else:
            bans_plural = "s"

        if msgType > 1:
            embd = discord.Embed(
            title="BAN",
            type='rich',
            description="You have been banned from the Corporate Clash discord because of repeated infractions to our policy.\nPlease read the rules: <#{}>".format(config.rules_id),
            colour=discord.Colour.red()
            )
            embd.add_field(name='Reason', value=response)
            embd.add_field(name='Total Bans', value="{}".format(str(infractions)))

            embdstaff = discord.Embed(
            title="Banned",
            type='rich',
            description="Done! {} has been banned from the server, the last {} days of their messages have been removed".format(user, d_delete),
            colour=discord.Colour.green()
            )
            embdstaff.add_field(name='Reason', value='```{}```'.format(response))
            embdstaff.add_field(name='Total Bans', value="{} ban{}!".format(str(infractions), bans_plural))
            embdstaff.add_field(name='User ID', value="```{}```".format(user.id))
        else:
            embd = discord.Embed(
            title="BAN",
            type='rich',
            description='You have been banned from the Corporate Clash discord because of repeated infractions to our policy, your latest being rule {}, this rule corresponds to "{}"'.format(response, config.rules[resp]),
            colour=discord.Colour.red()
            )
            embd.add_field(name='Reason', value="Rule {}".format(response))
            embd.add_field(name='Total Bans', value="{}".format(str(infractions)))

            embdstaff = discord.Embed(
            title="Banned",
            type='rich',
            description="Done! {} has been banned from the server, the last {} days of their messages have been removed".format(user, d_delete),
            colour=discord.Colour.green()
            )
            embdstaff.add_field(name='Reason', value='```Rule {}```'.format(config.rules[resp]))
            embdstaff.add_field(name='Total Bans', value="{} ban{}!".format(str(infractions), bans_plural))
            embdstaff.add_field(name='User ID', value="```{}```".format(user.id))
        await self.client.send_message(discord.Object(id=config.logs_id), embed=embdstaff)
        try:
            await self.client.send_message(user, embed=embd)
            await self.client.ban(user, d_delete)
        except:
            await self.client.ban(user, d_delete)

    @rate_limited(10, 3)
    async def command_unban(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return

        if len(message.content.split()) < 2:
            await self.client.send_message(message.channel, 'Please include the user\'s id!')
            return

        con = self._delete_first_word(message.content)
        user_id = str((con).split()[0])
        server_id = str(message.server.id)
        server = discord.Server(id=server_id)
        user = await self.client.get_user_info(user_id)

        if len(message.content.split()) < 3:
            await self.client.send_message(message.channel, 'Please include a reason!')
            return

        reason = self._delete_first_word(con)
        response = 'by {}'.format(message.author)

        db.add_unban(user_id, response)

        embdstaff = discord.Embed(
        title="Unbanned",
        type='rich',
        description="Done! User with id: {} has been unbanned from the server by {}".format(user_id, message.author),
        colour=discord.Colour.green()
        )
        embdstaff.add_field(name='Reason', value='```{}```'.format(reason))
        embdstaff.add_field(name='User ID', value="```{}```".format(user_id))

        await self.client.send_message(discord.Object(id=config.logs_id), embed=embdstaff)
        await self.client.unban(server, user)


    @rate_limited(10, 3)
    async def command_warn(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        if len(message.content.split()) < 3:
            await self.client.send_message(message.channel, 'Please specify the type!')
            return
        if len(message.content.split()) < 4:
            await self.client.send_message(message.channel, 'Please include a reason!')
            return
        msgType = int(self._delete_first_two_words(message.content)[0])
        response = self._delete_first_three_words(message.content)
        if (msgType == 1):
            if (isinstance(response, int) == True):
                if (response <= len(config.rules)):
                    msgType = msgType
                else:
                    msgType = 2
            resp = int(response) - 1
        db.add_warning(user.id, response)
        await WarningCheck(self.client).check_warnings(user.id)
        infractions = db.get_warning_count(user.id)
        if infractions == 1:
            warnings_plural = ""
        else:
            warnings_plural = "s"
        if msgType > 1:
            warnembed = discord.Embed(
            title="WARNING",
            type='rich',
            description="You have been warned in the Corporate Clash discord.\nPlease read the rules: <#{}>".format(config.rules_id),
            colour=discord.Colour.red()
            )
            warnembed.add_field(name='Reason', value=response)
            warnembed.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))

            warnedstaff = discord.Embed(
            title="Warned",
            type='rich',
            description="Done! {} has been warned".format(user),
            colour=discord.Colour.green()
            )
            warnedstaff.add_field(name='Reason', value='```{}```'.format(response))
            warnedstaff.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))
            warnedstaff.add_field(name='User ID', value="```{}```".format(user.id))
        else:
            warnembed = discord.Embed(
            title="WARNING",
            type='rich',
            description='You have been warned in the Corporate Clash discord because you\'ve broken rule {}, this rule corresponds to "{}"'.format(response, config.rules[resp]),
            colour=discord.Colour.red()
            )
            warnembed.add_field(name='Reason', value="Rule {}".format(response))
            warnembed.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))

            warnedstaff = discord.Embed(
            title="Warned",
            type='rich',
            description="Done! {} has been warned".format(user),
            colour=discord.Colour.green()
            )
            warnedstaff.add_field(name='Reason', value='```{}```'.format(config.rules[resp]))
            warnedstaff.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))
            warnedstaff.add_field(name='User ID', value="```{}```".format(user.id))
        await self.client.send_message(discord.Object(id=config.logs_id), embed=warnedstaff)
        await self.client.send_message(user, embed=warnembed)

    @rate_limited(10, 3)
    async def command_limit(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        giverole = discord.utils.get(message.server.roles, name=config.limiting_role)
        await self.client.add_roles(user, giverole)
        limitstaffembed = discord.Embed(
        title="Limited",
        type='rich',
        description="I have given {} the {} role!".format(user, config.limiting_role),
        colour=discord.Colour.green()
        )
        await self.client.send_message(message.channel, embed=limitstaffembed)
        if len(config.limited_channels) == 1:
            plural_check = "channel."
        else:
            plural_check = "channels."
        limitembed = discord.Embed(
        title="LIMITED",
        type='rich',
        description="You have been restricted from contributing to the {} {}\nThis is due to breaking rule 15 which can be viewed here: <#{}>\n\nIf you'd like to appeal, please send a Direct Message to <@{}>".format(', '.join(config.limited_channels), plural_check, config.rules_id, 379820496759554049),
        colour=discord.Colour.red()
        )
        await self.client.send_message(user, embed=limitembed)

    @rate_limited(10, 3)
    async def command_unlimit(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        removerole = discord.utils.get(message.server.roles, name=config.limiting_role)
        await self.client.remove_roles(user, removerole)
        if len(config.limited_channels) == 1:
            plural_check = "channel."
        else:
            plural_check = "channels."
        limitstaffembed = discord.Embed(
        title="Limited",
        type='rich',
        description="I have removed the {} role from {}".format(config.limiting_role, user),
        colour=discord.Colour.green()
        )
        limitembed = discord.Embed(
        title="Removed Limitation",
        type='rich',
        description="You are no longer limited from the {} {}".format(', '.join(config.limited_channels), plural_check),
        colour=discord.Colour.green()
        )
        await self.client.send_message(message.channel, embed=limitstaffembed)
        await self.client.send_message(user, embed=limitembed)

    @rate_limited(10, 3)
    async def command_artlimit(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        giverole = discord.utils.get(message.server.roles, name=config.artlimiting_role)
        await self.client.add_roles(user, giverole)
        limitstaffembed = discord.Embed(
        title="Limited",
        type='rich',
        description="I have given {} the {} role!".format(user, config.artlimiting_role),
        colour=discord.Colour.green()
        )
        await self.client.send_message(message.channel, embed=limitstaffembed)
        if len(config.limited_channels) == 1:
            plural_check = "channel."
        else:
            plural_check = "channels."
        limitembed = discord.Embed(
        title="LIMITED",
        type='rich',
        description="You have been restricted from contributing to the {} {}\nThis is due to breaking rule 15 which can be viewed here: <#{}>\n\nIf you'd like to appeal, please send a Direct Message to <@{}>".format(', '.join(config.artlimited_channels), plural_check, config.rules_id, 379820496759554049),
        colour=discord.Colour.red()
        )
        await self.client.send_message(user, embed=limitembed)

    @rate_limited(10, 3)
    async def command_artunlimit(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        removerole = discord.utils.get(message.server.roles, name=config.artlimiting_role)
        await self.client.remove_roles(user, removerole)
        if len(config.limited_channels) == 1:
            plural_check = "channel."
        else:
            plural_check = "channels."
        limitstaffembed = discord.Embed(
        title="Limited",
        type='rich',
        description="I have removed the {} role from {}".format(config.limiting_role, user),
        colour=discord.Colour.green()
        )
        limitembed = discord.Embed(
        title="Removed Limitation",
        type='rich',
        description="You are no longer limited from the {} {}".format(', '.join(config.artlimited_channels), plural_check),
        colour=discord.Colour.green()
        )
        await self.client.send_message(message.channel, embed=limitstaffembed)
        await self.client.send_message(user, embed=limitembed)

    @rate_limited(2, 5)
    async def command_user(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return

        if len(message.content.split()) < 2:
            await self.client.send_message(message.channel, 'Please include the user\'s id!')
            return

        con = self._delete_first_word(message.content)
        user_id = str((con).split()[0])
        user = await self.client.get_user_info(user_id)

        w_infractions = db.get_warning_count(user_id)
        k_infractions = db.get_kicks_count(user_id)
        b_infractions = db.get_bans_count(user_id)
        links = db.get_link_infractions(user_id)

        try:
            get_users_roles = [role.name for role in user.roles]
            for role in message.author.roles:
                if config.limiting_role in get_users_roles:
                    limiting_message = "**YES**"
                else:
                    limiting_message = "**NO**"
        except:
            # if the user isnt in the guild, they have no (guild) member object,
            # therefore don't need to be check for roles
            limiting_message = "**NO**"

        if b_infractions == 1:
            bans_plural = ""
        else:
            bans_plural = "s"
        if k_infractions == 1:
            kicks_plural = ""
        else:
            kicks_plural = "s"
        if w_infractions == 1:
            warnings_plural = ""
        else:
            warnings_plural = "s"
        if links == 1:
            links_plural = ""
        else:
            links_plural = "s"
        userembed = discord.Embed(
            title='Documented History / Information',
            type='rich',
            description='Username: {}\nUser ID: {}\nNickname: {}\nDoC: {}\nBot User?: {}'.format(user.name, user.id, user.display_name, user.created_at, user.bot),
            colour=discord.Colour.orange()
        )
        userembed.add_field(name='Warnings', value="They have {} warning{}!\n\n{}".format(str(w_infractions), warnings_plural, db.get_warnings_text(user_id)))
        userembed.add_field(name='Kicks', value="They have {} kick{}!\n\n{}".format(str(k_infractions), kicks_plural, db.get_kicks_text(user_id)))
        userembed.add_field(name='Bans', value="They have {} ban{}!\n\n{}".format(str(b_infractions), bans_plural, db.get_bans_text(user_id)))
        userembed.add_field(name='Link Infractions', value='{} infraction{}'.format(links, links_plural))
        userembed.add_field(name='Rule 15 role?', value=limiting_message)
        await self.client.send_message(message.channel, embed=userembed)


    @rate_limited(2, 5)
    async def command_bot(self, message):
        cont = False
        for role in message.author.roles:
            if role.name.lower() in config.warn_command_allowed_roles:
                cont = True
        if not cont:
            return
        warnid = self._delete_first_word(message.content)
        botwarning = db.get_bot_warns(warnid)
        botlookup = discord.Embed(
            title='ID Lookup',
            type='rich',
            description='Info for ID: {}'.format(warnid),
            colour=discord.Colour.green()
        )
        botlookup.add_field(name='Message', value="```{}```".format(botwarning))
        await self.client.send_message(message.channel, embed=botlookup)
