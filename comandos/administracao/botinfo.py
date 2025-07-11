from discord.ext import commands
import discord
import platform
import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        bot = self.bot
        uptime = datetime.datetime.utcnow() - bot.launch_time if hasattr(bot, 'launch_time') else None
        days, remainder = divmod(int(uptime.total_seconds()), 86400) if uptime else (0, 0)
        hours, remainder = divmod(remainder, 3600) if uptime else (0, 0)
        minutes, seconds = divmod(remainder, 60) if uptime else (0, 0)

        embed = discord.Embed(
            title="Minhas informações!!",
            description=f"Olá {ctx.author.mention}! Tudo bem com vc? Espero que sim! Eu procuro divertir as pessoas com meus comandos (**Se você não sabe meu prefix é '{ctx.prefix}'**)\nMinhas informações estão abaixo!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Criadora:", value="<@916737425978589235>", inline=False)
        embed.add_field(name=":blond_haired_man: Usuários", value=f"`{len(bot.users)}`", inline=True)
        embed.add_field(name="Servers", value=f"`{len(bot.guilds)}`", inline=True)
        embed.add_field(name="😴 Uptime", value=f"{days}d {hours}h {minutes}m {seconds}s", inline=False)
        embed.add_field(name="💬 Canais", value=f"`{len(bot.channels)}`", inline=True)
        embed.add_field(name="📁 Emojis", value=f"`{len(bot.emojis)}`", inline=True)
        embed.add_field(name="🔢 Fui criado em", value="6 de novembro de 2021", inline=False)
        embed.add_field(name="Suporte", value="[clique aqui](https://discord.gg/fv99BGYKHh) para entrar", inline=True)
        embed.add_field(name="Invite", value="[clique aqui](https://discord.com/api/oauth2/authorize?client_id=904397870856306708&permissions=0&scope=bot) para me convidar", inline=True)
        embed.set_footer(text="Zik")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    # Salva o horário de início do bot para calcular uptime
    if not hasattr(bot, 'launch_time'):
        bot.launch_time