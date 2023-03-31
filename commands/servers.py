import requests
import nextcord

async def serverswbot(interaction: nextcord.Interaction):
    servers = interaction.client.guilds
    message = "My bot is in the following servers:\n"
    
    for server in servers:
        server_link = f"https://discord.com/channels/{server.id}"
        server_name = server.name
        message += f"\n- [{server_name}]({server_link})"
    
    await interaction.response.send_message(message)