# ADVANCED MATCHUP BUILDER
# Works with the corrected scraper.py and produces stable, frontend-ready matchup objects.

def compute_pitcher_vulnerability(pitcher):
    era = pitcher.get("era", 4.00)
    recent_er = pitcher.get("recent_er", 2)

    # Lower ERA = better pitcher = lower vulnerability
    era_component = max(0, (era - 3.00) * 10)

    # Recent earned runs increase vulnerability
    recent_component = recent_er * 5

    # Final vulnerability score
    return min(100, era_component + recent_component)


def compute_hitter_score(h):
    hr = h.get("hr_vs_pitcher", 0)
    avg = h.get("avg_vs_pitcher", 0.0)
    streak = h.get("streak", 0)
    pa = h.get("pa_vs_pitcher", 0)

    # Weighted hitter score
    return (
        hr * 12 +
        avg * 100 +
        streak * 3 +
        pa * 0.5
    )


def compute_team_score(top_hitters, opposing_pitcher, stadium):
    pitcher_vuln = compute_pitcher_vulnerability(opposing_pitcher)
    stadium_factor = stadium.get("hr_factor", 100)

    hitter_total = sum(h.get("hitter_score", 0) for h in top_hitters)

    # Weighted team score
    return (
        hitter_total * 0.6 +
        pitcher_vuln * 0.3 +
        stadium_factor * 0.1
    )


def compute_game_score(away_score, home_score):
    # Final matchup score
    return round((away_score + home_score) / 2, 2)


def build_matchup_objects(games):
    matchups = []

    for g in games:
        away_pitcher = g["pitchers"]["away_pitcher"]
        home_pitcher = g["pitchers"]["home_pitcher"]

        away_hitters = g["hitters"]["away_top_hitters"]
        home_hitters = g["hitters"]["home_top_hitters"]

        stadium = g["stadium"]

        # Compute hitter scores
        for h in away_hitters:
            h["hitter_score"] = compute_hitter_score(h)

        for h in home_hitters:
            h["hitter_score"] = compute_hitter_score(h)

        # Compute team scores
        away_team_score = compute_team_score(away_hitters, home_pitcher, stadium)
        home_team_score = compute_team_score(home_hitters, away_pitcher, stadium)

        # Compute final game score
        game_score = compute_game_score(away_team_score, home_team_score)

        matchups.append({
            "game_id": g["game_id"],
            "start_time": g["start_time"],
            "away_team": g["away_team"],
            "home_team": g["home_team"],
            "pitchers": g["pitchers"],
            "hitters": g["hitters"],
            "stadium": stadium,
            "team_scores": {
                "away_team_score": round(away_team_score, 2),
                "home_team_score": round(home_team_score, 2)
            },
            "game_score": game_score
        })

    return matchups
