# app/models.py

from typing import List, Optional
from pydantic import BaseModel


class Pitcher(BaseModel):
    name: str
    team: str
    era: float
    whip: float
    photo_url: Optional[str] = None


class Hitter(BaseModel):
    name: str
    team: str
    avg: float
    obp: float
    slg: float
    hr: int
    rbi: int
    photo_url: Optional[str] = None


class Matchup(BaseModel):
    home_team: str
    away_team: str
    home_pitcher: Pitcher
    away_pitcher: Pitcher
    top_hitters: List[Hitter] = []


class Dashboard(BaseModel):
    matchups: List[Matchup]
    hitters: List[Hitter]
    pitchers: List[Pitcher]
