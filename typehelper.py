#####################
#
# Helping to annotate types within ClashBot. Great for pycharm development and doesn't impact runtime functionality.
#
# Created by Judge2020 on 10/17/2017
# https://judge2020.com
#
# Created for "ClashBot", which is property of Toontown: Corporate Clash.
# https://corpclash.com
#
#
# We trust that the passed paramater is correct, so if something is incorrectly passed it throws an exception.
#####################


import discord
from typing import NewType


__member = NewType('member', discord.Member)
def Member(member):
    return __member(member)


__message = NewType('message', discord.Message)
def Message(message):
    return __message(message)


__author = NewType('author', discord.Member)
def Author(author):
    return __author(author)
