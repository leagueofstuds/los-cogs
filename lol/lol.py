import discord
from discord.ext import commands

import urllib.request, json
import requests
import string

class Lol:
  """League of Legends"""

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def lol(self, region: str, summoner: str):
    '''Sample: !lol na "summoner name"'''
    error_msg = None

    # Start by making sure that they gave us a summoner name
    available_regions = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]
    if region in available_regions:
      error_msg = "You must start with the region name (e.g. NA, EUW, OCE)"

    summoner_uid = summoner.replace(" ", "").lower()
    api_key ="86a95428-3bb8-486d-89e6-8e3c4b2f8f4e"
    fetch_summoner_url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{summoner}?api_key={api_key}".format(
      region = region, summoner = summoner_uid, api_key = api_key)
    summoner_request = requests.get(fetch_summoner_url)

    if summoner_request.status_code == 404:
      error_msg = "A summoner named {summoner_name} does not exist!".format(summoner_name = summoner)
    elif not summoner_request.ok:
      error_msg = "Oops! Something went wrong! Sorry... might want to ask Daddy about it."

    if error_msg is not None: return await self.bot.say(error_msg)

    # TODO: this is a static helper
    region_code = region.upper()
    if (region_code != "KR") or (region_code!="RU"):
      region_code = region_code + "1"
    else:
      region_code = region_code

    if region_code == "OCE1":
      region_code = "OC1"

    if region_code == "EUNE1":
      region_code = "EUN1"

    summoner_data = summoner_request.json()[summoner_uid]
    match_info_url = "https://{region}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{region_code}/{summoner_id}?api_key={api_key}".format(
      region = region, region_code = region_code, summoner_id = summoner_data["id"], api_key = api_key)
    match_info_request = requests.get(match_info_url)

    if match_info_request.status_code == 404:
      error_msg = "{summoner_name} is not currently in a match.".format(summoner_name = summoner_data['name'])
    elif not match_info_request.ok:
      error_msg = "Oops! Something went wrong! Sorry... might want to ask Daddy about it."

    if error_msg is not None: return await self.bot.say(error_msg)

    team_colors = ["**Blue**", "**Red**"]
    team = team_colors[0]
    message = "Hello"
    match_info_data = match_info_request.json()

    def search_champion(champion_id: str):
      champ_info_url = "https://global.api.pvp.net/api/lol/static-data/{region}/v1.2/champion/{champion_id}?api_key={api_key}".format(
      region = region, champion_id = champion_id, api_key = api_key)
      champ_info_request = requests.get(champ_info_url)
      champ_info_data = champ_info_request.json()
      return champ_info_data['name']

    for participant in match_info_data["participants"]:
      if participant["summonerId"] == summoner_data["id"]:
        team_number = str(participant["teamId"])
        team_number = team_number[:1]
        team = team_colors[int(team_number)-1]
        message = "**"+summoner+"** is in "+team+" Team"

    message += "\n\n__Blue Team__"

    for x in range(len(match_info_data["participants"])):
      if match_info_data["participants"][x]["teamId"] == 100:
        message += "\n**"+match_info_data["participants"][x]["summonerName"]+"** | "+search_champion(str(match_info_data["participants"][x]["championId"]))

    message +="\n\n__Red Team__"\

    for y in range(len(match_info_data["participants"])):
      if match_info_data["participants"][y]["teamId"] == 200:
        message += "\n**"+match_info_data["participants"][y]["summonerName"]+"** | "+search_champion(str(match_info_data["participants"][y]["championId"]))

    await self.bot.say(message)

def setup(bot):
    bot.add_cog(Lol(bot))

