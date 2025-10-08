import os, discord
from discord.ext import commands
import sqlite3

# Conecte (ou crie) o banco de dados
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/bot.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS prefixes (
    guild_id INTEGER PRIMARY KEY,
    prefix TEXT DEFAULT '!'
)
""")
conn.commit()

def get_prefix(bot, message):
    if message.guild is None:
        return "!"  # prefixo padrão no DM
    cur.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    row = cur.fetchone()
    return row[0] if row else "!"  # retorna prefixo salvo ou "!"

intents = discord.Intents.default()
intents.message_content = True  # necessário para comandos baseados em mensagem

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logado como {bot.user} ({bot.user.id})")

async def main():
    async with bot:
        await bot.load_extension("cogs.core")
        await bot.load_extension("cogs.moderation")
        await bot.start(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
