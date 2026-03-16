from app.services.scoring import score_hitter, score_pitcher

# Demo fallback values (used when ESPN data is missing)
DEMO_MATCHUP = {
    "game_id": "demo-1",
    "start_time": "2026-04-12T13:05:00Z",
    "home_team": "NYY",
    "away_team": "BOS",
    "pitchers": {
        "home_pitcher": {
            "name": "Demo Home Pitcher",
            "era": 3.25,
            "whip": 1.12,
            "hand": "R"
        },
        "away_pitcher": {
            "name": "Demo Away Pitcher",
            "era": 3.75,
            "whip": 1.20,
            "hand": "L"
        }
    },
    "top_hitters": {
        "home_top_hitters": [],
        "away_top_hitters": []
    }
}


def build_matchups(games):
    matchups = []

    for g in games:
        try:
            home = g["home_team"]
            away = g["away_team"]
            pitchers = g.get("pitchers", {})
            hitters = g.get("hitters", [])
        except:
            matchups.append(DEMO_MATCHUP)
            continue

        # Extract pitchers safely
        home_pitcher = pitchers.get("home_pitcher")
        away_pitcher = pitchers.get("away_pitcher")

        # Fallback if missing
        if home_pitcher is None or away_pitcher is None:
            home_pitcher = DEMO_MATCHUP["pitchers"]["home_pitcher"]
            away_pitcher = DEMO_MATCHUP["pitchers"]["away_pitcher"]

        # Score pitchers
        scored_home_pitcher = score_pitcher(home_pitcher)
        scored_away_pitcher = score_pitcher(away_pitcher)

        # Split hitters by team
        home_hitters = [h for h in hitters if h.get("team") == home]
        away_hitters = [h for h in hitters if h.get("team") == away]

        # Fallback hitters if empty
        if not home_hitters:
            home_hitters = [
                {"name": "Demo Hitter 1", "team": home, "avg": .300, "hr": 5, "rbi": 12}
            ]
        if not away_hitters:
            away_hitters = [
                {"name": "Demo Hitter 2", "team": away, "avg": .280, "hr": 4, "rbi": 10}
            ]

        # Score hitters
        scored_home_hitters = [score_hitter(h, away_pitcher) for h in home_hitters]
        scored_away_hitters = [score_hitter(h, home_pitcher) for h in away_hitters]

        # Sort and take top 5
        top_home = sorted(scored_home_hitters, key=lambda x: x["hitter_score"], reverse=True)[:5]
        top_away = sorted(scored_away_hitters, key=lambda x: x["hitter_score"], reverse=True)[:5]

        matchups.append({
            "game_id": g.get("game_id", "demo"),
            "start_time": g.get("start_time", DEMO_MATCHUP["start_time"]),
            "home_team": home,
            "away_team": away,
            "pitchers": {
                "home_pitcher": scored_home_pitcher,
                "away_pitcher": scored_away_pitcher
            },
            "top_hitters": {
                "home_top_hitters": top_home,
                "away_top_hitters": top_away
            }
        })

    return matchups
