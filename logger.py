import logging

def setup_logger(logger_name, log_file=None):
    # Configure the logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file) if log_file else logging.StreamHandler()
        ]
    )
    
    # Create and return a logger
    logger = logging.getLogger(logger_name)
    return logger