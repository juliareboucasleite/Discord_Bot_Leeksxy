import discord
from discord.ext import commands
import sqlite3

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='addreactionrole', aliases=['arr', 'adicionarcargoreacao', 'addrr'], help='Adiciona um cargo por reação a uma mensagem. Uso: !addreactionrole <ID_da_mensagem> <emoji> <@cargo>')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True, add_reactions=True, read_message_history=True)
    async def add_reaction_role(self, ctx, message_id: int, emoji, *, role: discord.Role):
        guild_id = ctx.guild.id
        
        # Normalize o emoji. Para emojis personalizados, pegamos apenas o nome e ID.
        # Para emojis unicode, ele já é a string correta.
        if emoji.startswith('<:') and emoji.endswith('>'):
            # Emoji personalizado: <a:nome:ID> ou <:nome:ID>
            parts = emoji.split(':')
            if len(parts) == 3: # <:nome:ID>
                emoji_name = parts[1]
                emoji_id = parts[2][:-1] # Remove o '>'
                normalized_emoji = f'{emoji_name}:{emoji_id}'
            elif len(parts) == 4: # <a:nome:ID>
                emoji_name = parts[1]
                emoji_id = parts[2]
                normalized_emoji = f'{emoji_name}:{emoji_id}'
            else:
                embed = discord.Embed(
                    title="❌ Erro de Emoji",
                    description="Formato de emoji personalizado inválido. Use um emoji padrão ou um emoji personalizado no formato `:<nome_emoji>:` ou `<:nome_emoji:ID>`.",
                    color=0xDCDCDC
                )
                await ctx.send(embed=embed)
                return
        elif emoji.startswith('<a:') and emoji.endswith('>'):
            parts = emoji.split(':')
            if len(parts) == 4:
                emoji_name = parts[1]
                emoji_id = parts[2]
                normalized_emoji = f'a:{emoji_name}:{emoji_id}'
            else:
                embed = discord.Embed(
                    title="❌ Erro de Emoji",
                    description="Formato de emoji animado personalizado inválido. Use um emoji padrão ou um emoji personalizado no formato `<a:nome_emoji:ID>`.",
                    color=0xDCDCDC
                )
                await ctx.send(embed=embed)
                return
        else:
            # Emoji unicode
            normalized_emoji = emoji

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO reaction_roles (guild_id, message_id, emoji, role_id) VALUES (?, ?, ?, ?)",
                           (guild_id, message_id, normalized_emoji, role.id))
            conn.commit()
            
            # Tentar adicionar a reação à mensagem imediatamente
            try:
                message = await ctx.fetch_message(message_id)
                await message.add_reaction(emoji)
            except discord.NotFound:
                embed = discord.Embed(
                    title="⚠️ Mensagem Não Encontrada",
                    description=f"O comando foi salvo, mas não consegui encontrar a mensagem com ID `{message_id}` para adicionar a reação. Certifique-se de que o ID da mensagem está correto e que o bot tem permissão para ver o canal e adicionar reações.",
                    color=0xFFCC00 # Amarelo/Laranja para aviso
                )
                await ctx.send(embed=embed)
                return
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Permissões Insuficientes",
                    description=f"O comando foi salvo, mas não tenho permissão para adicionar a reação '{emoji}' na mensagem com ID `{message_id}`. Por favor, verifique minhas permissões no canal.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Erro ao Adicionar Reação",
                    description=f"O comando foi salvo, mas ocorreu um erro ao tentar adicionar a reação à mensagem: {e}",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title="✅ Cargo por Reação Adicionado!",
                description=f"Se a reação {emoji} for adicionada à mensagem com ID `{message_id}`, o cargo {role.mention} será concedido.",
                color=0x2ECC71 # Verde
            )
            await ctx.send(embed=embed)
        except sqlite3.IntegrityError:
            embed = discord.Embed(
                title="❌ Configuração Existente",
                description=f"Já existe um cargo configurado para o emoji {emoji} na mensagem com ID `{message_id}`.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro ao Adicionar Cargo por Reação",
                description=f"Ocorreu um erro: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

    @commands.command(name='removereactionrole', aliases=['rrr', 'removercargoreacao', 'remrr'], help='Remove um cargo por reação de uma mensagem. Uso: !removereactionrole <ID_da_mensagem> <emoji>')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_reaction_role(self, ctx, message_id: int, emoji):
        guild_id = ctx.guild.id

        # Normalize o emoji da mesma forma que em add_reaction_role
        if emoji.startswith('<:') and emoji.endswith('>'):
            parts = emoji.split(':')
            if len(parts) == 3:
                emoji_name = parts[1]
                emoji_id = parts[2][:-1]
                normalized_emoji = f'{emoji_name}:{emoji_id}'
            elif len(parts) == 4:
                emoji_name = parts[1]
                emoji_id = parts[2]
                normalized_emoji = f'{emoji_name}:{emoji_id}'
            else:
                embed = discord.Embed(
                    title="❌ Erro de Emoji",
                    description="Formato de emoji personalizado inválido. Use um emoji padrão ou um emoji personalizado no formato `:<nome_emoji>:` ou `<:nome_emoji:ID>`.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
        elif emoji.startswith('<a:') and emoji.endswith('>'):
            parts = emoji.split(':')
            if len(parts) == 4:
                emoji_name = parts[1]
                emoji_id = parts[2]
                normalized_emoji = f'a:{emoji_name}:{emoji_id}'
            else:
                embed = discord.Embed(
                    title="❌ Erro de Emoji",
                    description="Formato de emoji animado personalizado inválido. Use um emoji padrão ou um emoji personalizado no formato `<a:nome_emoji:ID>`.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
        else:
            normalized_emoji = emoji

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
                       (guild_id, message_id, normalized_emoji))
        conn.commit()
        if cursor.rowcount > 0:
            embed = discord.Embed(
                title="✅ Cargo por Reação Removido!",
                description=f"A configuração para o emoji {emoji} na mensagem com ID `{message_id}` foi removida.",
                color=0x2ECC71
            )
            # Tentar remover a reação da mensagem, se existir
            try:
                message = await ctx.fetch_message(message_id)
                await message.remove_reaction(emoji, self.bot.user)
            except discord.NotFound:
                pass # Mensagem já pode ter sido deletada
            except discord.Forbidden:
                print(f"❌ Permissões insuficientes para remover a reação {emoji} da mensagem {message_id}")
            except Exception as e:
                print(f"❌ Erro ao remover reação da mensagem: {e}")
        else:
            embed = discord.Embed(
                title="ℹ️ Configuração Não Encontrada",
                description=f"Nenhuma configuração de cargo por reação encontrada para o emoji {emoji} na mensagem com ID `{message_id}`.",
                color=0xFFCC00
            )
        await ctx.send(embed=embed)
        conn.close()

    @commands.command(name='listreactionroles', aliases=['lrr', 'listarcargosreacao', 'viewrr'], help='Lista todos os cargos por reação configurados para este servidor.')
    @commands.has_permissions(manage_roles=True)
    async def list_reaction_roles(self, ctx):
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT message_id, emoji, role_id FROM reaction_roles WHERE guild_id = ?", (guild_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            embed = discord.Embed(
                title="ℹ️ Nenhum Cargo por Reação Configurado",
                description="Nenhum cargo por reação foi configurado para este servidor.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed)
            return

        description = ""
        for message_id, emoji, role_id in rows:
            role = ctx.guild.get_role(role_id)
            if role:
                description += f"- **Mensagem ID:** `{message_id}` | **Emoji:** {emoji} | **Cargo:** {role.mention}\n"
            else:
                description += f"- **Mensagem ID:** `{message_id}` | **Emoji:** {emoji} | **Cargo ID:** `{role_id}` (Cargo não encontrado)\n"
        
        embed = discord.Embed(
            title="📋 Cargos por Reação Configurados",
            description=description,
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot)) 