import discord
import asyncio
import config
import time
import traceback
import json
import requests


class InvasionHandler():
    def __init__(self, client):
        self.client = client

    async def tracker(self):
        await self.client.wait_until_ready()
        messagelive = False
        while True == True:
            data = requests.get('https://www.corpclash.com/api/invasion')
            invdata = json.loads(data.text)

            # Setting vars for use later
            district_name = ""
            invasion_cog = ""
            invasion_counter = ""
            invasion_live = False

            try: #Checks to see if there is any districts
                for district in invdata['districts']: #  Loops through the districts on the API
                    districtvalues = district.values() # Gets the values from the district.

                	# Getting district name, might be used later
                    for apikey in district:
                        districtname = apikey

                	# Starting invasion check
                    for valueloop in districtvalues:
                        if type(valueloop['invasion']) is dict: # Checking if district has a invasion
                            invasion_live = True
                            disval = valueloop['invasion'] # Less typing
                            district_name = district_name + "{}\n".format(districtname)# Adding the district name to the var above
                            if disval['cog'] == 'Sellbot Department Invasion':
                                invasion_cog = invasion_cog + "Sellbot Department\n"
                            elif disval['cog'] == 'Cashbot Department Invasion':
                                invasion_cog = invasion_cog + "Cashbot Department\n"
                            elif disval['cog'] == 'Lawbot Department Invasion':
                                invasion_cog = invasion_cog + "Lawbot Department\n"
                            elif disval['cog'] == 'Bossbot Department Invasion':
                                invasion_cog = invasion_cog + "Bossbot Department\n"
                            elif disval['cog'] == 'Boardbot Department Invasion':
                                invasion_cog = invasion_cog + "Boardbot Department\n"
                            else:
                                invasion_cog = invasion_cog + "{}\n".format(disval['cog'])
                            invasion_counter = invasion_counter + "{}/{} - {} Min left\n".format(disval['defeated'], disval['size'], disval['left'])
                        else: # If there is no invasion
                            pass # Ignore this district
                if invasion_live == True:
                    invasion_tracker_embed = discord.Embed(
                    title="Invasion Tracker",
                    type='rich',
                    description="Updated every 15 seconds",
                    colour=discord.Colour.green()
                    )
                    invasion_tracker_embed.add_field(name='District', value=district_name)
                    invasion_tracker_embed.add_field(name='Cog', value=invasion_cog)
                    invasion_tracker_embed.add_field(name='Status', value=invasion_counter)
                    if messagelive == False:
                        message = await self.client.send_message(discord.Object(id=config.gameinfo), embed=invasion_tracker_embed)
                        message
                        messagelive = True
                    elif messagelive == True:
                        await self.client.edit_message(message, embed=invasion_tracker_embed)
                elif invasion_live == False:
                    district_name = "None"
                    invasion_cog = "None"
                    invasion_counter = "None"

                    invasion_tracker_embed = discord.Embed(
                    title="Invasion Tracker",
                    type='rich',
                    description="Updated every 15 seconds",
                    colour=discord.Colour.green()
                    )
                    invasion_tracker_embed.add_field(name='District', value=district_name)
                    invasion_tracker_embed.add_field(name='Cog', value=invasion_cog)
                    invasion_tracker_embed.add_field(name='Status', value=invasion_counter)
                    if messagelive == False:
                        message = await self.client.send_message(discord.Object(id=config.gameinfo), embed=invasion_tracker_embed)
                        message
                        messagelive = True
                    elif messagelive == True:
                        await self.client.edit_message(message, embed=invasion_tracker_embed)

            except: #If there's no districts print None for everything.
                district_name = "None"
                invasion_cog = "None"
                invasion_counter = "None"

                invasion_tracker_embed = discord.Embed(
                title="Invasion Tracker",
                type='rich',
                description="Updated every 15 seconds",
                colour=discord.Colour.green()
                )
                invasion_tracker_embed.add_field(name='District', value=district_name)
                invasion_tracker_embed.add_field(name='Cog', value=invasion_cog)
                invasion_tracker_embed.add_field(name='Status', value=invasion_counter)
                if messagelive == False: #Checks to see if this is the first message
                    message = await self.client.send_message(discord.Object(id=config.gameinfo), embed=invasion_tracker_embed)
                    message
                    messagelive = True
                elif messagelive == True: # Edit the message if there already is one
                    await self.client.edit_message(message, embed=invasion_tracker_embed)

            await asyncio.sleep(15) #Nap time for 15 seconds!


    async def statustracker(self):
        await self.client.wait_until_ready()
        messagelive = False
        while True:
            embed = discord.Embed(
                title='Corporate Clash Status',
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
            if messagelive == False:
                statusmessage = await self.client.send_message(discord.Object(id=config.gameinfo), embed=embed)
                statusmessage
                messagelive = True
            elif messagelive == True:
                await self.client.edit_message(statusmessage, embed=embed)
            await asyncio.sleep(120)
