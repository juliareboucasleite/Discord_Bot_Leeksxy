from discord.ext import commands
import discord
import platform
import datetime
import os

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")
DISCORD_BOT_INVITE_URL = os.getenv("DISCORD_BOT_INVITE_URL", "https://discord.com/oauth2/authorize")
LINK_SERVIDOR = os.getenv("LINK_SERVIDOR", "https://discord.gg/seulink")
DATA_CRIACAO = os.getenv("DATA_CRIACAO", "6 de novembro de 2021")

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
        # Monta a lista de donos do bot (menção + ID)
        mentions = []
        for oid in OWNER_IDS:
            oid = oid.strip()
            if oid.isdigit():
                user = bot.get_user(int(oid))
                if user:
                    mentions.append(f"{user.mention} ({oid})")
                else:
                    mentions.append(f"<@{oid}> ({oid})")
        donos_str = '\n'.join(mentions) if mentions else 'Nenhum dono configurado no .env!'
        embed.add_field(name="Criadora(s):", value=donos_str, inline=False)
        embed.add_field(name=":blond_haired_man: Usuários", value=f"`{len(bot.users)}`", inline=True)
        embed.add_field(name="Servers", value=f"`{len(bot.guilds)}`", inline=True)
        embed.add_field(name="😴 Uptime", value=f"{days}d {hours}h {minutes}m {seconds}s", inline=False)
        embed.add_field(name="💬 Canais", value=f"`{len(bot.channels)}`", inline=True)
        embed.add_field(name="📁 Emojis", value=f"`{len(bot.emojis)}`", inline=True)
        embed.add_field(name="🔢 Fui criado em", value=DATA_CRIACAO, inline=False)
        embed.add_field(name="Suporte", value=f"[clique aqui]({LINK_SERVIDOR}) para entrar", inline=True)
        embed.add_field(name="Invite", value=f"[clique aqui]({DISCORD_BOT_INVITE_URL}) para me convidar", inline=True)
        embed.set_footer(text="Zik")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)