# Fragrantica Web Scraper

This repository contains two Python scripts for scraping data from Fragrantica.com: `parser_links.py`, which collects links to perfume pages, and `parser_data.py`, which extracts detailed information about perfumes from those links.

## Project Structure

The project is organized as follows:

├── config/
│   └── config.yaml         # Configuration file for the scripts
├── data/
│   └── fragrance_links.csv # CSV file storing the collected perfume links
│   └── fragrance_data.csv  # CSV file storing the scraped data 
├── logs/
│   └── error_log_data.log  # Log file for errors during data parsing
│   └── error_log_links.log # Log file for errors during link parsing
├── src/
│    # (This directory is currently empty, but can be used to add other scripts)
├── .gitignore            # Files ignored by git
├── environment.yml       # Environment file for setting up the virtual env
├── parser_data.py        # Script to collect detailed perfume data
├── parser_links.py       # Script to collect perfume page links
└── README.md             # This file

## `parser_links.py`

This script gathers links to perfume pages from Fragrantica.com based on gender and year of release. It navigates the website, extracts links, and saves them to `data/fragrance_links.csv`. It iterates through gender categories (male, female, unisex) and scrapes links for perfumes released each year from 2024 down to 1920. The script handles "Show more results" buttons, logs errors to `logs/error_log_links.log`, closes popup banners, uses a configurable timeout, randomly chooses a user agent to mimic real users, and removes duplicate links. The configuration, including website links, the number of elements to parse from a page, timeout, path for saving data, and a list of user agents, is loaded from `config/config.yaml`.

## `parser_data.py`

This script reads the perfume page links from `data/fragrance_links.csv` and extracts detailed information from each page on Fragrantica.com, saving the data to `data/fragrance_data.csv`. It extracts data such as the perfume title, main accords, votes, ratings, seasonality, fragrance notes, longevity, sillage, gender, and price-to-value ratings. The script logs errors to `logs/error_log_data.log` and closes popup banners. Configuration, such as the path to the links file and a list of user agents, is loaded from `config/config.yaml`.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2.  **Create and activate a virtual environment using conda:**

    ```bash
    conda env create --file environment.yml
    conda activate web_scraper
    ```

    This command will create a new conda environment named `web_scraper` using the dependencies specified in `environment.yml`.  This file ensures that you have all the necessary Python packages at the correct versions to run the project.  The `conda activate web_scraper` command then activates this environment so that you are using these installed packages in your current shell.

3.  **Install Playwright browsers:**

    ```bash
    playwright install
    ```
    This command downloads the necessary browser binaries for Playwright to operate correctly.

4. **Configure the `config/config.yaml` file:**
    Adjust parameters such as website links, timeouts, and output paths to your needs.

## Usage

To run the scripts:

1.  Ensure you have activated the conda environment (`conda activate web_scraper`).
2.  Run `parser_links.py` first:

    ```bash
    python parser_links.py
    ```
    This will create the `data/fragrance_links.csv` file containing perfume links.

3.  Then, run `parser_data.py`:

    ```bash
    python parser_data.py
    ```
    This script will use the generated `fragrance_links.csv` to collect data and save it to `data/fragrance_data.csv`.

## Logging

Both scripts utilize Python's `logging` module to record errors during execution. Error messages are saved in:

-   `logs/error_log_links.log` for `parser_links.py`.
-   `logs/error_log_data.log` for `parser_data.py`.

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the [Your License] License - see the [LICENSE.md](LICENSE.md) file for details.
