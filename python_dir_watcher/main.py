from pathlib import Path
import subprocess
import datetime
import asyncio

WATCHED_DIR = Path('watched_dir')
LOG_FILE = Path('activity.log')
INTERVAL = 60 

def snapshot():
    return {f: f.stat().st_mtime for f in WATCHED_DIR.rglob('*') if f.is_file()}

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def run_external_command():
    subprocess.run(['echo', 'Changes found!'], capture_output=True)

async def main():
    previous_snapshot = snapshot()
    
    while True:
        await asyncio.sleep(INTERVAL)
        current_snapshot = snapshot()
        
        added_files = current_snapshot.keys() - previous_snapshot.keys()

        removed_files = previous_snapshot.keys() - current_snapshot.keys()

        modified_files = {f for f in current_snapshot
            if f in previous_snapshot and current_snapshot[f] != previous_snapshot[f]}
        
        if added_files or removed_files or modified_files:
            log(f"Found changes: +{len(added_files)} ~{len(modified_files)} -{len(removed_files)}")
            run_external_command()
        previous_snapshot = current_snapshot

if __name__ == "__main__":
    asyncio.run(main())