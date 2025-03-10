# Installation & Setup

This document provides instructions for setting up the Hotel Data Scraper, Analysis, and Visualization project.

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for Selenium)
- ChromeDriver (compatible with your Chrome version)

## Environment Setup

1. Clone the repository or download the project files.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ChromeDriver Setup

The project uses Selenium with Chrome for web scraping. You need to have ChromeDriver installed and available in your PATH.

1. Check your Chrome version:
   - Open Chrome
   - Go to Menu (three dots) > Help > About Google Chrome
   - Note the version number

2. Download the matching ChromeDriver version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/).

3. Extract the downloaded file and place the ChromeDriver executable in a location that's in your system's PATH.
   - On Windows, you can place it in the same directory as your Python executable.
   - On macOS/Linux, you can place it in `/usr/local/bin/`.

## Verifying Setup

To verify that everything is set up correctly:

1. Activate your virtual environment if it's not already activated.

2. Run a simple test to check if Selenium and ChromeDriver are working:
   ```python
   from selenium import webdriver
   
   options = webdriver.ChromeOptions()
   driver = webdriver.Chrome(options=options)
   driver.get("https://www.google.com")
   print("Title:", driver.title)
   driver.quit()
   ```

3. If the test runs without errors and displays the title of the Google homepage, your setup is correct.

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   - Ensure ChromeDriver is in your PATH
   - Try specifying the path explicitly: `driver = webdriver.Chrome(executable_path='/path/to/chromedriver')`

2. **Version mismatch**:
   - Make sure your ChromeDriver version matches your Chrome browser version
   - Update both Chrome and ChromeDriver to the latest versions

3. **Dependency issues**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check for any error messages during installation

4. **Permission issues** (macOS/Linux):
   - Make ChromeDriver executable: `chmod +x /path/to/chromedriver`
