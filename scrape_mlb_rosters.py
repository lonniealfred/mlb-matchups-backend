import httpx
import csv
import time

OUTPUT_CSV = "players.csv"

TEAMS = [
    "atl", "mia", "nym", "phi", "wsh",
    "chc", "cin", "mil", "pit", "stl",
    "ari", "col", "lad", "sd", "sf",
    "bal", "bos", "nyy", "tb", "tor",
    "chw", "cle", "det", "kc", "min",
    "hou", "laa", "oak", "sea", "tex",
]

ROSTER_URL = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/teams/{team}/roster"

def fetch_roster(team):
    try:
        r = httpx.get(ROSTER_URL.format(team=team), timeout=10)
        data = r.json()
        return data.get("athletes", [])
    except Exception as e:
        print(f"Error fetching roster for {team}: {e}")
        return []

def main():
    players = []

    for team in TEAMS:
        print(f"Fetching roster for {team}...")
        roster = fetch_roster(team)

        for group in roster:
            for athlete in group.get("items", []):
                name = athlete.get("fullName")
                if name:
                    players.append(name)

        time.sleep(0.3)

    players = sorted(set(players))

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        for name in players:
            writer.writerow([name])

    print(f"Saved {len(players)} players to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
