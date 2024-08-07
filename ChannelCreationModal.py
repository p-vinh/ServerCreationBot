import discord
from discord.ext import commands


class ChannelCreationModal(discord.ui.Modal):
    def __init__(self, client):
        super().__init__(title="Create a Channel")
        self.client = client

        self.channel_name = discord.ui.TextInput(
            label="Channel Name",
            placeholder="Enter the new channel name",
            style=discord.TextStyle.short,
            required=True,
        )
        self.add_item(self.channel_name)

        self.channel_type = discord.ui.Select(
            placeholder="Select Channel Type",
            options=[
                discord.SelectOption(label="Text Channel", value="text"),
                discord.SelectOption(label="Voice Channel", value="voice"),
            ],
        )
        self.add_item(self.channel_type)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.channel_name.value.strip()
        channel_type = self.channel_type.values[0]

        if channel_type == "text":
            await interaction.guild.create_text_channel(name)
        elif channel_type == "voice":
            await interaction.guild.create_voice_channel(name)

    async def create_text_channel(self, interaction: discord.Interaction, name: str):
        await interaction.guild.create_text_channel(name)
        await interaction.response.send_message(
            f"Text channel '{name}' created.", ephemeral=True
        )

    async def create_voice_channel(self, interaction: discord.Interaction, name: str):
        await interaction.guild.create_voice_channel(name)
        await interaction.response.send_message(
            f"Voice channel '{name}' created.", ephemeral=True
        )
