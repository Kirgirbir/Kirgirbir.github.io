import discord
from discord import app_commands
from ItemManagment import InitView


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


@client.tree.command(description="Добавить Предмет")
async def manageitem(interaction: discord.Interaction):
    view = InitView()
    await interaction.response.send_message(view = view, ephemeral = True)


client.run('MTA3NzY1NTk3MTMxNDI5MDcyMA.GaF_Lb.bDFOEwuU4lRLJ4AOYn-qFg_hCNPmtxLMGb2XtM')
