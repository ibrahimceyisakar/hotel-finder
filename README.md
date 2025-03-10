# Hotel Data Scraper, Analysis, and Visualization

This project is a comprehensive system for scraping hotel data, analyzing it for value, and visualizing the results through an interactive dashboard.

## Live Demo

The hotel analysis dashboard is deployed and accessible at:
[https://hotel-analyzer-dashboard-gg78.streamlit.app/](https://hotel-analyzer-dashboard-gg78.streamlit.app/)

## Project Components

The project consists of three main components:

1. **Web Scraping**: Automated scraping of hotel data from obilet.com using Selenium
2. **Data Analysis**: Calculation of value ratios and identification of top value hotels
3. **Data Visualization**: Interactive Streamlit dashboard for exploring the hotel data

## Live Demo

The hotel analysis dashboard is deployed and accessible at:
[https://hotel-analyzer-dashboard-gg78.streamlit.app/](https://hotel-analyzer-dashboard-gg78.streamlit.app/)

## Documentation

Detailed documentation for each component of the project:

- [Installation & Setup](docs/installation.md)
- [Web Scraping Component](docs/scraping.md)
- [Data Analysis Component](docs/analysis.md)
- [Visualization Dashboard](docs/dashboard.md)
- [Complete Workflow Guide](docs/workflow.md)

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```
   python main.py
   ```

3. Run the value analysis:
   ```
   python value_analysis.py
   ```

4. Launch the dashboard:
   ```
   streamlit run hotel_dashboard.py
   ```

## Project Structure

- `main.py` - Web scraping script
- `value_analysis.py` - Data analysis script
- `hotel_dashboard.py` - Streamlit dashboard
- `requirements.txt` - Project dependencies
- `docs/` - Detailed documentation
- `hotels_data.csv` - Scraped hotel data (generated)
- `hotels_data.json` - Scraped hotel data in JSON format (generated)
- `top_value_hotels.csv` - Analyzed hotel data (generated)
- `top_value_hotels.json` - Analyzed hotel data in JSON format (generated)
