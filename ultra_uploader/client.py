import os
from pyrogram import Client, enums
from dotenv import load_dotenv

class UltraClient(Client):
    """Custom Pyrogram Client optimized for high-speed uploads."""
    
    def __init__(self, session_name="ultra_uploader"):
        load_dotenv()
        
        api_id = os.getenv("TG_API_ID")
        api_hash = os.getenv("TG_API_HASH")
        
        if not api_id or not api_hash:
            # We'll handle prompting in the CLI part, but for the class, we need these.
            api_id = os.getenv("TG_API_ID", "0")
            api_hash = os.getenv("TG_API_HASH", "")

        super().__init__(
            name=session_name,
            api_id=int(api_id) if api_id.isdigit() else 0,
            api_hash=api_hash,
            parse_mode=enums.ParseMode.HTML,
            workers=32, # High worker count for better concurrency
            max_concurrent_transmissions=10, # Optimized for speed
            sleep_threshold=60,
            no_updates=True
        )
