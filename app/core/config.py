import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_environment() -> None:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


load_environment()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./relationship_analyzer.db")
_raw_public_base = (
    os.getenv("BASE_URL")
    or os.getenv("WEBAPP_BASE_URL")
    or os.getenv("APP_BASE_URL")
    or ""
)
BASE_URL = _raw_public_base.rstrip("/")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
TELEGRAM_BOT_USERNAME = (os.getenv("TELEGRAM_BOT_USERNAME") or os.getenv("BOT_USERNAME") or "").lstrip("@")
WEBAPP_BASE_URL = BASE_URL
ADMIN_USERNAME = (os.getenv("ADMIN_USERNAME") or "").lstrip("@")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID") or ""
ADMIN_CONTACT_URL = (os.getenv("ADMIN_CONTACT_URL") or "").strip()
