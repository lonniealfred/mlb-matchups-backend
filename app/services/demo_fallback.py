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
                }
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
                }
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
                }
            }
        ],

        "hitters": [],
        "top_hitters": [],
        "pitchers": [],
        "stadium_factors": [],
        "momentum": [],
        "weather_factors": [],
        "league_scoring_trends": [],
        "team_streaks": []
    }
