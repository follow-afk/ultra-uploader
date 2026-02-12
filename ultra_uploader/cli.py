import os
import asyncio
import argparse
from .client import UltraClient
from .uploader import upload_file

async def run_uploader(args):
    """Main logic to handle CLI arguments and start the upload process."""
    if not os.getenv("TG_API_ID") or not os.getenv("TG_API_HASH"):
        print("Telegram API credentials not found.")
        api_id = input("Enter TG_API_ID: ").strip()
        api_hash = input("Enter TG_API_HASH: ").strip()
        
        with open(".env", "a") as f:
            f.write(f"\nTG_API_ID={api_id}\nTG_API_HASH={api_hash}\n")
        os.environ["TG_API_ID"] = api_id
        os.environ["TG_API_HASH"] = api_hash

    client = UltraClient()
    await client.start()
    
    try:
        path = args.path
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            return

        files_to_upload = []
        if os.path.isfile(path):
            files_to_upload.append(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_upload.append(os.path.join(root, file))
        
        files_to_upload.sort()
        print(f"Found {len(files_to_upload)} files to upload.")

        for file_path in files_to_upload:
            await upload_file(
                client,
                args.chat_id,
                file_path,
                caption=args.caption,
                force_document=args.force_document,
                thread_id=args.topic,
                delete_on_success=args.delete
            )
            await asyncio.sleep(1)
            
    finally:
        await client.stop()

def main():
    parser = argparse.ArgumentParser(description="Ultra High-Speed Telegram Uploader")
    parser.add_argument("chat_id", help="Target Chat ID or Username")
    parser.add_argument("path", help="File or Directory path to upload")
    parser.add_argument("--caption", help="Custom caption for uploads")
    parser.add_argument("--force-document", action="store_true", help="Force upload as document")
    parser.add_argument("--delete", action="store_true", help="Delete file after successful upload")
    parser.add_argument("--topic", type=int, help="Topic ID (for forum threads)")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_uploader(args))
    except KeyboardInterrupt:
        print("\nAborted by user.")

if __name__ == "__main__":
    main()
