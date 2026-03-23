# app/services/demo_fallback.py

def get_demo_dashboard():
    return {
        "matchups": [
            {
                "game_id": "NYY-BOS",
                "home_team": "Yankees",
                "away_team": "Red Sox",
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",

                "home_featured_hitter": {
                    "name": "Aaron Judge",
                    "avg": ".310",
                    "hr": 6
                },
                "away_featured_hitter": {
                    "name": "Rafael Devers",
                    "avg": ".295",
                    "hr": 5
                },

                "home_pitcher": "Gerrit Cole",
                "away_pitcher": "Chris Sale",
                "game_time": "1:05 PM ET",

                "home_colors": {"primary": "#132448"},
                "away_colors": {"primary": "#BD3039"}
            },
            {
                "game_id": "CHC-MIL",
                "home_team": "Cubs",
                "away_team": "Brewers",
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",

                "home_featured_hitter": {
                    "name": "Seiya Suzuki",
                    "avg": ".285",
                    "hr": 4
                },
                "away_featured_hitter": {
                    "name": "Christian Yelich",
                    "avg": ".300",
                    "hr": 3
                },

                "home_pitcher": "Justin Steele",
                "away_pitcher": "Corbin Burnes",
                "game_time": "2:10 PM ET",

                "home_colors": {"primary": "#0E3386"},
                "away_colors": {"primary": "#12284B"}
            },
            {
                "game_id": "LAD-SF",
                "home_team": "Dodgers",
                "away_team": "Giants",
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",

                "home_featured_hitter": {
                    "name": "Mookie Betts",
                    "avg": ".320",
                    "hr": 3
                },
                "away_featured_hitter": {
                    "name": "Mike Yastrzemski",
                    "avg": ".270",
                    "hr": 4
                },

                "home_pitcher": "Clayton Kershaw",
                "away_pitcher": "Logan Webb",
                "game_time": "4:05 PM ET",

                "home_colors": {"primary": "#005A9C"},
                "away_colors": {"primary": "#FD5A1E"}
            }
        ],

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

        "top_hitters": [
            {
                "name": "Aaron Judge",
                "team": "NYY",
                "score": 94,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "colors": {"primary": "#132448"}
            },
            {
                "name": "Mookie Betts",
                "team": "LAD",
                "score": 92,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
                "colors": {"primary": "#005A9C"}
            },
            {
                "name": "Rafael Devers",
                "team": "BOS",
                "score": 89,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "colors": {"primary": "#BD3039"}
            }
        ],

        "pitchers": [
            {
                "name": "Corbin Burnes",
                "team": "MIL",
                "era": 2.45,
                "whip": 0.98,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
                "colors": {"primary": "#12284B"}
            },
            {
                "name": "Chris Sale",
                "team": "BOS",
                "era": 3.78,
                "whip": 1.20,
                "logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "colors": {"primary": "#BD3039"}
            }
        ],

        "stadium_factors": [
            {"stadium": "Coors Field", "hr_factor": 1.35},
            {"stadium": "Yankee Stadium", "hr_factor": 1.25}
        ],

        "weather_factors": [
            {"game": "NYY vs BOS", "wind": "12 mph Out to RF", "temp": 68},
            {"game": "CHC vs MIL", "wind": "5 mph In", "temp": 59}
        ],

        "momentum": [
            {"team": "Yankees", "trend": "Won 4 of last 5"},
            {"team": "Dodgers", "trend": "Won 6 straight"}
        ],

        "league_scoring_trends": {
            "runs_per_game": 9.1,
            "hr_per_game": 2.3
        },

        "team_streaks": [
            {"team": "Dodgers", "streak": "W6"},
            {"team": "Giants", "streak": "L4"}
        ]
    }
