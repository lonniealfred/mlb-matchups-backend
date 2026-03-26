# app/services/team_data.py

# ============================================================
# TEAM NAME → ABBREVIATION (ESPN FULL NAMES)
# ============================================================

TEAM_NAME_TO_ABBR = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Chicago White Sox": "CHW",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Mets": "NYM",
    "New York Yankees": "NYY",
    "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD",
    "Seattle Mariners": "SEA",
    "San Francisco Giants": "SF",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH",
}

# ============================================================
# TEAM LOGOS (BY ABBREVIATION)
# ============================================================

TEAM_LOGOS = {
    "ATL": "https://a.espncdn.com/i/teamlogos/mlb/500/atl.png",
    "ARI": "https://a.espncdn.com/i/teamlogos/mlb/500/ari.png",
    "BAL": "https://a.espncdn.com/i/teamlogos/mlb/500/bal.png",
    "BOS": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
    "CHC": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
    "CHW": "https://a.espncdn.com/i/teamlogos/mlb/500/chw.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/mlb/500/cin.png",
    "CLE": "https://a.espncdn.com/i/teamlogos/mlb/500/cle.png",
    "COL": "https://a.espncdn.com/i/teamlogos/mlb/500/col.png",
    "DET": "https://a.espncdn.com/i/teamlogos/mlb/500/det.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/mlb/500/hou.png",
    "KC":  "https://a.espncdn.com/i/teamlogos/mlb/500/kc.png",
    "LAA": "https://a.espncdn.com/i/teamlogos/mlb/500/laa.png",
    "LAD": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
    "MIA": "https://a.espncdn.com/i/teamlogos/mlb/500/mia.png",
    "MIL": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
    "MIN": "https://a.espncdn.com/i/teamlogos/mlb/500/min.png",
    "NYM": "https://a.espncdn.com/i/teamlogos/mlb/500/nym.png",
    "NYY": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
    "OAK": "https://a.espncdn.com/i/teamlogos/mlb/500/oak.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/mlb/500/phi.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/mlb/500/pit.png",
    "SD":  "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/mlb/500/sea.png",
    "SF":  "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",
    "STL": "https://a.espncdn.com/i/teamlogos/mlb/500/stl.png",
    "TB":  "https://a.espncdn.com/i/teamlogos/mlb/500/tb.png",
    "TEX": "https://a.espncdn.com/i/teamlogos/mlb/500/tex.png",
    "TOR": "https://a.espncdn.com/i/teamlogos/mlb/500/tor.png",
    "WSH": "https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png",
}

# ============================================================
# TEAM COLORS (BY ABBREVIATION)
# ============================================================

TEAM_COLORS = {
    "ATL": {"primary": "#CE1141", "secondary": "#13274F"},
    "ARI": {"primary": "#A71930", "secondary": "#000000"},
    "BAL": {"primary": "#DF4601", "secondary": "#000000"},
    "BOS": {"primary": "#BD3039", "secondary": "#0D2B56"},
    "CHC": {"primary": "#0E3386", "secondary": "#CC3433"},
    "CHW": {"primary": "#000000", "secondary": "#C4CED4"},
    "CIN": {"primary": "#C6011F", "secondary": "#000000"},
    "CLE": {"primary": "#00385D", "secondary": "#E31937"},
    "COL": {"primary": "#33006F", "secondary": "#C4CED4"},
    "DET": {"primary": "#0C2340", "secondary": "#FA4616"},
    "HOU": {"primary": "#002D62", "secondary": "#EB6E1F"},
    "KC":  {"primary": "#004687", "secondary": "#BD9B60"},
    "LAA": {"primary": "#BA0021", "secondary": "#003263"},
    "LAD": {"primary": "#005A9C", "secondary": "#EF3E42"},
    "MIA": {"primary": "#00A3E0", "secondary": "#EF3340"},
    "MIL": {"primary": "#12284B", "secondary": "#FFC52F"},
    "MIN": {"primary": "#002B5C", "secondary": "#D31145"},
    "NYM": {"primary": "#002D72", "secondary": "#FF5910"},
    "NYY": {"primary": "#132448", "secondary": "#C4CED4"},
    "OAK": {"primary": "#003831", "secondary": "#EFB21E"},
    "PHI": {"primary": "#E81828", "secondary": "#002D72"},
    "PIT": {"primary": "#000000", "secondary": "#FDB827"},
    "SD":  {"primary": "#2F241D", "secondary": "#FFC425"},
    "SEA": {"primary": "#0C2C56", "secondary": "#005C5C"},
    "SF":  {"primary": "#FD5A1E", "secondary": "#000000"},
    "STL": {"primary": "#C41E3A", "secondary": "#0A2252"},
    "TB":  {"primary": "#092C5C", "secondary": "#8FBCE6"},
    "TEX": {"primary": "#003278", "secondary": "#C0111F"},
    "TOR": {"primary": "#134A8E", "secondary": "#E8291C"},
    "WSH": {"primary": "#AB0003", "secondary": "#14225A"},
}

# ============================================================
# GETTERS (SAFE)
# ============================================================

def get_team_logo(team_name: str) -> str:
    abbr = TEAM_NAME_TO_ABBR.get(team_name)
    return TEAM_LOGOS.get(abbr, "")

def get_team_colors(team_name: str) -> dict:
    abbr = TEAM_NAME_TO_ABBR.get(team_name)
    return TEAM_COLORS.get(abbr, {"primary": "#1e293b"})

# ============================================================
# STATIC STADIUM FACTORS
# ============================================================

STADIUM_FACTORS = [
    {"team": "COL", "park_factor": 1.28, "hr_factor": 1.32, "name": "Coors Field"},
    {"team": "NYY", "park_factor": 1.12, "hr_factor": 1.25, "name": "Yankee Stadium"},
    {"team": "BOS", "park_factor": 1.10, "hr_factor": 0.95, "name": "Fenway Park"},
    {"team": "CIN", "park_factor": 1.09, "hr_factor": 1.18, "name": "Great American Ball Park"},
    {"team": "LAD", "park_factor": 0.98, "hr_factor": 0.92, "name": "Dodger Stadium"},
    {"team": "SEA", "park_factor": 0.95, "hr_factor": 0.88, "name": "T-Mobile Park"},
    {"team": "SD",  "park_factor": 0.93, "hr_factor": 0.85, "name": "Petco Park"},
    {"team": "SF",  "park_factor": 0.90, "hr_factor": 0.82, "name": "Oracle Park"},
]

def get_stadium_factors():
    return STADIUM_FACTORS

# ============================================================
# WEATHER FACTORS
# ============================================================

WEATHER_FACTORS = [
    {"condition": "Clear", "run_factor": 1.05, "hr_factor": 1.08},
    {"condition": "Partly Cloudy", "run_factor": 1.02, "hr_factor": 1.03},
    {"condition": "Overcast", "run_factor": 0.98, "hr_factor": 0.95},
    {"condition": "Rain", "run_factor": 0.92, "hr_factor": 0.85},
    {"condition": "Wind Out", "run_factor": 1.12, "hr_factor": 1.20},
    {"condition": "Wind In", "run_factor": 0.90, "hr_factor": 0.82},
]

def get_weather_factors():
    return WEATHER_FACTORS

# ============================================================
# TEAM MOMENTUM
# ============================================================

TEAM_MOMENTUM = [
    {"team": "ATL", "last10": "7-3", "momentum": 0.72},
    {"team": "NYY", "last10": "6-4", "momentum": 0.66},
    {"team": "LAD", "last10": "5-5", "momentum": 0.50},
    {"team": "COL", "last10": "3-7", "momentum": 0.32},
    {"team": "OAK", "last10": "2-8", "momentum": 0.20},
]

def get_team_momentum():
    return TEAM_MOMENTUM

# ============================================================
# LEAGUE SCORING TRENDS
# ============================================================

LEAGUE_SCORING_TRENDS = {
    "avg_runs_per_game": 9.1,
    "avg_hr_per_game": 2.1,
    "run_trend_7d": +0.12,
    "hr_trend_7d": +0.05,
    "run_trend_30d": -0.08,
    "hr_trend_30d": -0.03,
}

def get_league_scoring_trends():
    return LEAGUE_SCORING_TRENDS

# ============================================================
# TEAM HOT / COLD STREAKS
# ============================================================

TEAM_STREAKS = [
    {"team": "PHI", "streak": "+5", "type": "hot"},
    {"team": "SEA", "streak": "+4", "type": "hot"},
    {"team": "MIA", "streak": "-6", "type": "cold"},
    {"team": "KC",  "streak": "-4", "type": "cold"},
]

def get_team_streaks():
    return TEAM_STREAKS
