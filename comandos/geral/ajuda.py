import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ajuda",
        description="Mostra todos os comandos do bot organizados por categorias.",
        aliases=["help"]
    )
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="📚 Lista de Comandos",
            description="Use `'ajuda <comando>` para saber mais sobre um comando específico.\n\n",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        embed.set_author(name=self.bot.user.display_name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.timestamp = discord.utils.utcnow()

        # Dicionário para armazenar comandos por categoria
        categorias = {
            "Geral": [],
            "Moderação": [],
            "Diversão": [],
            "Economia": [],
            "Música": [],
            "Administração": []
        }

        # Iterar sobre todos os comandos do bot
        for command in self.bot.commands:
            if command.hidden: # Ignorar comandos ocultos
                continue

            # Tenta determinar a categoria com base no caminho do arquivo do cog
            # Isso é uma heurística e pode precisar de ajuste dependendo da estrutura exata
            category_name = "Outros" # Categoria padrão
            if command.cog_name:
                if command.cog_name == "ServerSettings" or command.cog_name == "ReactionRoles":
                    category_name = "Administração"
                elif command.cog_name == "Kick" or command.cog_name == "Warn" or command.cog_name == "Unwarn" or command.cog_name == "Warnings" or command.cog_name == "Mute" or command.cog_name == "Unmute":
                    category_name = "Moderação"
                elif command.cog_name == "Dado" or command.cog_name == "Moeda" or command.cog_name == "EightBall" or command.cog_name == "Fato" or command.cog_name == "Abraço" or command.cog_name == "Tapa" or command.cog_name == "Kiss" or command.cog_name == "Lamber" or command.cog_name == "Carinho" or command.cog_name == "Say" or command.cog_name == "Avatar":
                    category_name = "Diversão"
                elif command.cog_name == "Daily" or command.cog_name == "Work" or command.cog_name == "Balance" or command.cog_name == "Shop" or command.cog_name == "Perfil" or command.cog_name == "Emblema" or command.cog_name == "XP" or command.cog_name == "Ranking" or command.cog_name == "Moedas":
                    category_name = "Economia"
                elif command.cog_name == "Music": # Assumindo um cog Music principal
                    category_name = "Música"
                elif command.cog_name == "Ping" or command.cog_name == "Ajuda":
                    category_name = "Geral"

            command_aliases = [f"`'{alias}`" for alias in command.aliases]
            command_entry = f"`'{command.name}`"
            if command_aliases:
                command_entry += f" (ou {', '.join(command_aliases)})"
            command_entry += f" - {command.help or 'Sem descrição.'}"
            
            # Adicionar o comando à categoria correta
            if category_name not in categorias:
                categorias[category_name] = [] # Cria a categoria se não existir
            categorias[category_name].append(command_entry)
        
        # Adicionar slash commands manualmente ou buscar (para comandos de barra, o bot.commands não lista diretamente)
        # Para '/oi'
        categorias["Geral"].append("`/oi` - O bot diz oi! (Comando de barra)")


        # Adicionar campos para cada categoria que tem comandos
        for category, commands_list in categorias.items():
            if commands_list:
                # Ordenar comandos alfabeticamente dentro de cada categoria
                commands_list.sort()
                # Limitar o tamanho da descrição do campo para evitar erros do Discord
                field_value = "\n".join(commands_list)
                if len(field_value) > 1024: # Limite de 1024 caracteres por campo
                    field_value = field_value[:1020] + "..." # Truncar se for muito longo
                
                embed.add_field(
                    name=f"✨ {category} ({len(commands_list)})", # Ícone genérico, pode personalizar
                    value=field_value,
                    inline=False
                )

        # Links Adicionais
        embed.add_field(
            name="🔗 Links Adicionais",
            value="[Meu convite](https://discord.com/oauth2/authorize?client_id=1370143300228747284&permissions=8&integration_type=0&scope=bot) | [Meu servidor](https://discord.gg/pJAuxtr2QQ)", # Substitua pelos links reais
            inline=False
        )

        embed.set_footer(text="Leeksxy • Ajuda organizada por categorias")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
