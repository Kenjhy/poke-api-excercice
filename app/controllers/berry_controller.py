from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.berry_service import BerryService
from app.models.berry_stats_model import BerryStats
from app.utils.histogram import generate_histogram
import os
from pathlib import Path

router = APIRouter()
service = BerryService()

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/allBerryStats", response_model=BerryStats)
async def get_all_berry_stats():
    stats = service.get_berry_stats()
    return JSONResponse(content=stats.dict(), media_type="application/json")


@router.get("/berryStatsHistogram", response_class=HTMLResponse)
async def get_berry_stats_histogram(request: Request):
    stats = service.get_berry_stats()
    histogram = generate_histogram(stats.frequency_growth_time)
    
    return templates.TemplateResponse("histogram_template.html", {"request": request, "histogram": histogram})


@router.get("/apiInfo")
async def get_api_info():
    return {
        "host": os.getenv("API_HOST"),
        "port": os.getenv("API_PORT"),
        "pokeapi_base_url": os.getenv("POKEAPI_BASE_URL")
    }