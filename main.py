import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import importlib

load_dotenv()
bot = commands.Bot(command_prefix='-', intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="👽 Sizi"))
    print("Bot bağlandı ve durumu güncellendi.")
  
  
  

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        cog_name = filename[:-3]
        cog_module = importlib.import_module("cogs." + cog_name)
        cog_class = getattr(cog_module, cog_name)
        bot.add_cog(cog_class(bot))



bot.run(os.getenv("TOKEN"))


