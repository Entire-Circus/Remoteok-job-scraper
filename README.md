# remoteok-job-scraper

RemoteOK Job Scraper
A simple, efficient command-line tool for scraping job listings from RemoteOK using zendriver and BeautifulSoup. It allows users to collect data, track new listings since a specified date, or perform both actions. Results are saved in CSV format for further analysis.

Features
Command-line interface (CLI) for flexible user input

Configurable scraping options stored in a config file

Data export to structured CSV files

Easy mode selection: data collection, change detection, or both

Date-based filtering for new listings

Requirements
Python 3.10+

Installation
Clone the repository:

git clone https://github.com/Entire-Circus/remoteok-job-scraper.git
cd remoteok-job-scraper

Install dependencies:

pip install -r requirements.txt
Usage
Run the scraper from the command line:

python -m src.main
You will be prompted to:

Use existing config or enter new settings

Enter a custom filtered URL (optional)

Choose scraping mode:

(1) Data collection

(2) Detect new listings

(3) Both

Enter a date if detecting new listings

CSV files will be saved in the /data folder, and configurations in /config.

Folder Structure

remoteok-job-scraper/
│
├── config/         # Stores user configs (JSON)
├── data/           # Output CSV files
├── src/            # Source code
│   ├── cli.py
│   ├── config_handler.py
│   ├── scraper.py
│   ├── utils.py
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md

License
This project is intended for educational and portfolio purposes only. All rights reserved.
