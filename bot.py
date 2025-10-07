import os, discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # marque essa intent no portal do Discord
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(os.environ["DISCORD_TOKEN"])
