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
        if message.content.startswith(config.command_prefix + 'status'):
            await self.command_status(message)
            return True
        if message.content.startswith(config.command_prefix + 'warn'):
            await self.command_warn(message)
            return True
        if message.content.startswith(config.command_prefix + 'user'):
            await self.command_user(message)
            return True
        if message.content.startswith(config.command_prefix + 'help'):
            await self.command_help(message)
            return True
        if message.content.startswith(config.command_prefix + 'ip'):
            await self.command_ip(message)
            return True

    async def command_ip(self, message):
        ip_help = """
{0.author.mention}
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

        await self.client.send_message(discord.Object(id='347411900864135189'), ip_help)

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
        await self.client.send_message(user, 'You have been warned in the Altis discord. Reason: \n' + response)

    async def command_user(self, message):
        if len(message.mentions) != 1:
            await self.client.send_message(message.channel, 'Please (only) mention one user!')
            return
        user = message.mentions[0]
        infractions = db.get_warning_count(user.id)
        reason = "This user has " + str(infractions) + " warnings!\n" + db.get_warnings_text(user.id)
        await self.client.send_message(message.channel, reason)

    async def command_status(self, message):
        mention_user = "{0.author.mention}".format(message)
        embed = discord.Embed(
            title='Project Altis Status',
            type='rich',
            description='Statuses for the game. Some are updated automatically.',
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
        # Set color appropriately based on the worst status
        embed.colour = {
            1: discord.Colour.green(),
            2: discord.Colour.blue(),
            3: discord.Colour.gold(),
            4: discord.Colour.dark_red()
        }[worst_status]
        await self.client.send_message(discord.Object(id='347411900864135189'), mention_user)
        await self.client.send_message(discord.Object(id='347411900864135189'), embed=embed)
