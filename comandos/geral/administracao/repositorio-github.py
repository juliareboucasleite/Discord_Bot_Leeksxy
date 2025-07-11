import discord
from discord.ext import commands

class RepoButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="GitHub",
            url="https://github.com/juliareboucasleite",
            style=discord.ButtonStyle.link
        ))
        self.add_item(discord.ui.Button(
            label="Replit",
            url="https://replit.com/@M4arii/Mady",
            style=discord.ButtonStyle.link
        ))

class Repo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="repo")
    async def repo(self, ctx):
        embed = discord.Embed(
            title="Fala dev!",
            description="Nosso bot está em constante desenvolvimento.\n"
                        "Se você quiser ajudar de alguma forma, é só apertar em um dos botões abaixo!",
            color=discord.Color.blue()
        )
        embed.set_author(
            name="ProgramaBOT",
            icon_url="https://i.pinimg.com/564x/38/15/b5/3815b57c9d884cb29e13beb03e91cb0d.jpg",
            url="https://discord.gg/bbmVB5TdWk"
        )

        await ctx.send(embed=embed, view=RepoButtonView())

def setup(bot):
    bot.add_cog(Repo(bot))
