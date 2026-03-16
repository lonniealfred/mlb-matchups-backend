from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your mock dashboard data
from app.services.mock_dashboard import MOCK_DASHBOARD

app = FastAPI()

# CORS middleware (required for frontend → backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard():
    # Return mock data for now
    return MOCK_DASHBOARD
