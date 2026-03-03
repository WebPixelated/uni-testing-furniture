import sys
from loguru import logger

# Remove the default handler
logger.remove()

# Console: INFO and above, colored
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>"
    ),
)

# File: DEBUG and above, rotated daily, kept for 7 days
logger.add(
    "logs/test_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} — {message}",
)

__all__ = ["logger"]
