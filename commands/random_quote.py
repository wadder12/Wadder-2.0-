import requests
import nextcord

async def random_quotes(interaction: nextcord.Interaction):
    response = requests.get("https://api.quotable.io/random")
    data = response.json()
    quote = data["content"]
    author = data["author"]
    await interaction.response.send_message(f"{quote} - {author}")