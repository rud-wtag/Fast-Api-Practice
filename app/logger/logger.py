from loguru import logger

from app.core.config import settings

logger.remove(0)

logger.add(
  settings.LOG_FILE,
  level=settings.LOG_LEVEL,
  rotation=settings.LOG_ROTATION,
  retention=settings.LOG_RENTATION,
  compression="zip",
  serialize=settings.LOG_SERIALIZATION,
)
