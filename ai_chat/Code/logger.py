# logger.py
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, level=logging.DEBUG, max_log_size=10485760, backup_count=3):
    # Define the log directory and file path
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    log_file_path = os.path.join(log_directory, 'app.log')

    # Ensure the directory exists
    os.makedirs(log_directory, exist_ok=True)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler that writes log messages to a file with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
    file_handler.setLevel(level)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
