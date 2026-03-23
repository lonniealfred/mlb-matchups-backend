# app/scrapers/mlb_scoreboard.py
import requests
from bs4 import BeautifulSoup
from datetime import date

SCOREBOARD_URL = "https://www.espn.com/mlb/scoreboard/_/date/{date_str}"

def fetch_scoreboard():
  today = date.today().strftime("%Y%m%d")
  url = SCOREBOARD_URL.format(date_str=today)
  resp = requests.get(url, timeout=10)
  resp.raise_for_status()
  soup = BeautifulSoup(resp.text, "html.parser")

  # This is pseudo-structure; you’ll tweak selectors after inspecting HTML
  games = []
  for game in soup.select(".Scoreboard"):
    home_team = game.select_one(".ScoreCell__Team--home .ScoreCell__TeamName").get_text(strip=True)
    away_team = game.select_one(".ScoreCell__Team--away .ScoreCell__TeamName").get_text(strip=True)
    game_time = game.select_one(".ScoreCell__Time").get_text(strip=True)

    games.append({
      "home_team": home_team,
      "away_team": away_team,
      "game_time": game_time,
      # you’ll later attach logos, pitchers, colors, etc.
    })

  return games
