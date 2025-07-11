import discord
from discord.ext import commands

class VoteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Disboard', url='https://discord.gg/bbmVB5TdWk'))
        self.add_item(discord.ui.Button(label='Discod', url='https://i.pinimg.com/564x/ce/ec/a1/ceeca1f21607a3b85431e8aed33f6d04.jpg'))

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vote', help='Envia links para votar no servidor.')
    async def vote(self, ctx):
        embed = discord.Embed(
            title='Fala dev!',
            color=0x0099ff,
            description='Você pode ajudar o servidor a crescer votando nos sites abaixo\n\nObs: é possível compartilhar várias vezes por dia <3'
        )
        embed.set_author(name='ProgramaBOT', icon_url='https://i.pinimg.com/564x/38/15/b5/3815b57c9d884cb29e13beb03e91cb0d.jpg', url='https://discord.gg/bbmVB5TdWk')
        await ctx.send(embed=embed, view=VoteView())

async def setup(bot):
    await bot.add_cog(Vote(bot))