from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ---------------------------------------------------------
# Stadium
# ---------------------------------------------------------

class Stadium(BaseModel):
    name: str
    hr_factor: float
    stadium_score: Optional[float] = None


# ---------------------------------------------------------
# Pitchers
# ---------------------------------------------------------

class Pitcher(BaseModel):
    name: str
    era: float
    recent_er: float
    split_ops: float
    era_vs_team: Optional[float] = None
    vulnerability_score: Optional[float] = None
    id: Optional[str] = None


class PitcherSet(BaseModel):
    away_pitcher: Pitcher
    home_pitcher: Pitcher


# ---------------------------------------------------------
# Hitters
# ---------------------------------------------------------

class Hitter(BaseModel):
    name: str
    hr_vs_pitcher: int
    avg_vs_pitcher: float
    pa_vs_pitcher: int
    streak: int
    hitter_score: Optional[float] = None


class HitterSet(BaseModel):
    away_top_hitters: List[Hitter]
    home_top_hitters: List[Hitter]


# ---------------------------------------------------------
# Team Offense Scores
# ---------------------------------------------------------

class TeamScores(BaseModel):
    away_offense_score: float
    home_offense_score: float


# ---------------------------------------------------------
# Game Object
# ---------------------------------------------------------

class Game(BaseModel):
    game_id: int
    start_time: datetime
    away_team: str
    home_team: str
    stadium: Stadium
    pitchers: PitcherSet
    hitters: HitterSet
    team_scores: TeamScores
    game_score: float


# ---------------------------------------------------------
# Global Hit Streak Leaderboard
# ---------------------------------------------------------

class HitStreak(BaseModel):
    player: str
    team: str
    streak: int
    today_opponent: str
    today_pitcher: str


# ---------------------------------------------------------
# Dashboard Response
# ---------------------------------------------------------

class DashboardResponse(BaseModel):
    date: str
    games: List[Game]
    hit_streaks: List[HitStreak]
