from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.espn_scraper import build_dashboard
from app.services.matchups import build_matchups
from app.services.scoring import score_pitcher, score_hitter

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}


# ---------------------------------------------------------
# 1) FULL MATCHUPS ENDPOINT (already implemented)
# ---------------------------------------------------------
@app.get("/dashboard")
def dashboard():
    raw = build_dashboard()              # Safe ESPN scraper
    games = raw.get("games", [])
    matchups = build_matchups(games)     # Safe scoring + fallback

    return {"games": matchups}


# ---------------------------------------------------------
# 2) PITCHERS ENDPOINT (fallback-aware)
# ---------------------------------------------------------
@app.get("/pitchers")
def pitchers():
    raw = build_dashboard()
    games = raw.get("games", [])
    matchups = build_matchups(games)

    pitcher_list = []

    for g in matchups:
        home_p = g["pitchers"]["home_pitcher"]
        away_p = g["pitchers"]["away_pitcher"]

        pitcher_list.append({
            "game_id": g["game_id"],
            "team": g["home_team"],
            "pitcher": home_p
        })

        pitcher_list.append({
            "game_id": g["game_id"],
            "team": g["away_team"],
            "pitcher": away_p
        })

    # Always return at least demo pitchers
    if not pitcher_list:
        pitcher_list = [
            {"team": "NYY", "pitcher": score_pitcher(None)},
            {"team": "BOS", "pitcher": score_pitcher(None)}
        ]

    return {"pitchers": pitcher_list}


# ---------------------------------------------------------
# 3) HITTERS ENDPOINT (fallback-aware)
# ---------------------------------------------------------
@app.get("/hitters")
def hitters():
    raw = build_dashboard()
    games = raw.get("games", [])
    matchups = build_matchups(games)

    hitter_list = []

    for g in matchups:
        for h in g["top_hitters"]["home_top_hitters"]:
            hitter_list.append({
                "game_id": g["game_id"],
                "team": g["home_team"],
                "hitter": h
            })

        for h in g["top_hitters"]["away_top_hitters"]:
            hitter_list.append({
                "game_id": g["game_id"],
                "team": g["away_team"],
                "hitter": h
            })

    # Always return demo hitters if empty
    if not hitter_list:
        hitter_list = [
            {"team": "NYY", "hitter": score_hitter(None, None)},
            {"team": "BOS", "hitter": score_hitter(None, None)}
        ]

    return {"hitters": hitter_list}


# ---------------------------------------------------------
# 4) TRENDS ENDPOINT (fallback-aware)
# ---------------------------------------------------------
@app.get("/trends")
def trends():
    raw = build_dashboard()
    games = raw.get("games", [])
    matchups = build_matchups(games)

    stadium_factors = []
    pitcher_scores = []
    hitter_scores = []

    for g in matchups:
        # Stadium HR factor (fallback to 1.10)
        stadium_factors.append({
            "game_id": g["game_id"],
            "home_team": g["home_team"],
            "away_team": g["away_team"],
            "hr_factor": g.get("stadium_hr_factor", 1.10)
        })

        # Pitcher trends
        pitcher_scores.append({
            "team": g["home_team"],
            "pitcher": g["pitchers"]["home_pitcher"]
        })
        pitcher_scores.append({
            "team": g["away_team"],
            "pitcher": g["pitchers"]["away_pitcher"]
        })

        # Hitter trends
        for h in g["top_hitters"]["home_top_hitters"]:
            hitter_scores.append(h)
        for h in g["top_hitters"]["away_top_hitters"]:
            hitter_scores.append(h)

    # Fallback if ESPN returns nothing
    if not stadium_factors:
        stadium_factors = [
            {"game_id": "demo", "home_team": "NYY", "away_team": "BOS", "hr_factor": 1.25}
        ]

    if not pitcher_scores:
        pitcher_scores = [
            {"team": "NYY", "pitcher": score_pitcher(None)},
            {"team": "BOS", "pitcher": score_pitcher(None)}
        ]

    if not hitter_scores:
        hitter_scores = [
            score_hitter(None, None),
            score_hitter(None, None)
        ]

    return {
        "stadium_factors": stadium_factors,
        "pitcher_scores": pitcher_scores,
        "hitter_scores": hitter_scores
    }
