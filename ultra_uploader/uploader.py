import os
import time
import asyncio
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from .utils import ProgressTracker, human_bytes

async def upload_progress(current, total, message, tracker):
    """Callback for pyrogram upload progress."""
    if tracker.should_update() or current == total:
        text = tracker.get_progress_text(current)
        if text:
            try:
                await message.edit_text(text)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass

async def upload_file(client, chat_id, file_path, caption=None, force_document=False, thread_id=None, delete_on_success=False):
    """Uploads a single file with optimized settings and progress tracking."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    status_message = await client.send_message(
        chat_id=chat_id,
        text=f"<code>Initializing upload for {file_name}...</code>",
        message_thread_id=thread_id
    )

    tracker = ProgressTracker(file_size, description=f"Uploading {file_name}")
    
    try:
        is_video = file_name.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))
        is_audio = file_name.lower().endswith(('.mp3', '.m4a', '.flac', '.wav'))
        
        final_caption = caption if caption else f"<code>{file_name}</code>"
        
        start_time = time.time()
        
        if is_video and not force_document:
            await client.send_video(
                chat_id=chat_id,
                video=file_path,
                caption=final_caption,
                progress=upload_progress,
                progress_args=(status_message, tracker),
                message_thread_id=thread_id
            )
        elif is_audio and not force_document:
            await client.send_audio(
                chat_id=chat_id,
                audio=file_path,
                caption=final_caption,
                progress=upload_progress,
                progress_args=(status_message, tracker),
                message_thread_id=thread_id
            )
        else:
            await client.send_document(
                chat_id=chat_id,
                document=file_path,
                caption=final_caption,
                progress=upload_progress,
                progress_args=(status_message, tracker),
                message_thread_id=thread_id
            )
            
        end_time = time.time()
        duration = end_time - start_time
        avg_speed = file_size / duration if duration > 0 else 0
        
        await status_message.edit_text(
            f"✅ <b>Upload Complete!</b>\n"
            f"📄 <b>File:</b> <code>{file_name}</code>\n"
            f"📊 <b>Size:</b> {human_bytes(file_size)}\n"
            f"⏱️ <b>Time:</b> {int(duration)}s\n"
            f"🚀 <b>Avg Speed:</b> {human_bytes(avg_speed)}/s"
        )
        if delete_on_success:
            os.remove(file_path)
        return True
        
    except Exception as e:
        await status_message.edit_text(f"❌ <b>Upload Failed!</b>\nError: <code>{str(e)}</code>")
        print(f"Error uploading {file_name}: {e}")
        return False
