# app/services/espn_scraper.py

import httpx
from typing import Any, Dict, List, Optional


ESPN_SCOREBOARD_URL = (
    "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/scoreboard"
)


async def fetch_espn_scoreboard() -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(ESPN_SCOREBOARD_URL)
        resp.raise_for_status()
        return resp.json()


def _safe_get_probable_pitcher(team: Dict[str, Any]) -> Dict[str, Any]:
    """
    ESPN sometimes includes probable pitchers under 'probables' or 'leaders'.
    This is defensive: if we can't find it, we return a TBD pitcher.
    """
    # Default TBD pitcher
    pitcher = {
        "name": "TBD",
        "team": team.get("abbreviation") or team.get("shortDisplayName") or "",
        "era": 0,
        "whip": 0,
        "photo_url": None,
    }

    # Try probables
    probables = team.get("probables") or []
    if probables:
        p = probables[0]
        pitcher["name"] = p.get("athlete", {}).get("displayName", "TBD")
        stats = p.get("statistics") or []
        for s in stats:
            if s.get("name") == "earnedRunAverage":
                pitcher["era"] = float(s.get("value") or 0)
            if s.get("name") == "walksAndHitsPerInningPitched":
                pitcher["whip"] = float(s.get("value") or 0)
        pitcher["photo_url"] = (
            p.get("athlete", {}).get("headshot", {}).get("href") or None
        )
        return pitcher

    # Try leaders (sometimes used for pitchers)
    leaders = team.get("leaders") or []
    for group in leaders:
        if group.get("name") == "pitchingLeaders":
            leaders_athletes = group.get("leaders") or []
            if leaders_athletes:
                a = leaders_athletes[0].get("athlete", {})
                pitcher["name"] = a.get("displayName", "TBD")
                pitcher["photo_url"] = a.get("headshot", {}).get("href") or None
                break

    return pitcher


def _build_matchup_from_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    competitions = event.get("competitions") or []
    if not competitions:
        return None

    comp = competitions[0]
    competitors = comp.get("competitors") or []
    if len(competitors) != 2:
        return None

    # ESPN uses home/away flags
    home = next((c for c in competitors if c.get("homeAway") == "home"), None)
    away = next((c for c in competitors if c.get("homeAway") == "away"), None)
    if not home or not away:
        return None

    home_team = home.get("team", {})
    away_team = away.get("team", {})

    home_abbr = home_team.get("abbreviation") or home_team.get("shortDisplayName")
    away_abbr = away_team.get("abbreviation") or away_team.get("shortDisplayName")

    matchup = {
        "home_team": home_abbr,
        "away_team": away_abbr,
        "home_pitcher": _safe_get_probable_pitcher(home_team),
        "away_pitcher": _safe_get_probable_pitcher(away_team),
        "top_hitters": [],  # you can fill this later from boxscore/leaders
    }

    return matchup


async def build_matchups() -> List[Dict[str, Any]]:
    """
    Core function your router is already calling.

    Returns:
        List of matchup dicts with:
        - home_team
        - away_team
        - home_pitcher
        - away_pitcher
        - top_hitters (currently empty)
    """
    data = await fetch_espn_scoreboard()
    events = data.get("events") or []

    matchups: List[Dict[str, Any]] = []
    for event in events:
        m = _build_matchup_from_event(event)
        if m:
            matchups.append(m)

    return matchups


async def build_dashboard() -> Dict[str, Any]:
    """
    Higher-level builder if you want a full dashboard object.

    Matches the JSON shape you're already returning:
    {
      "matchups": [...],
      "hitters": [],
      "pitchers": [...]
    }
    """
    matchups = await build_matchups()

    # For now, pitchers list is just unique pitchers from matchups
    pitchers: List[Dict[str, Any]] = []
    seen = set()

    for m in matchups:
        for side in ("home_pitcher", "away_pitcher"):
            p = m.get(side) or {}
            key = (p.get("name"), p.get("team"))
            if key not in seen and p.get("name"):
                seen.add(key)
                pitchers.append(p)

    dashboard = {
        "matchups": matchups,
        "hitters": [],   # you can fill this later from boxscore/leaders
        "pitchers": pitchers,
    }

    return dashboard
