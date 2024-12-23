# Fragrantica Scraper

This repository contains a Python script that uses Playwright to scrape fragrance data from the Fragrantica website. The script extracts various details about a specific perfume, including its title, main accords, user evaluations, and more.

## Features

- Navigate to a specific perfume page on Fragrantica.
- Extract the perfume title.
- Retrieve the main accords and their corresponding percentages.
- Gather user votes on ownership and desire for the perfume.
- Collect user evaluations on various criteria (e.g., longevity, sillage, gender suitability).
- Extract the perfume rating and the number of votes.
- Get the fragrance pyramid (top, middle, and base notes).
- Assess the price-to-value ratio based on user feedback.

## Requirements

- Python 3.7 or higher
- Playwright library

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:FGJ666/fragrantica-parser.git
   cd fragrantica-scraper
   ```

2. Create a `conda` environment using the provided `environment.yml` file:

   ```bash
   conda env create -f environment.yml
   ```

3. Activate the conda environment:

   ```bash
   conda activate fragrantica-scraper
   ```

4. Install Playwright browsers:

   ```bash
   playwright install
   ```

## Usage

1. Open the script in your preferred code editor.
2. Modify the URL in the `navigate_to_fragrantica` function if you want to scrape a different perfume.
3. Run the script:

   ```bash
   python fragrantica_scraper.py
   ```

4. Follow the prompts in the terminal. The browser will open and navigate to the specified perfume page. The extracted data will be printed in the terminal.

## Functions

- `navigate_to_fragrantica(page: Page)`: Navigates to the specified perfume page and retrieves the title.
- `get_main_accords(page: Page)`: Extracts the main accords and their percentages.
- `get_wish(page: Page)`: Finds user votes on ownership and desire for the perfume.
- `get_fragrance_evaluation(page: Page)`: Collects user evaluations on various criteria.
- `get_fragrance_season(page: Page)`: Retrieves user evaluations on the suitable season for the fragrance.
- `get_rating(page: Page)`: Gets the perfume rating and the number of votes.
- `get_perfume_pyramid(page: Page)`: Extracts the fragrance pyramid (top, middle, and base notes).
- `get_longevity(page: Page)`: Gathers user feedback on the longevity of the fragrance.
- `get_sillage(page: Page)`: Collects user feedback on the sillage of the fragrance.
- `get_gender(page: Page)`: Retrieves user feedback on the gender suitability of the fragrance.
- `get_price_value(page: Page)`: Gathers user feedback on the price-to-value ratio of the fragrance.