import math
import time

def human_bytes(size: int) -> str:
    """Converts bytes to a human-readable string."""
    if not size:
        return "0 B"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return f"{s} {units[i]}"

def format_time(seconds: int) -> str:
    """Formats seconds into a readable string (HH:MM:SS)."""
    if seconds < 0:
        return "00:00:00"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

class ProgressTracker:
    """Tracks and formats upload progress with throttling to reduce overhead."""
    def __init__(self, total_size, description="Uploading"):
        self.total_size = total_size
        self.description = description
        self.start_time = time.time()
        self.last_update_time = 0
        self.update_interval = 3.0 # Update Telegram every 3 seconds

    def get_progress_text(self, current):
        now = time.time()
        elapsed = now - self.start_time
        
        # Avoid division by zero
        if elapsed <= 0 or current <= 0:
            return None
            
        speed = current / elapsed
        eta = (self.total_size - current) / speed if speed > 0 else 0
        percentage = (current / self.total_size) * 100
        
        # Create progress bar
        completed = int(percentage / 5)
        bar = "█" * completed + "░" * (20 - completed)
        
        return (
            f"<b>{self.description}</b>\n"
            f"<code>[{bar}] {percentage:.2f}%</code>\n"
            f"📦 <b>Size:</b> {human_bytes(current)} / {human_bytes(self.total_size)}\n"
            f"🚀 <b>Speed:</b> {human_bytes(speed)}/s\n"
            f"⏳ <b>ETA:</b> {format_time(int(eta))}"
        )

    def should_update(self):
        now = time.time()
        if now - self.last_update_time >= self.update_interval:
            self.last_update_time = now
            return True
        return False
