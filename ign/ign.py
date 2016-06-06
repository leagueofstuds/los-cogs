import os
import asyncio

import discord
from discord.ext import commands

from .utils.dataIO import fileIO
from __main__ import send_cmd_help
from .utils.chat_formatting import *

class IGN:
  """ share your in game names with the group """
  GAMES = ["LoLNA", "LoLEUW", "LoLOCE", "Battle.net", "GW2", "PSN", "Minecraft"]

  def __init__(self, bot):
    self.bot = bot
    self.names = fileIO("data/ign/names.json", "load")

  @commands.group(pass_context=True)
  async def ign(self, ctx):
    """ manage your in game names """
    if ctx.invoked_subcommand is None:
        await send_cmd_help(ctx)
        return

  @ign.command(name="whoami", pass_context=True)
  async def ign_whoami(self, ctx):
    """ see what IGNs you have added """
    user = ctx.message.author
    igns = self.names.get(user.mention)
    if not igns:
      await self.bot.say("You have not yet entered any IGN info. :cry:".format(user.mention))
    else:
      await self.bot.say(self.format_igns(user, igns))

  @ign.command(name="whois")
  async def ign_whois(self, user: discord.Member):
    """ get all IGNs for a member """
    igns = self.names.get(user.mention)
    if not igns:
      await self.bot.say("{0} has not yet entered any IGN info. :cry:".format(user.mention))
    else:
      await self.bot.say(self.format_igns(user, igns))

  @ign.command(name="whoplays", pass_context=True)
  async def ign_whoplays(self, ctx, game):
    """ list all members that play a certain game """
    supported_game = self.get_supported_game(game)
    if not supported_game:
      return await self.bot.say(self.format_supported_games())

    gamers = {}
    for player, games in self.names.items():
      if supported_game in games.keys():
        gamers.setdefault(player, games[supported_game])

    msg = "Here are the members that play {0}:\n".format(bold(supported_game))
    for discord_member, ign in gamers.items():
      msg += "{0}\t\t{1}\n".format(discord_member, italics(ign))
    await self.bot.say(msg)

  @ign.command(name="games", pass_context=True)
  async def ign_games(self, ctx):
    """ list all games """
    await self.bot.say(self.format_supported_games())

  @ign.command(name="set", pass_context=True)
  async def ign_set(self, ctx, game: str, *, ign):
    """ set your own IGNs """
    supported_game = self.get_supported_game(game)
    if not supported_game:
      return await self.bot.say(self.format_supported_games())

    mention = ctx.message.author.mention
    self.names.setdefault(mention, {})
    self.names[mention].update({supported_game: ign})
    self.save_settings()

    await self.bot.say("Set your {0} IGN to {1}".format(supported_game, ign))

  def get_supported_game(self, game):
    matching_games = [g for g in self.GAMES if g.lower() == game.lower()]
    if matching_games:
      return matching_games[0]

  def format_supported_games(self):
    err = "The IGN module supports {0} at this time. Ask Will to request a new game.".format(", ".join(self.GAMES))
    return box(err)

  def format_igns(self, user, ign_map):
    msg = "{0}:\n".format(user.mention)
    for game, name in ign_map.items():
      msg += "{0}\t\t {1}\n".format(bold(game), name)
    return msg

  def save_settings(self):
      fileIO('data/ign/names.json', 'save', self.names)

def check_folders():
    if not os.path.exists("data/ign"):
        print("Creating data/ign folder...")
        os.makedirs("data/ign")

def check_files():
    f = "data/ign/names.json"
    if not fileIO(f, "check"):
        print("Creating IGN names.json...")
        fileIO(f, "save", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(IGN(bot))
