import os
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# logs
logging.basicConfig(level=logging.WARNING)

# ENV
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = str(os.getenv("API_HASH", ""))
STRING_SESSION = str(os.getenv("STRING_SESSION", ""))

# KANALLAR
SOURCE_CHANNELS = ["@ww3media", "@Sancaktari"]
TARGET_CHANNEL = "@dunyadanhaberlerdeepweb"

# FOOTER
FOOTER = "\n\n⚡ @dunyadanhaberlerdeepweb"

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

# duplicate engel
seen_groups = set()
seen_messages = set()


@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    # ───────── ALBUM ─────────
    if event.grouped_id:

        gid = event.grouped_id
        if gid in seen_groups:
            return
        seen_groups.add(gid)

        try:
            await client.send_file(
                TARGET_CHANNEL,
                event.message,
                caption=FOOTER
            )
        except Exception as e:
            print("Album hata:", e)

        return

    # ───────── NORMAL MESAJ ─────────
    mid = (event.chat_id, event.id)

    if mid in seen_messages:
        return
    seen_messages.add(mid)

    try:
        msg = event.message

        # medya
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

    except Exception as e:
        print("Message hata:", e)


print("🚀 Bot çalışıyor...")

client.run_until_disconnected()
