import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from claude import Claude
import aiohttp
import asyncio
import time
from io import BytesIO
from PIL import Image
import base64

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

recent_users = {}

@tree.command(name='divination', description='わしがおぬしのスタンドを占ってやる')
async def profile(interaction: discord.Interaction):
    user_id = interaction.user.id
    current_time = time.time()

    if user_id in recent_users and current_time - recent_users[user_id] < 300:
        remaining_time = 300 - (current_time - recent_users[user_id])
        minutes, seconds = divmod(remaining_time, 60)
        await interaction.response.send_message(f"おぬしはさっきも占っただろう！{int(minutes):02d}:{int(seconds):02d}待ちな！")
        return

    recent_users[user_id] = current_time

    await interaction.response.send_message("占い中...", ephemeral=True)

    messages = []
    for channel in interaction.guild.text_channels:
        try:
            async for message in channel.history(limit=20):
                msg_count = 0
                if message.author == interaction.user:
                    messages.append(message.content)
                    msg_count += 1
                    if len(messages) >= 30 or len("\n\n".join(messages)) > 500 or msg_count > 3:
                      break 
        except discord.errors.Forbidden:
            pass
        if len(messages) >= 30 or len("\n\n".join(messages)) > 500:
            break

    messages.reverse()
    user_messages = "\n\n".join(messages)

    user_name = str(interaction.user.display_name or interaction.user)
    avatar_url = interaction.user.avatar.url

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            avatar_data = await response.read()

    with Image.open(BytesIO(avatar_data)) as avatar_image:
        avatar_image.thumbnail((512, 512))
        buffered = BytesIO()
        avatar_image.save(buffered, format="PNG")
        avatar_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    claude = Claude(CLAUDE_API_KEY)
    profile = claude.generate_profile(user_name, user_messages, avatar_base64)

    print(f"{user_name}: {profile}")

    # Send the profile to another API and get the response
    stand_data = claude.divination_stand(user_name, profile)

    await interaction.edit_original_response(content="占いが完了しました！")
    await interaction.followup.send(f"これがおぬしのスタンドじゃ！\n\n{stand_data}")

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

client.run(DISCORD_TOKEN)