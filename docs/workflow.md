# Complete Workflow Guide

This document provides a step-by-step guide for running the entire hotel data scraping, analysis, and visualization workflow.

## Overview

The workflow consists of three main steps:

1. **Web Scraping**: Extract hotel data from obilet.com
2. **Data Analysis**: Calculate value ratios and identify top value hotels
3. **Data Visualization**: Explore and analyze the data through an interactive dashboard

## Prerequisites

Before starting the workflow, ensure you have:

1. Completed the [installation and setup](installation.md)
2. Activated your virtual environment (if using one)
3. Installed all required dependencies

## Step 1: Run the Web Scraper

The first step is to run the web scraper to extract hotel data from obilet.com.

```bash
python main.py
```

**What happens during this step:**

1. A Chrome browser window will open
2. The script will navigate to obilet.com with specific search parameters
3. It will scroll through the hotel listings to load all results
4. It will extract data from each hotel listing
5. The data will be saved to `hotels_data.json` and `hotels_data.csv`

**Expected output:**

- Console messages showing progress
- Two output files: `hotels_data.json` and `hotels_data.csv`

**Estimated time:** 3-5 minutes, depending on the number of hotels and your internet connection speed.

**Note:** The browser window will remain open after the script finishes. You can close it manually.

## Step 2: Run the Value Analysis

After the scraper has completed and generated the data files, run the value analysis script:

```bash
python value_analysis.py
```

**What happens during this step:**

1. The script reads the hotel data from `hotels_data.json`
2. It calculates a value ratio for each hotel
3. It sorts the hotels by value ratio
4. It saves the top hotels to `top_value_hotels.json` and `top_value_hotels.csv`
5. It displays a summary of the top hotels in the console

**Expected output:**

- Console messages showing progress
- A table showing the top hotels by value ratio
- Two output files: `top_value_hotels.json` and `top_value_hotels.csv`

**Estimated time:** Less than 1 minute.

## Step 3: Launch the Dashboard

Finally, launch the Streamlit dashboard to visualize and explore the data:

```bash
streamlit run hotel_dashboard.py
```

**What happens during this step:**

1. The Streamlit server starts
2. A browser window opens with the dashboard
3. The dashboard loads the data from `top_value_hotels.json`
4. You can interact with the dashboard to explore the data

**Expected output:**

- A browser window with the interactive dashboard
- Console messages from the Streamlit server

**Note:** The dashboard will continue running until you stop the Streamlit server (press Ctrl+C in the terminal).

## Complete Workflow in One Command

If you want to run the entire workflow in sequence with a single command, you can create a shell script or use the following command:

**On macOS/Linux:**

```bash
python main.py && python value_analysis.py && streamlit run hotel_dashboard.py
```

**On Windows:**

```bash
python main.py && python value_analysis.py && streamlit run hotel_dashboard.py
```

This will run each script in sequence, and if any script fails, the subsequent scripts will not run.

## Customizing the Workflow

### Changing the Search Parameters

To search for hotels in a different city or with different dates:

1. Open `main.py`
2. Modify the configuration options in the `main()` function:
   ```python
   # Options for the hotel search
   CITY_CODE = "istanbul-250-60649-2"  # Change this to a different city code
   CHECKIN, CHECKOUT = find_next_weekend()  # You can replace this with specific dates
   ADULTS = 2  # Change the number of adults
   ```
3. Save the file and run the workflow again

### Adjusting the Number of Top Hotels

To change the number of top hotels analyzed and displayed:

1. Open `value_analysis.py`
2. Modify the `top_n` variable in the `main()` function:
   ```python
   # Number of top hotels to output
   top_n = 100  # Change this to your desired number
   ```
3. Save the file and run the workflow again

### Adding New Visualizations

To add new visualizations to the dashboard:

1. Open `hotel_dashboard.py`
2. Add new visualization functions
3. Update the dashboard tabs to include the new visualizations
4. Save the file and run the dashboard again

## Troubleshooting

### Web Scraper Issues

- **Browser doesn't open**: Check that Chrome and ChromeDriver are installed correctly
- **No data extracted**: Check that the website structure hasn't changed
- **Script crashes**: Check the error message for details on what went wrong

### Value Analysis Issues

- **Input file not found**: Ensure that the web scraper has run successfully
- **No hotels with valid ratios**: Check that the scraped data contains valid review scores and prices

### Dashboard Issues

- **Dashboard doesn't start**: Check that Streamlit is installed correctly
- **No data displayed**: Ensure that the value analysis has run successfully
- **Visualizations don't render**: Check the console for error messages

## Data Flow Diagram

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Web Scraper   |---->|  Value Analysis|---->|   Dashboard    |
|  (main.py)     |     |(value_analysis.py)   |(hotel_dashboard.py)
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
        |                     |                      |
        v                     v                      v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
| hotels_data.json|---->|top_value_hotels.json|--->|  Interactive  |
| hotels_data.csv |     |top_value_hotels.csv |    | Visualizations|
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
```

This diagram illustrates the flow of data through the three components of the system.

## Conclusion

By following this workflow guide, you should be able to:

1. Extract hotel data from obilet.com
2. Analyze the data to identify the best value hotels
3. Explore and visualize the data through an interactive dashboard

If you encounter any issues or have questions, refer to the specific documentation for each component:

- [Web Scraping Component](scraping.md)
- [Data Analysis Component](analysis.md)
- [Visualization Dashboard](dashboard.md)
