import sys

from loguru import logger

from app.core.config import settings


logger.remove()

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "{name}:{function}:{line} | "
           "{message}",
)

app_logger = logger