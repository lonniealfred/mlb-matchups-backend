from fastapi import FastAPI
from app.services.mock_dashboard import MOCK_DASHBOARD

app = FastAPI()

@app.get("/dashboard")
def dashboard():
    return MOCK_DASHBOARD
