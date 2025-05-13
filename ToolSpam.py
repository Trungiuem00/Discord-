import discord
import asyncio
import os
import threading
from flask import Flask
from dotenv import load_dotenv

# Tải token từ file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Cấu hình bot
CHANNEL_ID = 1364890863410352180
OWNER_ID = 1328308734627418213
FILE_PATH = 'noidung.txt'  # Tên file nằm cùng thư mục

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
        return

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

                await asyncio.sleep(20)
                await message.channel.send("Tạm nghỉ 20 giây...")
        except Exception as e:
            await message.channel.send(f"Lỗi: {e}")

    elif message.content.strip().lower() == "/stop":
        spamming[message.channel.id] = False
        await message.channel.send("Đã dừng spam.")

# Flask server để giữ Render không ngủ
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running."

@app.route('/ping')
def ping():
    return "pong"

# Chạy Flask song song với bot
def run_flask():
    import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
  # Port mặc định Render

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    client.run(TOKEN)
