import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot=commands.Bot(command_prefix=os.getenv('BOT_PREFIX'), intents=intents, status=discord.Status.idle, activity=discord.Game(name="Booting"))   
bot.remove_command("help")

bot.color = int(os.getenv('EMBED_COLOR'), 16)
bot.prefix = os.getenv('BOT_PREFIX')

@bot.event
async def on_ready():
    name_=bot.user.name
    print('\x1b[0;30;44m' + f'Logged in as {name_}' + '\x1b[0m' + '\n    ----------')
    print('\x1b[6;30;42m' + 'Bot - Online' + '\x1b[0m' + '\n')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"critterz {bot.prefix}help"))

@bot.command()
async def help(ctx):
    embed=discord.Embed(title=f"Hello {ctx.author.name}, here are the commands", color=bot.color).add_field(
        name=f'`{bot.prefix}stats <wallet>`', value='> View your stats', inline=False)                   
    await ctx.send(embed=embed)

initial_extensions = ['stat_checker']
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(str(os.getenv('BOT_TOKEN')))