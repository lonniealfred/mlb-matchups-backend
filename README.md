\# MLB Matchups – Automated MLB Scoring \& Analytics Engine



MLB Matchups is a fully automated backend system that scrapes real-time MLB data from ESPN, computes advanced matchup scores, and exposes a clean `/dashboard` API endpoint for use in analytics dashboards, betting tools, or fantasy baseball apps.



The system combines:

\- Real ESPN lineups

\- Batter vs Pitcher history

\- Hit streaks

\- Pitcher vulnerability scoring

\- Stadium HR factors

\- Team offense scoring

\- Final game-level matchup scores



All data is processed through a modular scoring engine and returned as typed Pydantic models via FastAPI.



---



\## 🚀 Features



\- \*\*Real ESPN scraping\*\* (scoreboard, lineups, pitcher stats, BvP, streaks, stadium factors)

\- \*\*Custom scoring engine\*\* for hitters, pitchers, stadiums, and full game matchups

\- \*\*Clean aggregation layer\*\* that produces final game scores

\- \*\*Typed FastAPI endpoint\*\* returning a `DashboardResponse`

\- \*\*Modular architecture\*\* for easy expansion (Statcast, weather, umpires, etc.)

\- \*\*Auto-generated API docs\*\* at `/docs`



---



\## 📁 Project Structure





