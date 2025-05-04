import logging
from datetime import datetime
from typing import Any


def setup_logger() -> logging.Logger:
    """
    Sets up and returns a console logger with a custom format for WSCMS execution details.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define the custom format to include job scraping metrics and timestamp
    formatter = logging.Formatter(
        "Scraper finished execution\n"
        "Duration: %(duration)s seconds\n"
        "URL used: %(url)s\n"
        "Rows saved: %(rows_saved)d\n"
        "New jobs saved: %(new_jobs_saved)d\n"
        "Time: %(time)s\n"
    )

    # Set up stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def log_wscms_info(
    logger: logging.Logger,
    duration: float,
    url: str,
    rows_saved: int,
    new_jobs_saved: int
) -> None:
    """
    Logs job scraping execution summary using the provided logger.

    Args:
        logger (logging.Logger): Logger instance configured with setup_logger().
        duration (float): Total execution time in seconds.
        url (str): Source URL used for scraping.
        rows_saved (int): Total number of job rows saved to the file.
        new_jobs_saved (int): Number of newly scraped jobs.
    """
    log_data = {
        "duration": round(duration, 2),
        "url": url,
        "rows_saved": rows_saved,
        "new_jobs_saved": new_jobs_saved,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Empty string for message because output is defined entirely by the formatter
    logger.info("", extra=log_data)
