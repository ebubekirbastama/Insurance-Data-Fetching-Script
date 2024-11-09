# Insurance Data Fetching Script

This Python script retrieves and aggregates vehicle insurance data from the [TSB](https://www.tsb.org.tr/) API. The program utilizes concurrent requests to improve performance and writes the retrieved data to a JSON file.

## Features

- Fetches available vehicle years, brands, models, and insurance data.
- Uses multithreading to fetch data efficiently.
- Saves the collected data to a `insurance_data.json` file.

## Requirements

- Python 3.x
- `requests` library

Install the required packages with:
```bash
pip install requests
```
