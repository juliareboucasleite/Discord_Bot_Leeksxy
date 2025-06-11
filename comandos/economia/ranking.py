import discord
import sqlite3
from discord.ext import commands

conn = sqlite3.connect("dados.db")
c = conn.cursor()

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ranking', aliases=['leaderboard', 'topxp', 'top', 'top10', 'top10xp'], help='Mostra o ranking de XP dos membros.')
    @commands.bot_has_permissions(send_messages=True)
    async def ranking_command(self, ctx):
        c.execute("SELECT user_id, xp FROM usuarios ORDER BY xp DESC LIMIT 10")
        top = c.fetchall()

        embed = discord.Embed(
            title="🏆 Ranking de XP",
            color=0xE8E8E8
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text="Continue interagindo para subir no ranking!")
        embed.timestamp = discord.utils.utcnow()

        if not top:
            embed.description = "Nenhum usuário no ranking ainda! Comece a interagir para aparecer aqui."
        else:
            description_text = ""
            for i, (user_id, xp) in enumerate(top, start=1):
                user = await self.bot.fetch_user(user_id)
                if i == 1:
                    medal = "🥇"
                elif i == 2:
                    medal = "🥈"
                elif i == 3:
                    medal = "🥉"
                else:
                    medal = ""

                description_text += f"{medal} **{i}.** {user.mention} - **{xp} XP**\n"
            embed.description = description_text

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ranking(bot))
