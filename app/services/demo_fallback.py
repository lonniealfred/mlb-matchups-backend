# app/services/demo_fallback.py

def get_demo_dashboard():
    return {
        "matchups": [
            {
                "game_id": "NYY-BOS",
                "home_team": "Yankees",
                "away_team": "Red Sox",
                "home_score": 4.2,
                "away_score": 3.8,
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",

                "home_top_hitters": [
                    {"name": "Aaron Judge", "avg": ".310", "hr": 6, "score": 94}
                ],
                "away_top_hitters": [
                    {"name": "Rafael Devers", "avg": ".295", "hr": 5, "score": 89}
                ],
            },
            {
                "game_id": "CHC-MIL",
                "home_team": "Cubs",
                "away_team": "Brewers",
                "home_score": 4.0,
                "away_score": 4.4,
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",

                "home_top_hitters": [
                    {"name": "Seiya Suzuki", "avg": ".285", "hr": 4, "score": 82}
                ],
                "away_top_hitters": [
                    {"name": "Christian Yelich", "avg": ".300", "hr": 3, "score": 80}
                ],
            },
            {
                "game_id": "LAD-SF",
                "home_team": "Dodgers",
                "away_team": "Giants",
                "home_score": 5.1,
                "away_score": 3.9,
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",

                "home_top_hitters": [
                    {"name": "Mookie Betts", "avg": ".320", "hr": 3, "score": 92}
                ],
                "away_top_hitters": [
                    {"name": "Mike Yastrzemski", "avg": ".270", "hr": 4, "score": 78}
                ],
            }
        ],

        # Hitters leaderboard (Hitters tab)
        "hitters": [
            {
                "name": "Aaron Judge",
                "team": "NYY",
                "score": 94,
                "bvp_hrs": 2,
                "bvp_hr_points": 4,
                "bvp_avg": 0.310,
                "bvp_avg_points": 3,
                "hit_streak": 7,
                "hit_streak_points": 7,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "colors": {"primary": "#132448"}
            },
            {
                "name": "Mookie Betts",
                "team": "LAD",
                "score": 92,
                "bvp_hrs": 3,
                "bvp_hr_points": 6,
                "bvp_avg": 0.320,
                "bvp_avg_points": 3,
                "hit_streak": 6,
                "hit_streak_points": 6,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
                "colors": {"primary": "#005A9C"}
            },
            {
                "name": "Rafael Devers",
                "team": "BOS",
                "score": 89,
                "bvp_hrs": 1,
                "bvp_hr_points": 2,
                "bvp_avg": 0.295,
                "bvp_avg_points": 3,
                "hit_streak": 5,
                "hit_streak_points": 5,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "colors": {"primary": "#BD3039"}
            }
        ],

        # Top hitters for Trends tab
        "top_hitters": [
            {"name": "Aaron Judge", "team": "NYY", "score": 94},
            {"name": "Mookie Betts", "team": "LAD", "score": 92},
            {"name": "Rafael Devers", "team": "BOS", "score": 89}
        ],

        # Other sections (safe empty placeholders)
        "pitchers": [],
        "stadium_factors": [],
        "momentum": [],
        "weather_factors": [],
        "league_scoring_trends": [],
        "team_streaks": []
    }
