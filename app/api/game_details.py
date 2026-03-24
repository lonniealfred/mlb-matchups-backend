# app/api/game_details.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.scrapers.mlb_bvp import fetch_bvp
from app.scrapers.mlb_streaks import fetch_hit_streak
from app.scrapers.mlb_season_stats import fetch_season_stats
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.data.player_data import get_player_id
from app.data.team_data import get_team_logo, get_team_colors

router = APIRouter()


@router.get("/game/{game_id}")
def get_game_details(game_id: str):
    """
    Deep-dive game details:
    - Full BvP for all hitters
    - Hit streaks
    - Season stats
    - Team branding
    """

    games = fetch_scoreboard()
    game = next((g for g in games if g.get("game_id") == game_id), None)

    if not game:
        return JSONResponse(content={"error": "Game not found"}, status_code=404)

    home = game["home_team"]
    away = game["away_team"]

    hitters = []

    # Collect hitters from both teams
    for team in [home, away]:
        # You can replace this with a real lineup scraper later
        featured = game.get(f"{team.lower()}_featured_hitter", {})
        name = featured.get("name", "TBD")

        player_id = get_player_id(name)

        # Defaults
        bvp = {"bvp_hrs": 0, "bvp_avg": 0.000}
        streak = 0
        season = {"avg": 0.000, "hr": 0}

        if player_id:
            try:
                streak = fetch_hit_streak(player_id)
                season = fetch_season_stats(player_id)
            except Exception:
                pass

        hitters.append({
            "name": name,
            "team": team,
            "logo": get_team_logo(team),
            "colors": get_team_colors(team),
            "bvp": bvp,
            "hit_streak": streak,
            "season": season,
        })

    return JSONResponse(content={
        "game_id": game_id,
        "home_team": home,
        "away_team": away,
        "hitters": hitters,
        "game_time": game.get("game_time", "TBD"),
        "stadium": game.get("stadium", "TBD"),
    })
