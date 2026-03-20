# app/services/matchups.py

from typing import Dict, List, Any

def safe_get(obj: Dict, path: List[str], default=None):
    """Safely walk nested dicts."""
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return default
        obj = obj[key]
    return obj


def extract_pitcher(team: Dict) -> Dict:
    """Extract pitcher info with safe defaults."""
    return {
        "name": safe_get(team, ["probables", 0, "athlete", "displayName"], "TBD"),
        "team": safe_get(team, ["team", "abbreviation"], "UNK"),
        "era": safe_get(team, ["probables", 0, "statistics", 0, "era"], 0.00),
        "whip": safe_get(team, ["probables", 0, "statistics", 0, "whip"], 0.00),
        "photo_url": safe_get(team, ["probables", 0, "athlete", "headshot"], None),
    }


def extract_hitter(athlete: Dict, opponent_pitcher: str) -> Dict:
    """Extract hitter info with safe defaults."""
    return {
        "name": athlete.get("displayName", "Unknown Player"),
        "team": athlete.get("team", {}).get("abbreviation", "UNK"),
        "avg": athlete.get("statistics", {}).get("avg", 0.0),
        "hr": athlete.get("statistics", {}).get("hr", 0),
        "rbi": athlete.get("statistics", {}).get("rbi", 0),
        "streak": athlete.get("statistics", {}).get("streak", 0),
        "opponent_pitcher": opponent_pitcher,
        "photo_url": athlete.get("headshot"),
        "score": {},  # filled in later by scoring.py
    }


def extract_matchups(scoreboard: Dict) -> List[Dict]:
    """Extract matchups from ESPN scoreboard JSON."""
    events = scoreboard.get("events", [])
    matchups = []

    for game in events:
        competitions = game.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])

        if len(competitors) != 2:
            continue

        home = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
        away = competitors[1] if home is competitors[0] else competitors[0]

        home_pitcher = extract_pitcher(home)
        away_pitcher = extract_pitcher(away)

        # Extract top hitters (if ESPN provides them)
        raw_hitters = comp.get("notes", [])  # ESPN sometimes puts hitters here
        top_hitters = []

        for h in raw_hitters:
            athlete = h.get("athlete")
            if not athlete:
                continue
            top_hitters.append(
                extract_hitter(athlete, opponent_pitcher=away_pitcher["name"])
            )

        matchups.append({
            "home_team": home.get("team", {}).get("abbreviation", "UNK"),
            "away_team": away.get("team", {}).get("abbreviation", "UNK"),
            "home_pitcher": home_pitcher,
            "away_pitcher": away_pitcher,
            "top_hitters": top_hitters,
        })

    return matchups
