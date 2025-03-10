# Web Scraping Component

This document provides detailed information about the web scraping component of the project, which is implemented in `main.py`.

## Overview

The scraper is designed to extract hotel data from [obilet.com](https://www.obilet.com/), specifically targeting hotel listings. It uses Selenium WebDriver to automate browser interactions, navigate to the hotel search page, and extract detailed information about each hotel.

## How It Works

1. The script navigates to the obilet.com hotel search page with specific parameters (city, check-in/out dates, number of adults).
2. It waits for the hotel listings to load.
3. It scrolls through the page to load all hotel listings.
4. For each hotel listing, it extracts various data points.
5. The extracted data is saved to both JSON and CSV files.

## CSS Selectors Used

The scraper uses the following CSS selectors to extract data:

| Data Point | CSS Selector |
|------------|--------------|
| Hotel Element | `li.item.journey.js-hotel-item` |
| Hotel Image | `.hotel-item__image` |
| Star Rating | `.hotel-item__star .star` |
| Location | `.hotel-location__address` |
| Distance to Center | `.hotel-location__city-center-distance` |
| Features | `.hotel-features__item span` |
| Review Score | `.hotel-review__badge` |
| Review Text | `.hotel-review__text` |
| Review Count | `.hotel-review__comment` |
| Price | `.hotel-price__amount` |
| Daily Price | `.hotel-price__daily-amount` |
| Nights | `.hotel-price__night` |

## Data Extraction

For each hotel, the following data is extracted:

- **id**: Unique identifier for the hotel
- **name**: Hotel name
- **image_url**: URL of the hotel image
- **star_rating**: Number of stars (1-5)
- **location**: Address of the hotel
- **distance_to_center**: Distance from city center
- **features**: List of hotel features/amenities
- **review_score**: Numerical review score
- **review_text**: Textual description of the review score
- **review_count**: Number of reviews
- **price**: Total price for the stay
- **daily_price**: Price per night
- **nights**: Number of nights

## Configuration Options

The main configuration options are defined at the beginning of the `main()` function:

```python
# Options for the hotel search
CITY_CODE = "istanbul-250-60649-2"
CHECKIN, CHECKOUT = find_next_weekend()
ADULTS = 2
```

You can modify these variables to change:
- The city to search for (`CITY_CODE`)
- The check-in and check-out dates (by default, it uses the next weekend)
- The number of adults (`ADULTS`)

## Running the Scraper

To run the scraper:

1. Ensure you have completed the [installation and setup](installation.md).
2. Activate your virtual environment if you're using one.
3. Run the script:
   ```bash
   python main.py
   ```

The script will:
1. Open a Chrome browser window
2. Navigate to the obilet.com hotel search page
3. Scroll through the results to load all hotels
4. Extract data from each hotel listing
5. Save the data to `hotels_data.json` and `hotels_data.csv`

## Output Files

The scraper generates two output files:

1. `hotels_data.json`: Contains the extracted data in JSON format
2. `hotels_data.csv`: Contains the same data in CSV format

These files will be used by the [data analysis component](analysis.md) for further processing.

## Customization

### Targeting Specific Hotels

The script currently includes a specific target hotel to wait for:

```python
target_hotel = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'li.item.journey.js-hotel-item[data-id="101336"][data-name="Swissôtel The Bosphorus İstanbul"]'))
)
```

You can modify this to target a different hotel or remove this specific targeting altogether.

### Adjusting Scroll Behavior

The script scrolls through the page to load all hotel listings. You can adjust the scrolling behavior by modifying:

```python
max_attempts = 30  # Limit the number of scroll attempts
```

Increase this value to allow more scrolling attempts, which may be necessary for searches with many results.

## Troubleshooting

### Common Issues

1. **TimeoutException**: This occurs when the target hotel element doesn't appear within the specified timeout period (30 seconds by default). Possible solutions:
   - Increase the timeout period
   - Check if the hotel is still available on the website
   - Check if the website structure has changed

2. **StaleElementReferenceException**: This occurs when a referenced element is no longer attached to the DOM. The script handles this by skipping the element and continuing.

3. **NoSuchElementException**: This occurs when an element cannot be found. The script handles this by setting the corresponding data field to `None`.
