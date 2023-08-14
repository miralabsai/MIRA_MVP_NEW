import logging
import sys

def get_logger(name: str):
    # Create a logger
    logger = logging.getLogger(name)
    logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(logging.DEBUG)

    return logger
