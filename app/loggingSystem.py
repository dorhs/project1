import logging, os


def setup_logger(log_file="logs/flask_app.log", log_level=logging.INFO):
    """
    Configures the logging system for the Flask app.
    Outputs logs only to the specified log file.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("FlaskAppLogger")
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(threadName)s - %(message)s"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    return logger
