import subprocess
import time

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # 1. Scrape latest rosters
    run("py scrape_mlb_rosters.py")

    # 2. Generate TS map
    run("py generate_player_photos.py")

    # 3. Convert TS → JSON
    run("py convert_ts_to_json.py")

    # 4. Download ESPN headshots
    run("py download_player_photos.py")

    print("\n✔ Nightly photo update complete.")

if __name__ == "__main__":
    main()
