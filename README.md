# Fragrantica Scraper

## Overview

This repository contains a script for scraping fragrance data from the Fragrantica website using Python and Selenium. The script extracts various details about fragrances such as names, accords, user ratings, longevity, sillage, and more.

## Requirements

To run the script, you need the following libraries installed:

```bash
pip install pandas numpy selenium requests
```

Additionally, make sure you have the Chrome WebDriver installed and accessible from your PATH.

## Notes

- Ensure that the paths to your CSV files are correct.
- Adjust the number of links to scrape according to your needs by modifying the range in the scraping loop.
- Be aware of website scraping policies and handle requests responsibly to avoid getting blocked.
