import discord
from discord.ext import commands


class ChannelTypeSelectModal(discord.ui.Select):
    def __init__(self, client):
        super().__init__(
            placeholder="Select Channel Type",
            options=[
                discord.SelectOption(label="None", value="none", default=True),
                discord.SelectOption(label="Text Channel", value="text"),
                discord.SelectOption(label="Voice Channel", value="voice"),
            ],
            max_values=1,
        )

        self.client = client

    async def send_select_menu(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(self)

        async def select_callback(interaction: discord.Interaction):
            channel_type = self.values[0]
            await interaction.response.send_modal(
                ChannelNameModal(self.client, channel_type)
            )

        self.callback = select_callback
        await interaction.response.send_message(
            "Select a channel type:", view=view, ephemeral=True
        )


class ChannelNameModal(discord.ui.Modal):
    def __init__(self, client, channel_type):
        super().__init__(title="Enter Channel Name")
        self.client = client
        self.channel_type = channel_type

        self.channel_name = discord.ui.TextInput(
            label="Channel Name",
            placeholder="Enter the new channel name",
            style=discord.TextStyle.short,
            required=True,
        )
        self.add_item(self.channel_name)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.channel_name.value.strip()

        if self.channel_type == "text":
            await interaction.guild.create_text_channel(name)
            await interaction.response.send_message(
                f"Text channel '{name}' created.", ephemeral=True
            )
        elif self.channel_type == "voice":
            await interaction.guild.create_voice_channel(name)
            await interaction.response.send_message(
                f"Voice channel '{name}' created.", ephemeral=True
            )
