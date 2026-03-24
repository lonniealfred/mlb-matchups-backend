# app/data/team_data.py

"""
Unified MLB team metadata module.
Used by all scrapers to ensure consistent:
- Abbreviations
- Logos
- Colors
- Safe defaults
"""

# -----------------------------------------
# TEAM ABBREVIATIONS (ESPN format)
# -----------------------------------------

TEAM_ABBR = {
    "Yankees": "nyy",
    "Red Sox": "bos",
    "Cubs": "chc",
    "Brewers": "mil",
    "Dodgers": "lad",
    "Giants": "sf",
    "Mets": "nym",
    "Phillies": "phi",
    "Braves": "atl",
    "Nationals": "wsh",
    "Orioles": "bal",
    "Blue Jays": "tor",
    "Rays": "tb",
    "Guardians": "cle",
    "Tigers": "det",
    "White Sox": "chw",
    "Twins": "min",
    "Royals": "kc",
    "Astros": "hou",
    "Rangers": "tex",
    "Mariners": "sea",
    "Athletics": "oak",
    "Angels": "laa",
    "Padres": "sd",
    "Diamondbacks": "ari",
    "Rockies": "col",
    "Cardinals": "stl",
    "Pirates": "pit",
    "Reds": "cin",
    "Marlins": "mia",
}

# -----------------------------------------
# TEAM LOGOS (ESPN 500px)
# -----------------------------------------

TEAM_LOGOS = {
    name: f"https://a.espncdn.com/i/teamlogos/mlb/500/{abbr}.png"
    for name, abbr in TEAM_ABBR.items()
}

# -----------------------------------------
# TEAM COLORS (primary brand color)
# -----------------------------------------

TEAM_COLORS = {
    "Yankees": {"primary": "#132448"},
    "Red Sox": {"primary": "#BD3039"},
    "Cubs": {"primary": "#0E3386"},
    "Brewers": {"primary": "#12284B"},
    "Dodgers": {"primary": "#005A9C"},
    "Giants": {"primary": "#FD5A1E"},
    "Mets": {"primary": "#002D72"},
    "Phillies": {"primary": "#E81828"},
    "Braves": {"primary": "#CE1141"},
    "Nationals": {"primary": "#AB0003"},
    "Orioles": {"primary": "#DF4601"},
    "Blue Jays": {"primary": "#134A8E"},
    "Rays": {"primary": "#092C5C"},
    "Guardians": {"primary": "#0C2340"},
    "Tigers": {"primary": "#0C2340"},
    "White Sox": {"primary": "#27251F"},
    "Twins": {"primary": "#002B5C"},
    "Royals": {"primary": "#004687"},
    "Astros": {"primary": "#002D62"},
    "Rangers": {"primary": "#003278"},
    "Mariners": {"primary": "#0C2C56"},
    "Athletics": {"primary": "#003831"},
    "Angels": {"primary": "#BA0021"},
    "Padres": {"primary": "#2F241D"},
    "Diamondbacks": {"primary": "#A71930"},
    "Rockies": {"primary": "#33006F"},
    "Cardinals": {"primary": "#C41E3A"},
    "Pirates": {"primary": "#FDB827"},
    "Reds": {"primary": "#C6011F"},
    "Marlins": {"primary": "#00A3E0"},
}

DEFAULT_COLORS = {"primary": "#111827"}  # slate gray fallback


# -----------------------------------------
# GETTERS (safe, frontend‑friendly)
# -----------------------------------------

def get_team_abbr(name: str) -> str | None:
    return TEAM_ABBR.get(name)


def get_team_logo(name: str) -> str:
    return TEAM_LOGOS.get(name, "")


def get_team_colors(name: str) -> dict:
    return TEAM_COLORS.get(name, DEFAULT_COLORS)


def get_team_meta(name: str) -> dict:
    """
    Returns a full metadata object for a team:
    {
        "abbr": "nyy",
        "logo": "...",
        "colors": { "primary": "#132448" }
    }
    """
    return {
        "abbr": get_team_abbr(name),
        "logo": get_team_logo(name),
        "colors": get_team_colors(name),
    }
