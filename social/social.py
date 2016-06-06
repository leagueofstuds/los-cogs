import os
import asyncio
from random import randint, sample

import discord
from discord.ext import commands

class Social:
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def kiss(self, context, user: discord.Member):
    """ kiss anyone """
    msg = '{0} Was KISSED by {1}! :kiss:'.format(user.mention, context.message.author.mention)
    folder = "kiss"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def taunt(self, context, user: discord.Member):
    """ taunt anyone """
    msg = '{0} Was TAUNTED by {1}! :kiss:'.format(user.mention, context.message.author.mention)
    folder = "taunt"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def gank(self, context, user: discord.Member):
    """ gank anyone """
    msg = '{0} Was Ganked by {1}! :kiss:'.format(user.mention, context.message.author.mention)
    folder = "gank"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def sit(self, context, user: discord.Member):
    """ sit on anyone face"""
    msg = '{1}! Sits on {0} face :smiling_imp: '.format(user.mention, context.message.author.mention)
    folder = "sit"
    await self.upload_random_gif(msg, folder)


  @commands.command(pass_context=True)
  async def tip(self, context, user: discord.Member):
    """ make it rain on anyone """
    msg = '{1}! Makes it rain on {0} :money_mouth: :money_with_wings:  '.format(user.mention, context.message.author.mention)
    folder = "tips"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def shoot(self, context, user: discord.Member):
    """ shoot anyone """
    msg = '{0} Was shot dead by {1}! :skull: :gun: '.format(user.mention, context.message.author.mention)
    folder = "shoot"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def snatch(self, context, user: discord.Member):
    """ snatch anyone wig"""
    msg = '{0} Wig has been snatched by {1}! r.i.p :scream: '.format(user.mention, context.message.author.mention)
    folder = "snatched"
    await self.upload_random_gif(msg, folder)
    
  @commands.command(pass_context=True)
  async def cuddle(self, context, user: discord.Member):
    """ cuddle with anyone """
    msg = '{1}! Cuddles {0} so hard! '.format(user.mention, context.message.author.mention)
    folder = "cuddle"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def spell(self, context, user: discord.Member):
    """ casts a spell on anyone """
    msg = '{1}! Casts a spell on {0} ! :dizzy: :comet: '.format(user.mention, context.message.author.mention)
    folder = "spell"
    await self.upload_random_gif(msg, folder)  

  @commands.command(pass_context=True)
  async def hugs(self, context, user: discord.Member):
    """ hugs anyone """
    msg = '{1}! Gives {0} a big hug! :hugging:  '.format(user.mention, context.message.author.mention)
    folder = "hug"
    await self.upload_random_gif(msg, folder)  
  

  @commands.command(pass_context=True)
  async def truth(self, context, user: discord.Member):
    """ truth questions """
    msg = '{1}! Challenges {0} to tell the truth!  '.format(user.mention, context.message.author.mention)
    folder = "truth"
    await self.upload_random_gif(msg, folder)  

  @commands.command(pass_context=True)
  async def dare(self, context, user: discord.Member):
    """ dare questions """
    msg = '{1}! Challenges {0} to a dare!  '.format(user.mention, context.message.author.mention)
    folder = "dare"
    await self.upload_random_gif(msg, folder)  
 
  @commands.command(pass_context=True)
  async def feed(self, context, user: discord.Member):
    """ feed anyone """
    msg = '{1}! Feeds {0}! :yum:  '.format(user.mention, context.message.author.mention)
    folder = "feeds"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def drag(self, context, user: discord.Member):
    """ drag race persona of a friend """
    msg = '{1}! Reveals {0}! true inner drag persona! :princess: '.format(user.mention, context.message.author.mention)
    folder = "drag"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def future(self, context, user: discord.Member):
    """ check some ones future """
    msg = '{1}! Takes a glance at what {0}! will become in the future! :scream:  '.format(user.mention, context.message.author.mention)
    folder = "future"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def shade(self, context, user: discord.Member):
    """ throw some serious shade """
    msg = 'It\'s cold in the shade. Isn\'t it {mentioned_user}?'.format(
      mentioned_user = user.mention)
    folder = "shade"
    await self.upload_random_gif(msg, folder)

  @commands.command(pass_context=True)
  async def adore(self, context, *gif):
    """ summon adore (e.g. die, drag, ew, fuck, gasp, idgaf, overit, party, tongue) """
    adores = ("die", "drag", "ew", "fuck", "gasp", "idgaf", "overit", "party", "tongue")
    if gif:
      gif = gif.lower()
      if gif in adores:
        return await self.bot.upload("data/gifs/adore/{0}.gif".format(gif))
    await self.upload_random_gif(None, "adore")

  @commands.command()
  async def rr(self):
    """ russian roulette... good luck! """
    await self.bot.say('You spin the cylinder of the revolver with 1 bullet in it...')
    await asyncio.sleep(1)
    await self.bot.say('...you place the muzzle against your head and pull the trigger...')
    await asyncio.sleep(2)
    if randint(1, 6) == 1:
      await self.bot.say('...your brain gets splattered all over the wall.')
    else:
      await self.bot.say('...you live to see another day.')

  async def upload_random_gif(self, msg, folder):
    if msg:
      await self.bot.say(msg)
    folderPath = "data/gifs/" + folder
    fileList = os.listdir(folderPath)
    gifPath = folderPath + "/" + fileList[randint(0, len(fileList) - 1)]
    await self.bot.upload(gifPath)

def setup(bot):
    bot.add_cog(Social(bot))

