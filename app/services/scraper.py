import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests

# ESPN endpoints
ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
ESPN_TEAM = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/{team_id}"
ESPN_VENUE = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/venues/{venue_id}"
ESPN_PLAYER_STATS = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/athletes/{player_id}/statistics"
ESPN_BVP = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/athletes/{batter_id}/versus/{pitcher_id}"

# -------------------------------------------------------------------
# Simple in-memory cache with thread safety
# -------------------------------------------------------------------

_cache = {}
_cache_lock = threading.Lock()


def cached_get_json(url, timeout=5):
    with _cache_lock:
        if url in _cache:
            return _cache[url]

    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        data = {}

    with _cache_lock:
        _cache[url] = data

    return data


def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default


# -------------------------------------------------------------------
# Fallback generators
# -------------------------------------------------------------------

def ensure_lineup(lineup, team_abbr):
    if lineup and len(lineup) > 0:
        return lineup

    return [
        {"id": f"{team_abbr}_P{i}", "name": f"{team_abbr} Player {i}"}
        for i in range(1, 10)
    ]


def fallback_pitcher(team_abbr):
    return {
        "id": f"{team_abbr}_PITCHER",
        "name": f"{team_abbr} Pitcher",
        "era": 4.00,
        "recent_er": 2,
        "vulnerability_score": 50.0,
    }


def fallback_stadium():
    return {
        "name": "Unknown Stadium",
        "hr_factor": 100,
    }


# -------------------------------------------------------------------
# ESPN data fetchers (single-resource)
# -------------------------------------------------------------------

def get_today_games():
    data = cached_get_json(ESPN_SCOREBOARD)
    events = safe_get(data, "events", [])

    games = []
    for ev in events:
        competitions = safe_get(ev, "competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = safe_get(comp, "competitors", [])
        if len(competitors) != 2:
            continue

        away = competitors[0]
        home = competitors[1]

        games.append(
            {
                "game_id": ev.get("id"),
                "start_time": ev.get("date"),
                "away_team": away["team"]["abbreviation"],
                "home_team": home["team"]["abbreviation"],
                "away_team_id": away["team"]["id"],
                "home_team_id": home["team"]["id"],
                "venue_id": safe_get(comp, "venue", {}).get("id"),
            }
        )

    return games


def get_lineup(team_id):
    url = ESPN_TEAM.format(team_id=team_id)
    data = cached_get_json(url)
    roster = safe_get(data, "athletes", [])

    lineup = []
    for player in roster[:9]:
        lineup.append(
            {
                "id": player.get("id"),
                "name": player.get("displayName"),
            }
        )

    return lineup


def get_pitcher_stats(player_id):
    url = ESPN_PLAYER_STATS.format(player_id=player_id)
    data = cached_get_json(url)
    splits = safe_get(data, "splits", [])

    if not splits:
        return {"era": 4.00, "recent_er": 2, "vulnerability_score": 50.0}

    # You can refine this later using real splits
    return {
        "era": 3.85,
        "recent_er": 2,
        "vulnerability_score": 55.0,
    }


def get_bvp_stats(batter_id, pitcher_id):
    url = ESPN_BVP.format(batter_id=batter_id, pitcher_id=pitcher_id)
    data = cached_get_json(url)
    return {
        "hr": safe_get(data, "homeRuns", 0),
        "avg": safe_get(data, "battingAverage", 0.0),
        "pa": safe_get(data, "plateAppearances", 0),
    }


def get_hit_streak(player_id):
    # Placeholder – can be wired to real streak data later
    return 3


def get_stadium_info(venue_id):
    if not venue_id:
        return fallback_stadium()

    url = ESPN_VENUE.format(venue_id=venue_id)
    data = cached_get_json(url)
    return {
        "name": safe_get(data, "fullName", "Unknown Stadium"),
        "hr_factor": safe_get(data, "homeRunFactor", 100),
    }


# -------------------------------------------------------------------
# Hitters logic
# -------------------------------------------------------------------

def build_hitter_with_stats(hitter, opposing_pitcher_id):
    batter_id = hitter["id"]
    bvp = get_bvp_stats(batter_id, opposing_pitcher_id)
    streak = get_hit_streak(batter_id)

    return {
        "name": hitter["name"],
        "hr_vs_pitcher": bvp["hr"],
        "avg_vs_pitcher": bvp["avg"],
        "pa_vs_pitcher": bvp["pa"],
        "streak": streak,
        # hitter_score will be computed in matchups.py
        "hitter_score": 0,
    }


def get_top_hitters(lineup, opposing_pitcher):
    pitcher_id = opposing_pitcher.get("id")
    if not pitcher_id:
        # If no real pitcher id, just return basic hitters
        return [
            {
                "name": h["name"],
                "hr_vs_pitcher": 0,
                "avg_vs_pitcher": 0.0,
                "pa_vs_pitcher": 0,
                "streak": 0,
                "hitter_score": 0,
            }
            for h in lineup[:4]
        ]

    # Parallelize BvP + streak fetches per hitter
    hitters_with_stats = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(build_hitter_with_stats, h, pitcher_id): h
            for h in lineup
        }
        for fut in as_completed(futures):
            try:
                hitters_with_stats.append(fut.result())
            except Exception:
                # Fallback for any failed hitter
                h = futures[fut]
                hitters_with_stats.append(
                    {
                        "name": h["name"],
                        "hr_vs_pitcher": 0,
                        "avg_vs_pitcher": 0.0,
                        "pa_vs_pitcher": 0,
                        "streak": 0,
                        "hitter_score": 0,
                    }
                )

    # matchups.py will compute final hitter_score; here we just sort by rough proxy
    hitters_with_stats.sort(
        key=lambda x: (x["hr_vs_pitcher"], x["avg_vs_pitcher"], x["streak"]),
        reverse=True,
    )
    return hitters_with_stats[:4]


# -------------------------------------------------------------------
# Main scraper assembly (parallelized per game)
# -------------------------------------------------------------------

def _build_single_game(game):
    # Lineups (with fallback)
    away_lineup = ensure_lineup(get_lineup(game["away_team_id"]), game["away_team"])
    home_lineup = ensure_lineup(get_lineup(game["home_team_id"]), game["home_team"])

    # Pitchers (with fallback)
    try:
        away_pitcher = {
            "id": away_lineup[0]["id"],
            "name": away_lineup[0]["name"],
            **get_pitcher_stats(away_lineup[0]["id"]),
        }
    except Exception:
        away_pitcher = fallback_pitcher(game["away_team"])

    try:
        home_pitcher = {
            "id": home_lineup[0]["id"],
            "name": home_lineup[0]["name"],
            **get_pitcher_stats(home_lineup[0]["id"]),
        }
    except Exception:
        home_pitcher = fallback_pitcher(game["home_team"])

    # Stadium
    stadium = get_stadium_info(game["venue_id"])

    # Hitters (parallelized inside get_top_hitters)
    away_top_hitters = get_top_hitters(away_lineup, home_pitcher)
    home_top_hitters = get_top_hitters(home_lineup, away_pitcher)

    return {
        **game,
        "pitchers": {
            "away_pitcher": away_pitcher,
            "home_pitcher": home_pitcher,
        },
        "hitters": {
            "away_top_hitters": away_top_hitters,
            "home_top_hitters": home_top_hitters,
        },
        "stadium": stadium,
    }


def scrape_full_game_data():
    games = get_today_games()
    if not games:
        return []

    full_games = []

    # Parallelize per-game assembly
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_build_single_game, g) for g in games]
        for fut in as_completed(futures):
            try:
                full_games.append(fut.result())
            except Exception:
                # Skip any completely failed game
                continue

    # Sort by start time for consistency
    full_games.sort(key=lambda g: g.get("start_time", ""))

    return full_games
