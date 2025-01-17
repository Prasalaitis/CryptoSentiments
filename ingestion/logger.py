import logging
import os

# Environment configurations for logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Initialize the root logger
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger("ApplicationLogger")

# Add a console handler (stdout logging)
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
