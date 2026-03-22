# app/services/espn_scraper.py

from typing import Any, Dict, List, Optional, Tuple
import httpx

from app.services.team_data import TEAM_LOGOS, TEAM_COLORS


ESPN_SCOREBOARD_URL = (
    "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/scoreboard"
)
ESPN_SUMMARY_URL = (
    "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/summary"
)


async def fetch_espn_scoreboard() -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(ESPN_SCOREBOARD_URL)
        resp.raise_for_status()
        return resp.json()


async def fetch_espn_summary(event_id: str) -> Optional[Dict[str, Any]]:
    params = {"event": event_id}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(ESPN_SUMMARY_URL, params=params)
        if resp.status_code != 200:
            return None
        return resp.json()


def _safe_get_pitcher_stats_from_stats_list(
    stats: List[Dict[str, Any]]
) -> Dict[str, float]:
    out: Dict[str, float] = {
        "era": 0.0,
        "whip": 0.0,
        "k9": 0.0,
        "bb9": 0.0,
        "opp_avg": 0.0,
    }
    for s in stats:
        name = s.get("name")
        try:
            val = float(s.get("value") or 0)
        except (TypeError, ValueError):
            val = 0.0

        if name == "earnedRunAverage":
            out["era"] = val
        elif name == "walksAndHitsPerInningPitched":
            out["whip"] = val
        elif name == "strikeoutsPerNineInnings":
            out["k9"] = val
        elif name == "walksPerNineInnings":
            out["bb9"] = val
        elif name == "opponentBattingAverage":
            out["opp_avg"] = val

    return out


def _safe_get_probable_pitcher(team: Dict[str, Any]) -> Dict[str, Any]:
    pitcher: Dict[str, Any] = {
        "name": "TBD",
        "team": team.get("abbreviation") or team.get("shortDisplayName") or "",
        "era": 0.0,
        "whip": 0.0,
        "k9": 0.0,
        "bb9": 0.0,
        "opp_avg": 0.0,
        "photo_url": None,
    }

    probables = team.get("probables") or []
    if probables:
        p = probables[0]
        athlete = p.get("athlete") or {}
        pitcher["name"] = athlete.get("displayName", "TBD")
        stats = p.get("statistics") or []
        stats_flat: List[Dict[str, Any]] = []
        for group in stats:
            stats_flat.extend(group.get("stats") or [])
        enriched = _safe_get_pitcher_stats_from_stats_list(stats_flat)
        pitcher.update(enriched)
        pitcher["photo_url"] = (athlete.get("headshot") or {}).get("href")
        return pitcher

    leaders = team.get("leaders") or []
    for group in leaders:
        if group.get("name") == "pitchingLeaders":
            leaders_athletes = group.get("leaders") or []
            if leaders_athletes:
                a = leaders_athletes[0].get("athlete") or {}
                pitcher["name"] = a.get("displayName", "TBD")
                pitcher["photo_url"] = (a.get("headshot") or {}).get("href")
                break

    return pitcher


def _extract_top_hitters_from_summary(
    summary: Dict[str, Any], home_abbr: str, away_abbr: str
) -> List[Dict[str, Any]]:
    boxscore = summary.get("boxscore") or {}
    players_groups = boxscore.get("players") or []
    hitters: List[Dict[str, Any]] = []

    for team_group in players_groups:
        team = team_group.get("team") or {}
        team_abbr = team.get("abbreviation") or team.get("shortDisplayName") or ""
        athletes = team_group.get("statistics") or []

        for stat_group in athletes:
            if stat_group.get("name") != "batting":
                continue
            stats_entries = stat_group.get("athletes") or []
            for entry in stats_entries:
                athlete = entry.get("athlete") or {}
                stat_list = entry.get("stats") or []
                stat_map: Dict[str, Any] = {}
                for s in stat_list:
                    stat_map[s.get("name")] = s.get("value")

                try:
                    avg = float(stat_map.get("battingAverage") or 0)
                except (TypeError, ValueError):
                    avg = 0.0
                try:
                    obp = float(stat_map.get("onBasePercentage") or 0)
                except (TypeError, ValueError):
                    obp = 0.0
                try:
                    slg = float(stat_map.get("sluggingPercentage") or 0)
                except (TypeError, ValueError):
                    slg = 0.0
                try:
                    hr = int(stat_map.get("homeRuns") or 0)
                except (TypeError, ValueError):
                    hr = 0
                try:
                    rbi = int(stat_map.get("runsBattedIn") or 0)
                except (TypeError, ValueError):
                    rbi = 0

                hitters.append(
                    {
                        "name": athlete.get("displayName", ""),
                        "team": team_abbr,
                        "avg": avg,
                        "obp": obp,
                        "slg": slg,
                        "hr": hr,
                        "rbi": rbi,
                        "photo_url": (athlete.get("headshot") or {}).get("href"),
                    }
                )

    hitters.sort(key=lambda h: (h["hr"], h["rbi"], h["slg"]), reverse=True)
    return hitters[:4]


def _build_matchup_from_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    competitions = event.get("competitions") or []
    if not competitions:
        return None

    comp = competitions[0]
    competitors = comp.get("competitors") or []
    if len(competitors) != 2:
        return None

    home = next((c for c in competitors if c.get("homeAway") == "home"), None)
    away = next((c for c in competitors if c.get("homeAway") == "away"), None)
    if not home or not away:
        return None

    home_team = home.get("team") or {}
    away_team = away.get("team") or {}

    home_abbr = home_team.get("abbreviation") or home_team.get("shortDisplayName")
    away_abbr = away_team.get("abbreviation") or away_team.get("shortDisplayName")

    matchup: Dict[str, Any] = {
        "event_id": event.get("id"),
        "home_team": home_abbr,
        "away_team": away_abbr,
        "home_pitcher": _safe_get_probable_pitcher(home_team),
        "away_pitcher": _safe_get_probable_pitcher(away_team),
        "top_hitters": [],
        "home_logo": TEAM_LOGOS.get(home_abbr),
        "away_logo": TEAM_LOGOS.get(away_abbr),
        "home_colors": TEAM_COLORS.get(home_abbr),
        "away_colors": TEAM_COLORS.get(away_abbr),
    }

    return matchup


async def build_matchups() -> List[Dict[str, Any]]:
    data = await fetch_espn_scoreboard()
    events = data.get("events") or []

    matchups: List[Dict[str, Any]] = []
    for event in events:
        m = _build_matchup_from_event(event)
        if not m:
            continue

        event_id = m.get("event_id")
        if event_id:
            try:
                summary = await fetch_espn_summary(event_id)
                if summary:
                    hitters = _extract_top_hitters_from_summary(
                        summary, m["home_team"], m["away_team"]
                    )
                    m["top_hitters"] = hitters
            except Exception:
                m["top_hitters"] = []

        matchups.append(m)

    return matchups


async def build_dashboard() -> Dict[str, Any]:
    matchups = await build_matchups()

    pitchers: List[Dict[str, Any]] = []
    hitters: List[Dict[str, Any]] = []
    seen_pitchers: set[Tuple[str, str]] = set()
    seen_hitters: set[Tuple[str, str]] = set()

    for m in matchups:
        for side in ("home_pitcher", "away_pitcher"):
            p = m.get(side) or {}
            key = (p.get("name"), p.get("team"))
            if key not in seen_pitchers and p.get("name"):
                seen_pitchers.add(key)
                pitchers.append(p)

        for h in m.get("top_hitters") or []:
            key_h = (h.get("name"), h.get("team"))
            if key_h not in seen_hitters and h.get("name"):
                seen_hitters.add(key_h)
                hitters.append(h)

    dashboard = {
        "matchups": matchups,
        "hitters": hitters,
        "pitchers": pitchers,
    }

    return dashboard
