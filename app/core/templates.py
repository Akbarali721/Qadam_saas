from jinja2 import ChoiceLoader, FileSystemLoader
from fastapi.templating import Jinja2Templates

from app.core.config import BASE_DIR


templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))
templates.env.loader = ChoiceLoader(
    [
        FileSystemLoader(str(BASE_DIR / "app" / "templates")),
        FileSystemLoader(str(BASE_DIR / "templates")),
    ],
)
