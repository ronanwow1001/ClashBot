import discord
import asyncio
import config
import traceback
import handlers.db_handler as db

class WarningCheck():
    def __init__(self, client):
        self.client = client

    async def check_warnings(self, mentioned_user_id):
        self.count = db.get_warning_count(mentioned_user_id)
        if self.count == 1:
            onewarning = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has one warning. You might want to kick them".format(mentioned_user_id),
            colour=discord.Colour.orange()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=onewarning)
        elif self.count == 2:
            twowarnings = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has two warnings. You might want to kick/ban them".format(mentioned_user_id),
            colour=discord.Colour.orange()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=twowarnings)
        elif self.count == 3:
            threewarnings = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has Three warnings. You should ban them".format(mentioned_user_id),
            colour=discord.Colour.red()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=threewarnings)
        elif self.count > 3:
            morewarnings = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has {} warnings. You should ban them".format(mentioned_user_id, self.count),
            colour=discord.Colour.red()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=morewarnings)
        else:
            pass
