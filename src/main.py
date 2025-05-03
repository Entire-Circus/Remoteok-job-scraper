# Async job scraper for RemoteOK using ZenDriver and BeautifulSoup
# Outputs job listings to a CSV file

import asyncio
import time
import os
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
import zendriver as zd

from safe_load import safe_load
from custom_scroll import ask_scroll_input, custom_scroll
from get_jobs_using_dates import get_jobs_with_dates
from cached_input import (
    cached_input, yes_no_validator, url_validator,
    date_validator, numbers_validator
)
from logger import setup_logger, log_wscms_info


async def main(ask_type: int, ask_date: str | None = None, custom_url: str | None = None) -> None:
    """
    Runs the asynchronous job scraping process.

    Args:
        ask_type (int): Mode of operation (1 = scrape only, 2 = monitor only, 3 = both).
        ask_date (str | None): Cutoff date for monitoring mode.
        custom_url (str | None): Custom URL to scrape from (instead of base).
    """
    base_url = "https://remoteok.com/"
    start_time = time.time()
    browser = await zd.start()

    page = await browser.get(custom_url if custom_url else base_url)

    await safe_load(page)
    scroll_amount = ask_scroll_input()
    await custom_scroll(page, scroll_amount)

    html = await page.get_content()
    soup = BeautifulSoup(html, "html.parser")
    jobs = soup.find_all("tr", class_="job")

    job_data = []
    row_count = 0

    for job in jobs:
        try:
            href = job.find("td", class_="company").find("a")["href"]
            url = base_url + href
        except AttributeError:
            url = "N/A"

        try:
            job_title = job.find("td", class_="company").find("a", class_="preventLink").find("h2").text.strip()
        except AttributeError:
            job_title = "N/A"

        location_divs = job.find_all("div", class_="location")
        location, salary, contractor = None, None, None

        for div in location_divs:
            text = div.text.strip()
            if any(x in text for x in ["$", "0", "k"]):
                salary = text
            elif "Contractor" in text:
                contractor = text
            else:
                location = f"{location} | {text}" if location else text

        contractor = contractor or "Not contractor"
        location = location or "N/A"
        salary = salary or "N/A"

        tags = job.find_all("h3")
        company_name = tags[0].text.strip()
        tag1 = tags[1].text.strip() if len(tags) > 1 else "N/A"
        tag2 = tags[2].text.strip() if len(tags) > 2 else "N/A"
        tag3 = tags[3].text.strip() if len(tags) > 3 else "N/A"

        try:
            iso = job.find("time")["datetime"]
            dt = datetime.fromisoformat(iso)
            time_posted = dt.strftime("%Y-%m-%d")
        except (AttributeError, TypeError):
            time_posted = "N/A"

        try:
            dh_ago = job.find("time").text.strip()
        except AttributeError:
            dh_ago = "N/A"

        job_data.append({
            "Job Title": job_title,
            "Link": url,
            "Posted (Date)": time_posted,
            "Posted (Relative)": dh_ago + " ago",
            "Estimated salary": salary,
            "Location": location,
            "Contractor?": contractor,
            "Company Name": company_name,
            "Tag1": tag1,
            "Tag2": tag2,
            "Tag3": tag3
        })
        row_count += 1

    df = pd.DataFrame(job_data)
    row_count_new = 0

    if ask_type in [1, 3]:
        df.to_csv("../data/Data.csv", index=False, encoding='utf-8-sig')
    if ask_type in [2, 3]:
        row_count_new = get_jobs_with_dates(ask_date, df)

    duration = time.time() - start_time
    logger = setup_logger()
    log_wscms_info(logger, duration, custom_url or base_url, row_count, row_count_new)


def run_cli() -> None:
    """
    Handles user CLI input and runs the scraper.
    """
    while True:
        user_input = input("Use existing config? (y/n): ").strip().lower()
        if user_input in {"y", "n"}:
            overwrite = user_input == "n"
            break
        print("Enter either y or n")

    ask_url = cached_input("Do you want to input custom URL (y/n)", overwrite=overwrite, validator=yes_no_validator).strip().lower()
    custom_url = cached_input("Open the site, add filters, and paste the URL: ", overwrite=overwrite, validator=url_validator).strip() if ask_url == "y" else None

    ask_type = int(cached_input(
        "Choose mode: data collecting (1), new listings (2), or both (3): ",
        overwrite=overwrite,
        validator=numbers_validator
    ))

    ask_date = (
        cached_input("Enter start date (YYYY-MM-DD): ", overwrite=overwrite, validator=date_validator)
        if ask_type in [2, 3] else None
    )

    asyncio.run(main(ask_type, ask_date=ask_date, custom_url=custom_url))


if __name__ == '__main__':
    run_cli()
