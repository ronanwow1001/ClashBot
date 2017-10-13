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

    # Return true to tell it to not handle anything after
    async def on_message(self, message):
        if message.author.bot:
            return False
        if message.content.startswith(config.command_prefix + 'status'):
            await self.command_status(message)
            return True


    async def command_status(self, message):
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
        await self.client.send_message(message.channel, embed=embed)
