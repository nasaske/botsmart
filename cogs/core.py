# cogs/core.py
import requests, discord, textwrap
from discord.ext import commands

API_URL = "https://script.google.com/macros/s/AKfycbyv2rRcR1OWJKdiAvU6BDZsdAjUdh8cqUFbKam0bgPV3ic4FfAPTfseRo-J9_TiTRMhRg/exec"  # seu URL do Apps Script /exec
SECRET  = "123"  # mesmo SECRET do Apps Script

class Core(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(name="regioes")
    async def regioes(self, ctx, *filtro):
        """
        Uso:
          !regioes            -> lista todas as regiões (um embed por região)
          !regioes norte      -> filtra só NORTE (case-insensitive)
        """
        await ctx.trigger_typing()
        try:
            r = requests.get(API_URL, params={"key": SECRET}, timeout=12)
            r.raise_for_status()
            data = r.json()
            regions = data.get("regions", [])

            if filtro:
                term = " ".join(filtro).strip().lower()
                regions = [rg for rg in regions if term in rg["regiao"].lower()]
                if not regions:
                    return await ctx.send(f"❌ Não encontrei região contendo: {term}")

            # Limite de 6000 chars por embed; vamos quebrar linhas se necessário
            for rg in regions:
                lines = []
                for it in rg.get("itens", []):
                    estado = it.get("estado", "—")
                    ag = it.get("agencia", "—")
                    lines.append(f"• **{estado}** → `{ag}`")

                # Se muito grande, fatiar em blocos
                chunks = []
                buf = ""
                for ln in lines:
                    if len(buf) + len(ln) + 1 > 3800:  # margem
                        chunks.append(buf)
                        buf = ""
                    buf += (ln + "\n")
                if buf: chunks.append(buf)

                if not chunks:
                    chunks = ["(sem linhas)"]

                for i, chunk in enumerate(chunks, start=1):
                    title = rg["regiao"] if len(chunks) == 1 else f"{rg['regiao']} ({i}/{len(chunks)})"
                    emb = discord.Embed(title=title, color=0x2ecc71, description=chunk)
                    await ctx.send(embed=emb)

        except Exception as e:
            await ctx.send(f"❌ Erro ao buscar mapa de regiões: `{type(e).__name__}: {e}`")

async def setup(bot):
    await bot.add_cog(Core(bot))
