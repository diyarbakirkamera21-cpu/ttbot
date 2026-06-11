from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio

API_ID = 38539979
API_HASH = "c763435d9e2e6397992c3cf60448ad33"
STRING_SESSION = "1BJWap1sBu5fPGaQonTVjHfaV82jvH7arf_zQOVD5lXsSYm299ymGfhQ6OUbt5b2vHVa5q65ugMkGAHEY5-5DrwwBOb4ydpby-adhMGuAzdOi3Utm3fI7Xm0DqqyIuyILZheZjCX0xXQ7CL26DZkzNyIT_Fi2J5iEL9u1HxRq3rE30PxI0dtLaTOuYEAL42Q3Q5ySIq4IwjirThlg5GExm3Wf2vFoB6gBUsrWDy2FRXHnZb9PX1IH9Jop2urgRmeC4cNfMM37GtIAhFVpuhfJ-Q_-Na0b0m0ALMr3bDQE486tyjag2rip_XnrX1b0PyaUwkSNX-kdBKnbxkQoqb6OUcGN-wbWWaQ="

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