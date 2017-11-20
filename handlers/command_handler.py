import discord
import config
import asyncio
import re
import json
import tldextract
import urlextract
import traceback
import requests
import handlers.db_handler as db
from ratelimit import rate_limited
import typehelper

class CommandHandler():
    def __init__(self, client):
        self.client = client

    def _delete_first_two_words(self, phrase: str) -> str:
        s = phrase.split()
        s.pop(0)
        s.pop(0)
        return " ".join(s)

    # Return true to tell it to not handle anything after
    async def on_message(self, message):
        if message.author.bot:
            return False
        if message.content.lower() == config.command_prefix + 'status':
            await self.command_status(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'warn'):
            await self.command_warn(message)
            return True
        if message.content.lower().startswith(config.command_prefix + 'limit'):
            await self.command_limit(message)
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
        if message.content.lower().startswith(config.command_prefix + 'stats'):
            await self.command_stats(message)
            return True

    @rate_limited(2, 5)
    async def command_stats(self, message):
        if len(message.mentions) > 1:
            await self.client.send_message(message.channel, 'Please only mention one user!')
            return
        user = typehelper.Member(message.mentions[0] if len(message.mentions) == 1 else message.author)
        upvotes = db.get_suggestion_upvotes(user.id)
        downvotes = db.get_suggestion_downvotes(user.id)
        await self.client.send_message(message.channel, '%s has received approximately %s upvotes and %s total downvotes!' % (user.mention, upvotes, downvotes))

    @rate_limited(2, 5)
    async def command_ip(self, message):
        ip_help = """
<@{0.author.id}>
Once you log on through the launcher, it may come up with an IP whitelisting error.
To fix this, do the following:
```
1. Go to https://projectaltis.com
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
        me = """```
-=- In The Logs Channel =-=
-Warn @user Reason

Example:
-Warn @Ricky#3642 Being British

-User @user

Example:
-User @Ricky#3642

This would then show:
This user has 1 warnings!
Reasons:
Reason 1: Being British```
        """
        await self.client.send_message(message.channel, me)

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
            await self.client.send_message(message.channel, 'Please include a reason!')
            return
        response = self._delete_first_two_words(message.content)
        db.add_warning(user.id, response)
        await self.client.send_message(message.channel, 'Warned ' + user.mention + '! The user now has ' +
                                       str(db.get_warning_count(user.id)) + ' warnings.')
        infractions = db.get_warning_count(user.id)
        if infractions == 1:
            warnings_plural = ""
        else:
            warnings_plural = "s"
        warnembed = discord.Embed(
        title="WARNING",
        type='rich',
        description="You have been warned in the Project Altis discord.\nPlease read the rules: <#{}>".format(config.rules_id),
        colour=discord.Colour.red()
        )
        warnembed.add_field(name='Reason', value=response)
        warnembed.add_field(name='Total Warnings', value="{} warning{}!".format(str(infractions), warnings_plural))
        #await self.client.send_message(user, 'You have been warned in the Altis discord. Reason: \n' + response)
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
        await self.client.send_message(message.channel, 'User ' + user.mention + 'has been assigned the Rule15 role')
        #db.add_warning(user.id, response)
        if len(config.limited_channels) == 1:
            plural_check = "channel."
        else:
            plural_check = "channels."
        await self.client.send_message(user, "You have been restricted from contributing to the {} {}".format(', '.join(config.limited_channels), plural_check) + "\nThis is due to breaking rule 15 which can be viewed here: <#{}>".format(config.rules_id) + "\n\nIf you'd like to appeal, please send a Direct Message to <@{}>".format(379820496759554049))

    @rate_limited(2, 5)
    async def command_user(self, message):
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
        infractions = db.get_warning_count(user.id)
        links = db.get_link_infractions(user.id)
        for role in message.author.roles:
            if role.name.lower() == config.limiting_role:
                limiting_message = "**YES**"
            else:
                limiting_message = "**NO**"
        if infractions == 1:
            warnings_plural = ""
        else:
            warnings_plural = "s"
        if links == 1:
            links_plural = ""
        else:
            links_plural = "s"
        userembed = discord.Embed(
            title='@{}'.format(user),
            type='rich',
            description='Info for the user {}'.format(user),
            colour=discord.Colour.orange()
        )
        userembed.add_field(name='Warnings', value="They have {} warning{}!\n\n".format(str(infractions), warnings_plural) + db.get_warnings_text(user.id))
        userembed.add_field(name='Link Infractions', value='{} infraction{}'.format(links, links_plural))
        userembed.add_field(name='Rule 15 role?', value=limiting_message)
        await self.client.send_message(message.channel, embed=userembed)

    @rate_limited(2, 10)
    async def command_status(self, message):
        embed = discord.Embed(
            title='Project Altis Status',
            type='rich',
            description='Statuses. Main Game is manually updated while the rest are checked every 5 minutes.',
            url='https://status.projectalt.is',
            colour=discord.Colour.green()
        )
        req = requests.get("https://status.projectalt.is/api/v1/components")

        # 1 = operational
        # 2 = performance
        # 3 = partial outage
        # 4 = major outage
        worst_status = 1
        try:
            jsn = json.loads(req.text)
            for dta in jsn["data"]:
                if dta["status"] > worst_status:
                    worst_status = dta["status"]
                embed.add_field(name=dta["name"], value=dta["status_name"])
        except:
            print("Cachet API is dying with code " + str(req.status_code) + ": " + req.text)
            return
        # Set color appropriately based on the worst status
        embed.colour = {
            1: discord.Colour.green(),
            2: discord.Colour.blue(),
            3: discord.Colour.gold(),
            4: discord.Colour.dark_red()
        }[worst_status]
        await self.client.send_message(discord.Object(id=config.toonhq_id), message.author.mention)
        await self.client.send_message(discord.Object(id=config.toonhq_id), embed=embed)
