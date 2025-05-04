# RemoteOK Job Scraper

A simple and efficient command-line tool for scraping job listings from [RemoteOK](https://remoteok.com), built using `zendriver` and `BeautifulSoup`. This tool allows users to collect job data, detect new listings since a specified date, or perform both actions. The results are exported to clean, structured CSV files for further analysis.

---

##  Features

- Command-line interface (CLI) for flexible interaction
- Configurable scraping options saved in a config file
- Export job listings to CSV format
- Choose between three modes:
  - Full data collection
  - Change detection (new jobs only)
  - Combined mode
- Date-based filtering for new listings
- Clean and minimal dependency set

---

## Requirements

- Python 3.10 or higher

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Entire-Circus/remoteok-job-scraper.git
cd remoteok-job-scraper
pip install -r requirements.txt
```

## Usage & Output

Run the scraper from the command line:

```bash
python -m src.main
```
You'll be prompted to:

Choose whether to reuse existing configuration or enter new settings

Optionally paste a filtered job search URL from RemoteOK

Select a scraping mode:

1 – Full data collection

2 – Detect new listings since a date

3 – Perform both actions

(If applicable) Enter a start date in YYYY-MM-DD format

# Output:

All scraped job listings are saved as CSV files in the /data folder

User settings and options are stored as JSON configs in the /config folder
