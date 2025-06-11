import discord
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shop', aliases=['loja', 'store', 'items', 'itens', 'comprar'], help='Exibe os itens disponíveis na loja.')
    @commands.bot_has_permissions(send_messages=True)
    async def shop_command(self, ctx):
        items = {
            "poção_de_vida": {
                "nome": "Poção de Vida",
                "descricao": "Restaura um pouco da sua energia. (Ainda não funcional)",
                "preco": 150
            },
            "espada_afiada": {
                "nome": "Espada Afiada",
                "descricao": "Uma espada básica para aventuras. (Ainda não funcional)",
                "preco": 500
            },
            "escudo_resistente": {
                "nome": "Escudo Resistente",
                "descricao": "Proteção extra em combate. (Ainda não funcional)",
                "preco": 300
            },
            "amuleto_da_sorte": {
                "nome": "Amuleto da Sorte",
                "descricao": "Aumenta suas chances em jogos. (Ainda não funcional)",
                "preco": 1000
            }
        }

        description = "**Itens disponíveis na loja:**\n\n"
        for item_id, item_info in items.items():
            description += f"**{item_info['nome']}** (`ID: {item_id}`)\n"
            description += f"**Preço:** {item_info['preco']} moedas\n"
            description += f"**Descrição:** {item_info['descricao']}\n"
            description += "---\n"
        
        embed = discord.Embed(
            title="🏪 Loja do Servidor",
            description=description,
            color=0xE8E8E8
        )
        embed.set_footer(text="Para comprar um item, um comando de compra será implementado futuramente.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot)) 