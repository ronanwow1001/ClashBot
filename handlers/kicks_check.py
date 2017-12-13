import discord
import asyncio
import config
import traceback
import handlers.db_handler as db

class KickCheck():
    def __init__(self, client):
        self.client = client

    async def check_kicks(self, mentioned_user_id):
        self.count = db.get_kicks_count(mentioned_user_id)
        if self.count == 2:
            kicks1 = discord.Embed(
            title="Heads up",
            type='rich',
            description="This is <@{}> second kick. You might want to ban them".format(mentioned_user_id),
            colour=discord.Colour.orange()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=kicks1)
        elif self.count == 3:
            kicks2 = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has three kicks. You might want to ban them".format(mentioned_user_id),
            colour=discord.Colour.red()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=kicks2)
        elif self.count > 3:
            kicks3 = discord.Embed(
            title="Heads up",
            type='rich',
            description="User <@{}> currently has {} warnings. You should ban them".format(mentioned_user_id, self.count),
            colour=discord.Colour.red()
            )
            await self.client.send_message(discord.Object(id=config.logs_id), embed=kicks3)
        else:
            pass
