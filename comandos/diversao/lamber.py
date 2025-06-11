import discord
from discord.ext import commands
import random

class LamberView(discord.ui.View):
    def __init__(self, autor, alvo):
        super().__init__(timeout=60)
        self.autor = autor
        self.alvo = alvo

    @discord.ui.button(label="👅 Lamber de volta", style=discord.ButtonStyle.secondary)
    async def lamber_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.alvo.id:
            embed = discord.Embed(
                title="❌ Não é sua vez!",
                description=f"Apenas {self.alvo.mention} pode retribuir o beijo!",
                color=0xE8E8E8
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        gifs = [
            'https://media.tenor.com/1oHjFb8iKGIAAAAC/lick-anime.gif',
            'https://media.tenor.com/1ChcN3szUGkAAAAC/lick-licking.gif',
            'https://media.tenor.com/zkVq_fXwM4wAAAAC/lick-anime-kiss.gif',
            'https://media.tenor.com/F0r0p_Y0_LAAAAAC/lick-anime-cute.gif',
            'https://media.tenor.com/gK9e4H_2m9QAAAAC/lick-cute.gif'
        ]

        embed = discord.Embed(
            title="👅 Lamber de Volta!",
            description=f"{self.alvo.mention} lambeu {self.autor.mention} de volta!",
            color=0xE8E8E8
        )
        embed.set_image(url=random.choice(gifs))
        embed.set_author(name=self.alvo.display_name, icon_url=self.alvo.avatar.url if self.alvo.avatar else None)
        embed.set_footer(text="Que divertido!")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed)
        self.stop()

class Lamber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lamber", aliases=["lick", "lambida"], help='Lambe um membro. Uso: \'lamber <@membro>')
    async def lamber(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem lamber?",
                description="Por favor, mencione um membro para lamber!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🤨 Lamber a Si Mesmo?",
                description="Você está tentando lamber a si mesmo? Que inusitado!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Ops!",
                description="Não me lamba! Sou um bot, não tenho sabor!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        gifs = [
            'https://media.tenor.com/ThT8ZvjghcYAAAAC/lick.gif',
            'https://media.tenor.com/rUUNQe_1K3wAAAAC/anime-lick.gif',
            'https://media.tenor.com/t0x1QpOmQ7gAAAAd/lick-anime.gif',
            'https://media.tenor.com/eB32sY_tq6QAAAAC/lick-anime.gif',
            'https://media.tenor.com/mJ-J6l_3gR4AAAAC/anime-lick.gif'
        ]

        embed = discord.Embed(
            title="👅 Lamber no Ar!",
            description=f"{ctx.author.mention} lambeu {membro.mention}! Que momento... peculiar!",
            color=0xE8E8E8
        )
        embed.set_image(url=random.choice(gifs))
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Sinta o sabor da amizade (ou não)!", icon_url="https://emoji.discord-static.com/emojis/795123456789012345.gif?v=1")
        embed.timestamp = discord.utils.utcnow()
        
        view = LamberView(ctx.author, membro)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Lamber(bot))