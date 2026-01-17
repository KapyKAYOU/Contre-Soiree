import os 
from datetime import datetime 
import shutil

def backup_pseudos():
    if not os.path.exists("pseudos.txt"):
        return None

    os.makedirs("backups", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backups/pseudos_{timestamp}.txt"

    with open("pseudos.txt", "r", encoding="utf-8") as src:
        content = src.read()

    with open(backup_name, "w", encoding="utf-8") as dst:
        dst.write(content)

    return backup_name