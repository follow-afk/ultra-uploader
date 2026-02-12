#!/usr/bin/env python3
import os
import sys
import time
import math
import asyncio
import argparse
from getpass import getpass

# ---------------------------------------------------------
# 1. INSTALL DEPENDENCIES (FOR COLAB)
# ---------------------------------------------------------
try:
    import pyrogram
    import nest_asyncio
except ImportError:
    print("Installing required libraries...")
    os.system("pip install pyrogram tgcrypto nest-asyncio python-dotenv")
    import pyrogram
    import nest_asyncio

from pyrogram import Client, enums
from pyrogram.errors import FloodWait

# ---------------------------------------------------------
# 2. UTILITIES
# ---------------------------------------------------------
def human_bytes(size: int) -> str:
    if not size: return "0 B"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    i = int(math.floor(math.log(size, 1024)))
    return f"{round(size / math.pow(1024, i), 2)} {units[i]}"

def format_time(seconds: int) -> str:
    if seconds < 0: return "00:00:00"
    m, s = divmod(seconds, 60); h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

class ProgressTracker:
    def __init__(self, total_size, description="Uploading"):
        self.total_size = total_size
        self.description = description
        self.start_time = time.time()
        self.last_update_time = 0
        self.update_interval = 3.5

    def get_text(self, current):
        now = time.time(); elapsed = now - self.start_time
        if elapsed <= 0 or current <= 0: return None
        speed = current / elapsed
        eta = (self.total_size - current) / speed if speed > 0 else 0
        percentage = (current / self.total_size) * 100
        bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
        return (f"<b>{self.description}</b>\n<code>[{bar}] {percentage:.2f}%</code>\n"
                f"📦 <b>Size:</b> {human_bytes(current)} / {human_bytes(self.total_size)}\n"
                f"🚀 <b>Speed:</b> {human_bytes(speed)}/s\n⏳ <b>ETA:</b> {format_time(int(eta))}")

    def should_update(self):
        now = time.time()
        if now - self.last_update_time >= self.update_interval:
            self.last_update_time = now; return True
        return False

# ---------------------------------------------------------
# 3. UPLOADER LOGIC
# ---------------------------------------------------------
async def upload_progress(current, total, message, tracker):
    if tracker.should_update() or current == total:
        text = tracker.get_text(current)
        if text:
            try: await message.edit_text(text)
            except FloodWait as e: await asyncio.sleep(e.value)
            except Exception: pass

async def upload_file(client, chat_id, file_path, caption=None, force_doc=False, thread_id=None, delete=False):
    if not os.path.exists(file_path): return False
    file_name = os.path.basename(file_path); file_size = os.path.getsize(file_path)
    status = await client.send_message(chat_id, f"<code>Initializing {file_name}...</code>", message_thread_id=thread_id)
    tracker = ProgressTracker(file_size, f"Uploading {file_name}")
    try:
        is_vid = file_name.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))
        is_aud = file_name.lower().endswith(('.mp3', '.m4a', '.flac', '.wav'))
        cap = caption if caption else f"<code>{file_name}</code>"
        params = {"chat_id": chat_id, "caption": cap, "progress": upload_progress, 
                  "progress_args": (status, tracker), "message_thread_id": thread_id}
        
        if is_vid and not force_doc: await client.send_video(video=file_path, **params)
        elif is_aud and not force_doc: await client.send_audio(audio=file_path, **params)
        else: await client.send_document(document=file_path, **params)
        
        await status.edit_text(f"✅ <b>Done:</b> <code>{file_name}</code>\n📊 <b>Size:</b> {human_bytes(file_size)}")
        if delete: os.remove(file_path)
        return True
    except Exception as e:
        await status.edit_text(f"❌ <b>Failed:</b> {file_name}\nError: <code>{str(e)}</code>")
        return False

# ---------------------------------------------------------
# 4. MAIN ENTRY POINT
# ---------------------------------------------------------
async def main_async():
    parser = argparse.ArgumentParser(description="Ultra Uploader for Colab")
    parser.add_argument("chat_id", help="Chat ID or Username")
    parser.add_argument("path", help="File or Folder path")
    parser.add_argument("--caption", help="Custom caption")
    parser.add_argument("--force-doc", action="store_true", help="Force as document")
    parser.add_argument("--delete", action="store_true", help="Delete after upload")
    parser.add_argument("--topic", type=int, help="Topic ID")
    args = parser.parse_args()

    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    if not api_id or not api_hash:
        print("\n--- Telegram Credentials Setup ---")
        api_id = input("Enter API_ID: ").strip()
        api_hash = input("Enter API_HASH: ").strip()
        os.environ["TG_API_ID"] = api_id
        os.environ["TG_API_HASH"] = api_hash

    client = Client("colab_session", api_id=int(api_id), api_hash=api_hash, 
                    workers=32, max_concurrent_transmissions=10, parse_mode=enums.ParseMode.HTML)
    await client.start()
    try:
        files = [args.path] if os.path.isfile(args.path) else [os.path.join(r, f) for r, _, fs in os.walk(args.path) for f in fs]
        files.sort()
        print(f"🚀 Found {len(files)} files. Starting...")
        for f in files:
            await upload_file(client, args.chat_id, f, args.caption, args.force_doc, args.topic, args.delete)
            await asyncio.sleep(1)
    finally:
        await client.stop()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main_async())
