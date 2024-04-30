from loguru import logger

logger.remove(0)

logger.add(
  "loguru.log",
  level="DEBUG",
  rotation="1 week",
  retention="30 days",
  compression="zip",
  serialize=True,
)
