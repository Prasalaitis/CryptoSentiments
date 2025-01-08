import logging
from logging.handlers import RotatingFileHandler
import os

# Environment configurations for logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 10 * 1024 * 1024))  # 10 MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 5))

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Initialize the root logger
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger("ApplicationLogger")

# Add a rotating file handler
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)

# Add a console handler for stdout logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(console_handler)

# Set the logging level for all handlers
logger.setLevel(LOG_LEVEL)

if __name__ == "__main__":
    logger.info("Logger initialized.")
    logger.debug("Debugging enabled.")
    logger.warning("This is a warning.")
    logger.error("This is an error message.")
    logger.critical("Critical error encountered.")
