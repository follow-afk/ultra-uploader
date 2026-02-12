# Ultra Uploader 🚀

A modernized, high-performance Telegram uploader built from the ground up for speed and reliability.

## Features

- **Blazing Fast**: Optimized with 32 workers and 10 concurrent transmissions.
- **Modern Architecture**: Clean package structure to avoid import issues.
- **Smart Progress**: Real-time progress bars with speed and ETA tracking.
- **Auto-Type Detection**: Automatically handles Videos, Audio, and Documents.
- **Topic Support**: Easily upload to specific forum topics.
- **Batch Upload**: Recursively upload entire directories.

## Installation

```bash
pip install pyrogram tgcrypto python-dotenv
```

## Setup

1. Get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
2. Create a `.env` file in the project root:
   ```env
   TG_API_ID=your_api_id
   TG_API_HASH=your_api_hash
   ```

## Usage

You can run the uploader directly using:

```bash
python3 -m ultra_uploader.cli <chat_id> <path_to_file_or_dir>
```

### Options

- `chat_id`: Target chat ID, username, or phone number.
- `path`: File or directory path to upload.
- `--caption`: Custom caption for the upload.
- `--force-document`: Disable media detection and upload as a generic file.
- `--delete`: Delete the local file after a successful upload.
- `--topic`: Specify a forum topic ID.

## Why this is better?

Unlike older scripts, **Ultra Uploader** uses a modular package design. This prevents the "ImportError: attempted relative import with no known parent package" error by allowing you to run it as a module (`python3 -m`). It also leverages the latest Pyrogram v2 features for maximum performance.
