import discord
from discord.ext import commands
from typing import Optional

class Recrutador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="convite")
    async def recrutador(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author

        try:
            invites = await ctx.guild.invites()
        except discord.Forbidden:
            return await ctx.send("❌ Não tenho permissão para ver os convites deste servidor.")

        # Filtrar convites criados pelo membro
        pessoais = [i for i in invites if i.inviter and i.inviter.id == member.id]
        total_uses = sum(i.uses for i in pessoais)
        links_info = "\n".join(
            [f"https://discord.gg/{i.code} - **{i.uses} novato(s)**" for i in pessoais]
        )

        if not links_info:
            links_info = f"**{member.display_name}** não possui convites ativos no servidor."

        embed = discord.Embed(
            title="📨 Recrutador",
            description=f"Convites criados por {member.mention}",
            color=discord.Color.random()
        )
        embed.add_field(name="Total de convites", value=f"**{total_uses}**", inline=True)
        embed.add_field(name="Convites", value=links_info, inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Requisitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Recrutador(bot))
