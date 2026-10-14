"""Lance un Chromium "normal" (sans flags d'automatisation) avec un port CDP.

Le profil est persistant (./profile) : tu te connectes à Suno une seule fois.
Les autres scripts (fill.py, inspect_page.py) se branchent dessus via CDP.
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
PROFILE = ROOT / "profile"
PORT = 9222
URL = "https://suno.com/create"


def main():
    with sync_playwright() as p:
        exe = p.chromium.executable_path
    proc = subprocess.Popen(
        [
            exe,
            f"--remote-debugging-port={PORT}",
            f"--user-data-dir={PROFILE}",
            "--no-first-run",
            "--no-default-browser-check",
            URL,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print(f"Chromium lancé (pid {proc.pid}), CDP sur http://127.0.0.1:{PORT}")
    print("Connecte-toi à Suno dans la fenêtre si ce n'est pas déjà fait.")
    if "--wait" in sys.argv:
        proc.wait()


if __name__ == "__main__":
    main()
