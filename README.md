# Hotel Data Scraper, Analysis, and Visualization

A comprehensive system for scraping hotel data from obilet.com, analyzing it for value metrics, and visualizing the results through an interactive Streamlit dashboard.

## 📋 Overview

This project automates the entire process of hotel data collection, analysis, and visualization to help travelers find the best value accommodations. It consists of three main components that work together to:

1. **Scrape** hotel listings from obilet.com using Selenium
2. **Analyze** the data to calculate value ratios and identify top value hotels
3. **Visualize** the results through an interactive Streamlit dashboard

## 🌟 Key Features

- **Automated Web Scraping**: Extracts detailed hotel information including prices, ratings, features, and locations
- **Value Analysis Algorithm**: Calculates a value ratio (review score / price) to identify hotels offering the best value for money
- **Interactive Dashboard**: Provides multiple visualization tabs for exploring different aspects of the hotel data
- **Data Export**: Saves data in both JSON and CSV formats for further analysis
- **Configurable Parameters**: Easily adjust search parameters, analysis criteria, and visualization options

## 🔍 Live Demo

The hotel analysis dashboard is deployed and accessible at:
[https://hotel-analyzer-dashboard-gg78.streamlit.app/](https://hotel-analyzer-dashboard-gg78.streamlit.app/)

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Selenium**: Web automation and scraping
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualizations
- **Streamlit**: Dashboard creation and deployment
- **Regular Expressions**: Text pattern extraction
- **JSON/CSV**: Data storage and exchange

## 📊 Dashboard Features

The interactive Streamlit dashboard includes:

- **Value Overview**: Bar charts and scatter plots showing hotels ranked by value ratio
- **Price Analysis**: Histograms and box plots of hotel prices
- **Review Analysis**: Distribution and comparison of review scores
- **Feature Analysis**: Most common hotel features and their impact on reviews
- **Location Analysis**: Geographical distribution and distance analysis

## 📚 Documentation

Detailed documentation for each component of the project:

- [Installation & Setup](docs/installation.md): Environment setup, dependencies, and ChromeDriver configuration
- [Web Scraping Component](docs/scraping.md): How the scraper works, CSS selectors, and data extraction
- [Data Analysis Component](docs/analysis.md): Value ratio calculation, price extraction, and ranking algorithm
- [Visualization Dashboard](docs/dashboard.md): Dashboard structure, visualizations, and customization options
- [Complete Workflow Guide](docs/workflow.md): Step-by-step guide for running the entire pipeline

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/hotel-data-scraper.git
   cd hotel-data-scraper
   ```

2. **Set up the environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver** (see [Installation Guide](docs/installation.md) for details)

4. **Run the scraper**:
   ```bash
   python main.py
   ```

5. **Run the value analysis**:
   ```bash
   python value_analysis.py
   ```

6. **Launch the dashboard**:
   ```bash
   streamlit run hotel_dashboard.py
   ```

## 📁 Project Structure

```
hotel-data-scraper/
├── main.py                  # Web scraping script
├── value_analysis.py        # Data analysis script
├── hotel_dashboard.py       # Streamlit dashboard
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── docs/                    # Detailed documentation
│   ├── installation.md      # Installation guide
│   ├── scraping.md          # Scraping documentation
│   ├── analysis.md          # Analysis documentation
│   ├── dashboard.md         # Dashboard documentation
│   └── workflow.md          # Complete workflow guide
├── hotels_data.json         # Scraped hotel data (generated)
├── hotels_data.csv          # Scraped hotel data in CSV (generated)
├── top_value_hotels.json    # Analyzed hotel data (generated)
└── top_value_hotels.csv     # Analyzed hotel data in CSV (generated)
```

## 🔄 Data Processing Pipeline

1. **Data Collection**:
   - Navigate to obilet.com with specified search parameters
   - Scroll through results to load all hotel listings
   - Extract detailed information for each hotel
   - Save raw data to JSON and CSV files

2. **Data Analysis**:
   - Load scraped hotel data
   - Extract numeric values from price strings
   - Calculate value ratio (review score / price * 1000)
   - Sort hotels by value ratio
   - Save top N hotels to JSON and CSV files

3. **Data Visualization**:
   - Load analyzed hotel data
   - Process and transform data for visualization
   - Create interactive charts and tables
   - Display results in a user-friendly dashboard

## 🔧 Customization Options

### Web Scraper

You can customize the scraper by modifying the following parameters in `main.py`:

```python
# Options for the hotel search
CITY_CODE = "istanbul-250-60649-2"  # Change to different city
CHECKIN, CHECKOUT = find_next_weekend()  # Or specify custom dates
ADULTS = 2  # Change number of adults
```

### Value Analysis

Adjust the analysis parameters in `value_analysis.py`:

```python
# Number of top hotels to output
top_n = 100  # Change to desired number

# Modify the value ratio calculation
ratio = (review_score / price_value) * 1000  # Adjust formula as needed
```

### Dashboard

Customize the dashboard in `hotel_dashboard.py`:

- Add new visualizations
- Modify existing charts
- Add additional tabs
- Change color schemes
- Add new metrics

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [obilet.com](https://www.obilet.com/) for providing the hotel data
- [Selenium](https://www.selenium.dev/) for web automation capabilities
- [Streamlit](https://streamlit.io/) for the interactive dashboard framework
- [Plotly](https://plotly.com/) for the visualization library
