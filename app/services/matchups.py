from app.services.scoring import score_hitter

def build_matchups(games):
    matchups = []

    for g in games:
        home = g["home_team"]
        away = g["away_team"]
        pitchers = g["pitchers"]
        hitters = g["hitters"]

        home_pitcher = pitchers["home_pitcher"]
        away_pitcher = pitchers["away_pitcher"]

        home_hitters = [h for h in hitters if h["team"] == home]
        away_hitters = [h for h in hitters if h["team"] == away]

        scored_home = [score_hitter(h, away_pitcher) for h in home_hitters]
        scored_away = [score_hitter(h, home_pitcher) for h in away_hitters]

        matchups.append({
            "game_id": g["game_id"],
            "start_time": g["start_time"],
            "home_team": home,
            "away_team": away,
            "pitchers": pitchers,
            "top_hitters": {
                "home_top_hitters": sorted(scored_home, key=lambda x: x["hitter_score"], reverse=True)[:5],
                "away_top_hitters": sorted(scored_away, key=lambda x: x["hitter_score"], reverse=True)[:5],
            }
        })

    return matchups
