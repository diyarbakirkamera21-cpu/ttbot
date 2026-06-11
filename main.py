from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

SOURCE_CHANNELS = ["@ww3media", "@Sancaktari"]
TARGET_CHANNEL = "@dunyadanhaberlerdeepweb"

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

# duplicate engel
seen = set()

# 🟢 ALBUM (3 foto + video vs BOZULMAZ)
@client.on(events.Album(chats=SOURCE_CHANNELS))
async def album_handler(event):
    try:
        key = event.grouped_id
        if key in seen:
            return
        seen.add(key)

        await client.send_file(
            TARGET_CHANNEL,
            event.messages
        )

    except Exception as e:
        print("Album hata:", e)


# 🟢 NORMAL MESAJ (text / tek medya)
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def message_handler(event):
    try:
        # album ise geç
        if event.grouped_id:
            return

        # duplicate engel
        if event.id in seen:
            return
        seen.add(event.id)

        msg = event.message

        # medya varsa dosya olarak gönder
        if msg.media:
            await client.send_file(TARGET_CHANNEL, msg.media, caption=msg.text or "")
        else:
            await client.send_message(TARGET_CHANNEL, msg.text)

    except Exception as e:
        print("Message hata:", e)


print("Bot çalışıyor...")

client.start()
client.run_until_disconnected()
