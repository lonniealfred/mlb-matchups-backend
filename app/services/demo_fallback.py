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
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb