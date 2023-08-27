import discord
from discord import app_commands
from ItemManagment import InitView, get_price_info


class MyClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync()

client = MyClient()


@client.tree.command(description="Манипуляции на рынке предметов")
async def manageitem(interaction: discord.Interaction):
    view = InitView()
    await interaction.response.send_message(view = view, ephemeral = True)

@client.tree.command(description = "Показать цену на предмет по имени/тегу")
async def showprice(interaction: discord.Interaction, id_to_show: str):
    row = await get_price_info(int(id_to_show))

    if row:
        id_val, product, tag, description, price = row

        embed = discord.Embed(title=f"Инормация о предмете: {product}",
                              description=f"Название: {product}\nОписание: {description}\nЦена: {price} ОТН",
                              color=discord.Color.green())

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_messaged("No information found for the specified ID.")



client.run('token')
