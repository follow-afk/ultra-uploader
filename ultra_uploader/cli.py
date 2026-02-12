import os
import asyncio
import argparse
import sys
from .client import UltraClient
from .uploader import upload_file

def patch_for_colab():
    """Patches asyncio to allow running within Google Colab/Jupyter environments."""
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        # If not in Colab or nest_asyncio not installed, we continue normally
        pass

async def run_uploader(args):
    """Main logic to handle CLI arguments and start the upload process."""
    # Check for credentials in environment or .env
    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    
    if not api_id or not api_hash:
        print("\n❌ Telegram API credentials not found!")
        print("Please set TG_API_ID and TG_API_HASH environment variables.")
        return

    client = UltraClient()
    await client.start()
    
    try:
        path = args.path
        if not os.path.exists(path):
            print(f"❌ Error: Path '{path}' does not exist.")
            return

        files_to_upload = []
        if os.path.isfile(path):
            files_to_upload.append(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_upload.append(os.path.join(root, file))
        
        files_to_upload.sort()
        if not files_to_upload:
            print("⚠️ No files found to upload.")
            return
            
        print(f"📦 Found {len(files_to_upload)} files to upload.")

        for file_path in files_to_upload:
            success = await upload_file(
                client,
                args.chat_id,
                file_path,
                caption=args.caption,
                force_document=args.force_document,
                thread_id=args.topic,
                delete_on_success=args.delete
            )
            if success:
                # Small delay between uploads to prevent flood
                await asyncio.sleep(1.5)
            
    finally:
        await client.stop()

def main():
    parser = argparse.ArgumentParser(description="Ultra High-Speed Telegram Uploader (Colab Optimized)")
    parser.add_argument("chat_id", help="Target Chat ID or Username")
    parser.add_argument("path", help="File or Directory path to upload")
    parser.add_argument("--caption", help="Custom caption for uploads")
    parser.add_argument("--force-document", action="store_true", help="Force upload as document")
    parser.add_argument("--delete", action="store_true", help="Delete file after successful upload")
    parser.add_argument("--topic", type=int, help="Topic ID (for forum threads)")
    
    args = parser.parse_args()
    
    # Patch for Colab/Jupyter before running
    patch_for_colab()
    
    try:
        # Check if an event loop is already running (e.g., in Colab)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # In Colab/Jupyter, we create a task instead of using asyncio.run()
            future = asyncio.ensure_future(run_uploader(args))
            # We don't want to block the cell if it's being run as a module, 
            # but in Colab we usually want to wait for it.
            # However, the proper way in a notebook is just to await the coroutine directly.
            # But for a CLI entry point, this is the best compatibility layer.
        else:
            asyncio.run(run_uploader(args))
            
    except KeyboardInterrupt:
        print("\n🛑 Aborted by user.")
    except Exception as e:
        print(f"\n💥 An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
