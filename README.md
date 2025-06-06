# GDP ETL Script

This project extracts GDP data from a webpage, transforms it into a usable format, and loads it into a CSV file and a SQLite database. Additionally, it logs the process and queries data from the database.

---

## Features

- Extract GDP data from a Wikipedia page.
- Transform data by cleaning and converting GDP figures into billions.
- Load data into a CSV file and SQLite database.
- Query data for GDP above a specified threshold.

---

## Requirements

- **Python Version:** 3.7 or later
- **Required Libraries:** 
  - `requests`
  - `pandas`
  - `numpy`
  - `BeautifulSoup` (from `bs4`)
  - `sqlite3`
  - `datetime`

Install the required libraries with:
- using command prompt in your computer or terminal in vs code
```bash
pip install requests pandas numpy beautifulsoup4
