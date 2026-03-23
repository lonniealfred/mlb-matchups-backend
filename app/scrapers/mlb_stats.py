# app/scrapers/mlb_stats.py
import requests
from bs4 import BeautifulSoup

TEAM_STATS_URL = "https://www.espn.com/mlb/team/stats/_/name/{team_abbr}"

def fetch_team_hit_leaders(team_abbr: str):
  url = TEAM_STATS_URL.format(team_abbr=team_abbr.lower())
  resp = requests.get(url, timeout=10)
  resp.raise_for_status()
  soup = BeautifulSoup(resp.text, "html.parser")

  # Again, selectors will be tuned to real HTML
  rows = soup.select("table tbody tr")[:3]
  hitters = []
  for row in rows:
    cols = [c.get_text(strip=True) for c in row.select("td")]
    if not cols:
      continue
    name = cols[0]
    avg = cols[5]  # depends on table layout
    hr = cols[6]

    hitters.append({
      "name": name,
      "avg": avg,
      "hr": int(hr) if hr.isdigit() else 0,
    })

  return hitters
