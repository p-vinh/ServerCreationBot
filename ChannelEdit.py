import discord
import asyncio
from ChannelCreationModal import ChannelNameModal


class ChannelEditModal(discord.ui.Select):
    def __init__(self, client, interaction):
        super().__init__()
        self.client = client
        self.interaction = interaction

        # Find all existing channels in the guild
        # Sort the channels by text and voice
        text_channels = []
        voice_channels = []
        for guild in self.client.guilds:
            if (
                guild.id == interaction.guild_id
            ):  # compare the guild id to where the message was sent
                for channel in guild.text_channels:
                    text_channels.append(
                        discord.SelectOption(label=channel.name, value=channel.id)
                    )
                for channel in guild.voice_channels:
                    voice_channels.append(
                        discord.SelectOption(label=channel.name, value=channel.id)
                    )

        self.options = text_channels + voice_channels
        self.placeholder = "Select Channel to Edit"
        self.max_values = 1

    async def send_select_menu(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(self)

        async def select_callback(interaction: discord.Interaction):
            channel_id = self.values[0]
            await interaction.response.send_modal(
                ChannelNameModal(self.client, channel_id, "edit")
            )
            

        self.callback = select_callback
        await interaction.response.send_message(
            "Select a channel to edit:", view=view, ephemeral=True
        )
