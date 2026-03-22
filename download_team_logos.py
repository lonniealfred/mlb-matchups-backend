import httpx
import os

OUTPUT_DIR = "public/logos/"
TEAM_URL = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/teams/{team}"

TEAMS = [
    "atl", "mia", "nym", "phi", "wsh",
    "chc", "cin", "mil", "pit", "stl",
    "ari", "col", "lad", "sd", "sf",
    "bal", "bos", "nyy", "tb", "tor",
    "chw", "cle", "det", "kc", "min",
    "hou", "laa", "oak", "sea", "tex",
]

def download(url, path):
    try:
        r = httpx.get(url, timeout=10)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for team in TEAMS:
        print(f"Fetching logo for {team}...")
        data = httpx.get(TEAM_URL.format(team=team)).json()

        logo = data.get("team", {}).get("logos", [{}])[0].get("href")
        if not logo:
            print(f"No logo found for {team}")
            continue

        path = os.path.join(OUTPUT_DIR, f"{team}.png")
        download(logo, path)

    print("\n✔ Team logos downloaded.")

if __name__ == "__main__":
    main()
