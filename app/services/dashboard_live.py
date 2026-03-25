import httpx
from datetime import datetime

from app.demo.demo_games import DEMO_GAMES
from app.demo.demo_hitters import DEMO_HITTERS
from app.demo.demo_trends import DEMO_TRENDS

# ---------------------------------------------------------
# SCRAPER STATUS TRACKING
# ---------------------------------------------------------

_last_scrape_status = {
    "mode": "unknown",
    "games_found": 0,
    "timestamp": None,
}

def record_scrape_status(mode: str, games_found: int):
    """Store the most recent scrape status for /scraper/status."""
    global _last_scrape_status
    _last_scrape_status = {
        "mode": mode,
        "games_found": games_found,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

def get_scraper_status():
    """Return the last scrape status."""
    return _last_scrape_status


# ---------------------------------------------------------
# ESPN SCRAPING
# ---------------------------------------------------------

ESPN_SCOREBOARD_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
)

async def fetch_scoreboard():
    """Fetch MLB scoreboard from ESPN."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(ESPN_SCOREBOARD_URL)
            data = res.json()
            return data.get("events", [])
    except Exception:
        return []


# ---------------------------------------------------------
# FLATTEN TRENDS (Option A)
# ---------------------------------------------------------

def flatten_trends(trends_obj):
    """Convert nested trends object into a flat list of {label, value} items."""
    flat = []

    # Stadium HR factors
    for item in trends_obj.get("stadium_factors", []):
        flat.append({
            "label": f"{item['stadium']} HR Factor",
            "value": item["hr_factor"]
        })

    # Weather factors
    for item in trends_obj.get("weather_factors", []):
        flat.append({
            "label": f"{item['stadium']} Weather",
            "value": item["wind"]
        })

    # Momentum
    for item in trends_obj.get("momentum", []):
        flat.append({
            "label": f"{item['team']} Momentum",
            "value": item["trend"]
        })

    # League scoring trends
    league = trends_obj.get("league_scoring_trends", {})
    if league:
        flat.append({
            "label": "League Runs/Game",
            "value": league.get("runs_per_game")
        })
        flat.append({
            "label": "League HR/Game",
            "value": league.get("hr_per_game")
        })

    # Team streaks
    for item in trends_obj.get("team_streaks", []):
        flat.append({
            "label": f"{item['team']} Streak",
            "value": item["streak"]
        })

    return flat


# ---------------------------------------------------------
# DEMO DASHBOARD
# ---------------------------------------------------------

def build_demo_dashboard():
    """Return demo dashboard when no live games exist."""
    return {
        "mode": "demo",
        "games": DEMO_GAMES,
        "hitters": DEMO_HITTERS,
        "trends": flatten_trends(DEMO_TRENDS),
    }


# ---------------------------------------------------------
# LIVE GAME PARSING
# ---------------------------------------------------------

def build_live_game_object(event):
    """Convert a single ESPN event into dashboard game format."""
    try:
        comp = event["competitions"][0]
        home = comp["competitors"][0]
        away = comp["competitors"][1]

        return {
            "home_team": home["team"]["displayName"],
            "away_team": away["team"]["displayName"],
            "home_logo": home["team"].get("logo"),
            "away_logo": away["team"].get("logo"),

            "home_pitcher": home.get("probables", [{}])[0].get("athlete", {}).get("displayName", "TBD"),
            "away_pitcher": away.get("probables", [{}])[0].get("athlete", {}).get("displayName", "TBD"),

            "game_time": comp.get("date", "TBD"),

            # Placeholder hitters until real stats are wired
            "home_featured_hitter": {"name": "TBD"},
            "away_featured_hitter": {"name": "TBD"},

            # Placeholder colors
            "home_colors": {"primary": "#1e293b"},
            "away_colors": {"primary": "#1e293b"},
        }
    except Exception:
        return None


def build_live_dashboard_from_games(events):
    """Convert ESPN events into full dashboard format."""
    games = []
    for event in events:
        g = build_live_game_object(event)
        if g:
            games.append(g)

    return {
        "mode": "live",
        "games": games,
        "hitters": DEMO_HITTERS,          # still demo until real stats added
        "trends": flatten_trends(DEMO_TRENDS),  # flattened for frontend compatibility
    }


# ---------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------

async def build_live_dashboard():
    """Main function used by /dashboard endpoint."""
    events = await fetch_scoreboard()

    # No games → demo mode
    if not events:
        record_scrape_status("demo", 0)
        return build_demo_dashboard()

    # Live games found
    record_scrape_status("live", len(events))
    return build_live_dashboard_from_games(events)
