import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, log_file: str, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Логгер для общего использования
app_logger = setup_logger("app", "app.log")
celery_logger = setup_logger("celery", "celery.log")
