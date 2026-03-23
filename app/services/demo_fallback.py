def get_demo_dashboard():
    return {
        "status": "demo",

        # -------------------------
        # MATCHUPS
        # -------------------------
        "matchups": [
            {
                "game_id": "NYY-BOS-1",
                "home_team": "BOS",
                "away_team": "NYY",
                "home_record": "12–8",
                "away_record": "14–6",
                "game_time": "1:05 PM ET",

                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",

                "home_colors": {"primary": "#BD3039"},
                "away_colors": {"primary": "#132448"},

                "home_pitcher": "Chris Sale (3.78 ERA, 1.20 WHIP)",
                "away_pitcher": "Gerrit Cole (2.45 ERA, 0.98 WHIP)",

                "home_featured_hitter": {
                    "name": "Rafael Devers",
                    "avg": ".295",
                    "hr": 5
                },
                "away_featured_hitter": {
                    "name": "Aaron Judge",
                    "avg": ".310",
                    "hr": 6
                }
            },
            {
                "game_id": "CHC-MIL-1",
                "home_team": "MIL",
                "away_team": "CHC",
                "home_record": "9–11",
                "away_record": "10–10",
                "game_time": "2:10 PM ET",

                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",

                "home_colors": {"primary": "#12284B"},
                "away_colors": {"primary": "#0E3386"},

                "home_pitcher": "Corbin Burnes (2.45 ERA, 0.98 WHIP)",
                "away_pitcher": "Justin Steele (3.10 ERA, 1.12 WHIP)",

                "home_featured_hitter": {
                    "name": "Christian Yelich",
                    "avg": ".278",
                    "hr": 3
                },
                "away_featured_hitter": {
                    "name": "Ian Happ",
                    "avg": ".265",
                    "hr": 4
                }
            },
            {
                "game_id": "LAD-SF-1",
                "home_team": "SF",
                "away_team": "LAD",
                "home_record": "8–12",
                "away_record": "14–6",
                "game_time": "4:05 PM ET",

                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",

                "home_colors": {"primary": "#FD5A1E"},
                "away_colors": {"primary": "#005A9C"},

                "home_pitcher": "Logan Webb (3.20 ERA, 1.10 WHIP)",
                "away_pitcher": "Clayton Kershaw (2.95 ERA, 1.05 WHIP)",

                "home_featured_hitter": {
                    "name": "Brandon Crawford",
                    "avg": ".250",
                    "hr": 4
                },
                "away_featured_hitter": {
                    "name": "Mookie Betts",
                    "avg": ".320",
                    "hr": 7
                }
            }
        ],

        # -------------------------
        # PITCHERS
        # -------------------------
        "pitchers": [
            {
                "name": "Corbin Burnes",
                "team": "MIL",
                "era": 2.45,
                "whip": 0.98,
                "kbb": 5.2,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
                "colors": {"primary": "#12284B"}
            },
            {
                "name": "Chris Sale",
                "team": "BOS",
                "era": 3.78,
                "whip": 1.20,
                "kbb": 4.1,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "colors": {"primary": "#BD3039"}
            },
            {
                "name": "Gerrit Cole",
                "team": "NYY",
                "era": 2.45,
                "whip": 0.98,
                "kbb": 6.0,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "colors": {"primary": "#132448"}
            }
        ],

        # -------------------------
        # HITTERS
        # -------------------------
        "hitters": [
            {
                "name": "Aaron Judge",
                "team": "NYY",
                "score": 94,
                "bvp_hrs": 2,
                "bvp_hr_points": 4,
                "bvp_avg": .310,
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
                "bvp_avg": .320,
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
                "bvp_avg": .295,
                "bvp_avg_points": 3,
                "hit_streak": 5,
                "hit_streak_points": 5,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "colors": {"primary": "#BD3039"}
            }
        ],

        # -------------------------
        # STADIUM FACTORS
        # -------------------------
        "stadium_factors": [
            {"team": "COL", "name": "Coors Field", "park_factor": 1.28, "hr_factor": 1.35},
            {"team": "NYY", "name": "Yankee Stadium", "park_factor": 1.12, "hr_factor": 1.25},
            {"team": "BOS", "name": "Fenway Park", "park_factor": 1.10, "hr_factor": 0.95},
            {"team": "CIN", "name": "Great American Ball Park", "park_factor": 1.09, "hr_factor": 1.18},
            {"team": "LAD", "name": "Dodger Stadium", "park_factor": 0.98, "hr_factor": 0.92},
            {"team": "SEA", "name": "T-Mobile Park", "park_factor": 0.95, "hr_factor": 0.88},
            {"team": "SD", "name": "Petco Park", "park_factor": 0.93, "hr_factor": 0.85}
        ],

        # -------------------------
        # MOMENTUM
        # -------------------------
        "momentum": [
            {"team": "NYY", "last10": "7–3", "momentum": 0.72},
            {"team": "LAD", "last10": "8–2", "momentum": 0.80},
            {"team": "BOS", "last10": "5–5", "momentum": 0.50}
        ],

        # -------------------------
        # WEATHER FACTORS
        # -------------------------
        "weather_factors": [
            {"condition": "Wind Out to LF", "run_factor": 1.12, "hr_factor": 1.18},
            {"condition": "Humid Air", "run_factor": 1.05, "hr_factor": 1.02}
        ],

        # -------------------------
        # LEAGUE SCORING TRENDS
        # -------------------------
        "league_scoring_trends": {
            "avg_runs_per_game": 9.1,
            "avg_hr_per_game": 2.1,
            "run_trend_7d": "+4%",
            "hr_trend_7d": "+3%",
            "run_trend_30d": "+2%",
            "hr_trend_30d": "+1%"
        },

        # -------------------------
        # TEAM STREAKS
        # -------------------------
        "team_streaks": [
            {"team": "LAD", "streak": "W5", "type": "hot"},
            {"team": "NYY", "streak": "W4", "type": "hot"},
            {"team": "SF", "streak": "L4", "type": "cold"}
        ]
    }
