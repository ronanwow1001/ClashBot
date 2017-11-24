import discord
import config
import asyncio
import re
import tldextract
import urlextract
import traceback
import handlers.db_handler as db
import typehelper

class ReactionHandler():
    def __init__(self, client):
        self.client = client

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        mem = typehelper.Member(reaction.message.author)
        if reaction.message.channel.id not in config.reaction_channels.keys() or user.id == self.client.user.id:
            return
        if isinstance(reaction.emoji, discord.Emoji):
            print('Random non-unicode emoji sent >:(')
            return
        if reaction.emoji == '✅':
            db.add_suggestion_upvote(mem.id)
        if reaction.emoji == '❌':
            db.add_suggestion_downvote(mem.id)



    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        mem = typehelper.Member(reaction.message.author)
        if reaction.message.channel.id not in config.reaction_channels.keys():
            return
        if isinstance(reaction.emoji, discord.Emoji):
            print('Random non-unicode emoji removed >:(')
            return
        if reaction.emoji == '✅':
            db.remove_suggestion_upvote(mem.id)
        if reaction.emoji == '❌':
            db.remove_suggestion_downvote(mem.id)
