# 🚀 Ultra Uploader: Google Colab Master Guide

This guide will walk you through running the Ultra Uploader in Google Colab, from scratch to advanced usage. We have optimized the code specifically to handle Colab's unique environment.

---

## 🛠️ Step 1: Initial Setup

Run this in your first Colab cell to install all required libraries.

```python
# 1. Install dependencies
!pip install pyrogram tgcrypto python-dotenv nest-asyncio

# 2. Clone the repository
!git clone https://github.com/follow-afk/ultra-uploader.git
%cd ultra-uploader
```

---

## 🔑 Step 2: Configuration

You need your Telegram API credentials. If you don't have them, get them from [my.telegram.org](https://my.telegram.org).

Run this cell to set your credentials securely without exposing them in the code.

```python
import os
from getpass import getpass

# Enter your credentials when prompted
api_id = getpass("Enter your TG_API_ID: ")
api_hash = getpass("Enter your TG_API_HASH: ")

# Save to environment variables for the uploader to use
os.environ["TG_API_ID"] = api_id
os.environ["TG_API_HASH"] = api_hash

print("✅ Credentials set successfully!")
```

---

## 📤 Step 3: Running the Uploader

Now you can upload files or directories. 

### Basic Usage (Single File)
```python
# Replace 'your_chat_id' with your target ID or username
# Replace 'path/to/file' with the actual file path in Colab
!python3 -m ultra_uploader.cli "your_chat_id" "/content/sample_data/README.md" --progress
```

### Advanced Usage (Directory Upload)
```python
# This will upload everything in the folder
!python3 -m ultra_uploader.cli "your_chat_id" "/content/my_folder" --progress --caption "Batch Upload"
```

---

## 💡 Pro Tips & Advanced Options

| Option | Description |
| :--- | :--- |
| `--force-document` | Upload videos/audio as files (disables streaming). |
| `--delete` | Automatically delete the file from Colab after a successful upload. |
| `--topic 123` | Upload to a specific forum topic (use the thread ID). |
| `--caption "text"` | Add a custom caption to all uploaded files. |

---

## ❓ Troubleshooting Common Errors

### 1. `ImportError: attempted relative import...`
**Fix:** Always run using `python3 -m ultra_uploader.cli`. Do not run the script file directly.

### 2. `asyncio.run() cannot be called from a running event loop`
**Fix:** This version of Ultra Uploader includes a built-in patch (`nest_asyncio`) to handle this. If you still see it, ensure you installed `nest-asyncio` in Step 1.

### 3. `FloodWait` (Telegram Limiting)
**Fix:** Our code automatically handles this by pausing and resuming. If it happens frequently, increase the `await asyncio.sleep()` value in `cli.py`.

### 4. `Session Lock`
**Fix:** If you get a database lock error, restart your Colab runtime (`Runtime -> Restart runtime`) and run Step 2 again.

---

## 🌟 Why use this over others?
- **Speed:** Uses 32 workers for multi-part uploads.
- **Reliability:** Custom-built for Pyrogram v2.x.
- **Colab Optimized:** Specifically patched for Jupyter environments.
