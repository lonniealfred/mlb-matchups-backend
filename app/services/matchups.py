from scoring import score_hitter


def build_matchup_objects(games):
    """
    Builds full matchup objects including:
    - pitcher data
    - hitter scoring (with ballpark factor)
    - stadium HR factor
    """

    matchups = []

    for g in games:
        stadium_hr_factor = g.get("stadium_hr_factor", 100)

        home_pitcher = g["pitchers"]["home_pitcher"]["name"]
        away_pitcher = g["pitchers"]["away_pitcher"]["name"]

        home_hitters_scored = []
        away_hitters_scored = []

        # -----------------------------
        # Score AWAY hitters
        # -----------------------------
        for h in g["hitters"]["away_top_hitters"]:
            scored = score_hitter(
                hitter=h,
                pitcher_name=home_pitcher,
                stadium_hr_factor=stadium_hr_factor
            )
            away_hitters_scored.append(scored)

        # -----------------------------
        # Score HOME hitters
        # -----------------------------
        for h in g["hitters"]["home_top_hitters"]:
            scored = score_hitter(
                hitter=h,
                pitcher_name=away_pitcher,
                stadium_hr_factor=stadium_hr_factor
            )
            home_hitters_scored.append(scored)

        # -----------------------------
        # Build final matchup object
        # -----------------------------
        matchup = {
            "game_id": g["game_id"],
            "start_time": g["start_time"],
            "home_team": g["home_team"],
            "away_team": g["away_team"],
            "stadium_hr_factor": stadium_hr_factor,
            "pitchers": g["pitchers"],
            "hitters": {
                "home_top_hitters": home_hitters_scored,
                "away_top_hitters": away_hitters_scored,
            },
        }

        matchups.append(matchup)

    return matchups
