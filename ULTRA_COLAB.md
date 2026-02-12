# 🚀 ULTRA UPLOADER: ONE-CELL COLAB GUIDE

This is the **foolproof** way to run the uploader in Google Colab. No package errors, no import issues.

### 📋 How to Use:
1. **Copy** the code below.
2. **Paste** it into a **single cell** in Google Colab.
3. **Run** the cell. It will ask for your API credentials and the file you want to upload.

---

### 💻 The "One-Cell" Code:
```python
# --- ULTRA UPLOADER FOR COLAB (COPY EVERYTHING BELOW) ---
import os, sys, time, math, asyncio, argparse
from getpass import getpass

# 1. Install & Patch
os.system("pip install -q pyrogram tgcrypto nest-asyncio")
import nest_asyncio
nest_asyncio.apply()

try:
    from pyrogram import Client, enums
    from pyrogram.errors import FloodWait
except ImportError:
    print("Please run the cell again to complete installation.")

# 2. Config & Helper Functions
def human_bytes(size):
    if not size: return "0 B"
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024: return f"{size:.2f} {unit}"
        size /= 1024

async def progress(current, total, message, start_time, last_update):
    now = time.time()
    if now - last_update[0] < 4 and current != total: return
    last_update[0] = now
    elapsed = now - start_time
    speed = current / elapsed if elapsed > 0 else 0
    perc = (current / total) * 100
    bar = "█" * int(perc / 5) + "░" * (20 - int(perc / 5))
    text = f"<b>Uploading...</b>\n<code>[{bar}] {perc:.2f}%</code>\n🚀 {human_bytes(speed)}/s"
    try: await message.edit_text(text)
    except: pass

# 3. Execution
async def run_ultra():
    print("--- 🛠️ Setup ---")
    api_id = input("Enter API_ID: ")
    api_hash = input("Enter API_HASH: ")
    chat_id = input("Enter Target Chat ID/Username: ")
    file_path = input("Enter File/Folder Path in Colab: ")
    
    async with Client("ultra", int(api_id), api_hash, workers=32) as app:
        files = [file_path] if os.path.isfile(file_path) else [os.path.join(r, f) for r, _, fs in os.walk(file_path) for f in fs]
        print(f"📦 Found {len(files)} files. Starting...")
        for f in sorted(files):
            name = os.path.basename(f)
            status = await app.send_message(chat_id, f"<code>Processing {name}...</code>")
            start_time = time.time()
            last_update = [0]
            await app.send_document(chat_id, f, progress=progress, progress_args=(status, start_time, last_update))
            await status.edit_text(f"✅ <b>Done:</b> <code>{name}</code>")

asyncio.run(run_ultra())
```

---

### 🌟 Why this works?
- **Self-Contained:** No external files to import. Everything is in one cell.
- **Auto-Install:** Automatically installs dependencies if they are missing.
- **Colab Ready:** Uses `nest_asyncio` to prevent event loop crashes.
- **Simple:** No complex CLI arguments, just follow the prompts.
