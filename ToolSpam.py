import discord
import asyncio
import os
from dotenv import load_dotenv

# Load token từ file .env
load_dotenv("/storage/emulated/0/Download/.env")
TOKEN = os.getenv("DISCORD_TOKEN")

# ID của kênh và user chủ bot
CHANNEL_ID = 1364890863410352180
OWNER_ID = 1328308734627418213  # ← Thay bằng user ID thật của bạn

FILE_PATH = 'noidung.txt'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
spamming = {}

@client.event
async def on_ready():
    print(f'Bot đã đăng nhập: {client.user}')

@client.event
async def on_message(message):
    global spamming

    if message.author == client.user:
        return

    if message.author.id != OWNER_ID:
        return  # Chặn người lạ dùng bot

    if message.content.strip().lower() == "!spam":
        if spamming.get(message.channel.id):
            await message.channel.send("Đang spam rồi!")
            return

        spamming[message.channel.id] = True
        await message.channel.send("Bắt đầu gửi nội dung...")

        try:
            while spamming[message.channel.id]:
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    content = f.read()

                formatted = '\n'.join([f"> # {line}" for line in content.splitlines()])
                await message.channel.send(formatted)

                await asyncio.sleep(5)
                await message.channel.send("Tạm nghỉ 20 giây...")
        except Exception as e:
            await message.channel.send(f"Lỗi: {e}")

    elif message.content.strip().lower() == "/stop":
        spamming[message.channel.id] = False
        await message.channel.send("Đã dừng spam.")

client.run(TOKEN)
