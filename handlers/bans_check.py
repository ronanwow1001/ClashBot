import discord
import asyncio
import config
import traceback
import handlers.db_handler as db

class BanCheck():
    def __init__(self, client):
        self.client = client

    async def check_bans(self, mentioned_user_id):
        self.count = db.get_bans_count(mentioned_user_id)
        if self.count >= 2:
            bans = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has {} bans. You should terminate them permanently.".format(mentioned_user_id, self.count),
            colour=discord.Colour.red()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=bans)
        else:
            pass
