# app/demo/demo_trends.py

DEMO_TRENDS = {
    "stadium_factors": [
        {"stadium": "Yankee Stadium", "hr_factor": 1.22},
        {"stadium": "Dodger Stadium", "hr_factor": 0.95},
    ],
    "weather_factors": [
        {"stadium": "Fenway Park", "wind": "12 mph Out to LF"},
    ],
    "momentum": [
        {"team": "Dodgers", "trend": "+3"},
        {"team": "Giants", "trend": "-2"},
    ],
    "league_scoring_trends": {"runs_per_game": 9.1, "hr_per_game": 2.3},
    "team_streaks": [
        {"team": "Yankees", "streak": "W4"},
        {"team": "Red Sox", "streak": "L3"},
    ],
}
