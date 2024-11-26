import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.settings import Settings

router = APIRouter(
    # prefix="/ui",
)

settings = Settings()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="static/templates")

@router.get("/")
def index(request: Request):
    """Render the index page."""
    logger.info("Rendering the index page")
    return templates.TemplateResponse("index.html", {"request": request})
