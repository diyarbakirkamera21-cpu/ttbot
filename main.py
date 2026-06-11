import os
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.WARNING)


API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
STRING_SESSION = os.getenv("STRING_SESSION")

# 🔥 CHECK (EN ÖNEMLİ KISIM)
if not API_ID or not API_HASH or not STRING_SESSION:
    print("❌ ENV eksik! Railway variables kontrol et")
    exit()

API_ID = int(API_ID)

SOURCE_CHANNELS = ["@ww3media", "@Sancaktari"]
TARGET_CHANNEL = "@dunyadanhaberlerdeepweb"

FOOTER = "\n\n⚡ @dunyadanhaberlerdeepweb"

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

seen_groups = set()
seen_messages = set()


@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    if event.grouped_id:
        if event.grouped_id in seen_groups:
            return
        seen_groups.add(event.grouped_id)

        await client.send_file(
            TARGET_CHANNEL,
            event.message,
            caption=FOOTER
        )
        return

    mid = (event.chat_id, event.id)

    if mid in seen_messages:
        return
    seen_messages.add(mid)

    msg = event.message

    if msg.media:
        await client.send_file(
            TARGET_CHANNEL,
            msg.media,
            caption=(msg.text or "") + FOOTER
        )
    else:
        if msg.text:
            await client.send_message(
                TARGET_CHANNEL,
                msg.text + FOOTER
            )

print("🚀 Bot çalışıyor...")
client.run_until_disconnected()
