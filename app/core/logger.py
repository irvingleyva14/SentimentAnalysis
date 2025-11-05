# app/core/logger.py
import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """Crea y configura un logger con formato consistente para toda la app."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita agregar handlers duplicados si el logger ya existe
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
