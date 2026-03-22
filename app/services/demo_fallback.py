# app/services/demo_fallback.py

from typing import Dict, Any

def get_demo_dashboard() -> Dict[str, Any]:
    return {
        "matchups": [
            {
                "home_team": "New York Yankees",
                "away_team": "Boston Red Sox",
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
                "start_time": "2024-04-01T23:05:00Z",
                "venue": "Yankee Stadium",
                "weather": {
                    "temp_f": 62,
                    "condition": "Clear",
                    "wind_mph": 5
                },
                "analytics": {
                    "run_expectancy": 9.1,
                    "park_factor": 1.12,
                    "weather_factor": 1.05,
                    "momentum_rating": 0.7
                }
            },
            {
                "home_team": "Los Angeles Dodgers",
                "away_team": "San Diego Padres",
                "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
                "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
                "start_time": "2024-04-01T02:10:00Z",
                "venue": "Dodger Stadium",
                "weather": {
                    "temp_f": 72,
                    "condition": "Partly Cloudy",
                    "wind_mph": 3
                },
                "analytics": {
                    "run_expectancy": 8.4,
                    "park_factor": 1.08,
                    "weather_factor": 1.02,
                    "momentum_rating": 0.6
                }
            }
        ],
        "pitchers": [],
        "hitters": [],
        "status": "demo",
        "message": "Demo fallback data loaded successfully."
    }
