import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set log level
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    app.logger.debug("DEBUG: Logging level set to DEBUG")

    # Configure app logger
    app.logger.setLevel(log_level)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    app.logger.addHandler(console_handler)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1_000_000, backupCount=5)
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    app.logger.addHandler(file_handler)

    # Example Log
    app.logger.info('Logging is set up.')
