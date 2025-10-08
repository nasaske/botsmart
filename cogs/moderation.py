# cogs/moderation.py
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str | None = None):
        """Bane um usuário. Uso: !ban @alguem [motivo]"""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member} banido. Motivo: {reason or '—'}")
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para banir esse usuário.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Falha ao banir: {e}")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str | None = None):
        """Expulsa um usuário. Uso: !kick @alguem [motivo]"""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member} expulso. Motivo: {reason or '—'}")
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para expulsar esse usuário.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Falha ao expulsar: {e}")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int):
        """Apaga N mensagens. Uso: !clear 10"""
        if amount < 1:
            return await ctx.send("Informe um número ≥ 1.")
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 inclui o comando
        confirm = await ctx.send(f"🧹 Apaguei {len(deleted)-1} mensagens.")
        await confirm.delete(delay=3)

# ENTRYPOINT (obrigatório para load_extension)
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
