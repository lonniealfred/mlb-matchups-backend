from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Restore your real scraper import
from app.services.espn_scraper import build_dashboard

app = FastAPI()

# Keep CORS — your frontend requires this
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

@app.get("/dashboard")
def dashboard():
    # Restore live data
    return build_dashboard()
