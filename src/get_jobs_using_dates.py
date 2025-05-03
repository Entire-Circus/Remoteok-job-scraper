import pandas as pd
from datetime import datetime

def get_jobs_with_dates(ask_date: datetime, df: pd.DataFrame) -> int:
    """
    Filters job postings by a given minimum date and saves the results to a CSV file.

    Args:
        ask_date (datetime): The earliest date a job posting can have.
        df (pd.DataFrame): The original DataFrame containing job postings.

    Returns:
        int: The number of job postings that match the date filter.
    """
    # Convert the "Posted (Date)" column to datetime format
    df["Posted (Date)"] = pd.to_datetime(df["Posted (Date)"], format="%Y-%m-%d")

    # Filter rows where the posting date is on or after the specified date
    filtered_rows = df[df["Posted (Date)"] >= ask_date]

    # Save filtered results to a new CSV file (encoding preserves emojis/special characters)
    filtered_rows.to_csv("../data/New jobs.csv", index=False, encoding='utf-8-sig')

    return len(filtered_rows)
