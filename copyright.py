
import os
import sys
import time
import datetime

from pyrogram import filters, Client, idle
from pyrogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import adduser, addchat

API_ID = 
API_HASH = ""
BOT_TOKEN = ""
DEVS = []

ALL_GROUPS = []
MEDIA_GROUPS = []
GROUP_MEDIAS = {}

RiZoeL = Client('Anti-CopyRight', api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

@RiZoel.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   adduser(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await rep.edit_text(f"🤖 **PONG**: `{ms}`ᴍs")

@RiZoeL.on_message(filters.user(Devs) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await RiZoeL.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@RiZoeL.on_message(filters.all)
async def watcher(_, message: Message):
   chat = message.chat
   
   if chat.id not in MEDIA_GROUPS:
      MEDIA_GROUPS.append(chat.id)
   if (message.video or message.photo):
      check = GROUP_MEDIAS.get(chat.id)
      if check:
         GROUP_MEDIAS[chat.id].append(message.id)
         print(f"Chat: {chat.title}, message ID: {message.id}")
      else:
         GROUP_MEDIAS[chat.id] = [message.id]

async def AutoDelete(RiZoeL: RiZoeL):
  async for i in MEDIA_GROUPS:
      list = GROUP_MEDIAS[i]
      await RiZoeL.delete_messages(i, list)
      MEDIA_GROUPS.remove(i)
  print("clean all medias ✓")
  print("waiting for 1 HR")


scheduler = AsyncIOScheduler()
scheduler.add_job(AutoDelete(RiZoeL), "delete_all_medias", seconds=3600)

scheduler.start()

if __name__ == "__main__":
   RiZoeL.start()
   idle()