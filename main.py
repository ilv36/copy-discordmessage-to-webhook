# ปรับบรรทัดที่ 27 ได้ว่าจะดึงข้อความมาเท่าไหร่
# ไม่สามารถดึงรูปภาพ,วิดีโอและ gif ได้
# เขียนโดย ilv ;) 
# ใช้ไม่ได้ติดต่อ ilv พร้อมสอนตลอด 24 ชั่วโมง

import discord
import requests
from discord.ext import commands

TOKEN = input("TOKEN: ")
CHANNEL_ID = int(input("CHANNEL ID: "))
WEBHOOK_URL = input("WEBHOOK URL: ")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = commands.Bot(command_prefix="!", intents=intents, self_bot=True)

@client.event
async def on_ready():
    print(f'Login  {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    
    if channel:
        messages = await channel.history(limit=100).flatten()
        
        for message in messages[::-1]:  
            if not any(attachment.content_type.startswith('image') for attachment in message.attachments):
                data = {
                    "content": message.content,
                    "username": message.author.name,
                    "avatar_url": str(message.author.avatar_url)   
                }
                response = requests.post(WEBHOOK_URL, json=data)

                if response.status_code == 204:
                    print(f"ข้อความจาก {message.author.name}: '{message.content}' ถูกส่งไปที่ Webhook สำเร็จแล้ว!")
                else:
                    print(f"เกิดข้อผิดพลาดในการส่งข้อความไปที่ Webhook: {response.status_code}")
    else:
        print(f"ไม่พบช่องที่มี ID : {CHANNEL_ID}")

    await client.close()

client.run(TOKEN, bot=False)