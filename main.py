import time
import json
import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

def find_next_weekend() -> tuple:
    """Returns the next weekend dates (friday and sunday)
    
    Returns:
    tuple: (str, str) -- Friday and Sunday dates in "YYYYMMDD" format
    """
    today = datetime.now()
    friday = today + timedelta((4 - today.weekday()) % 7)
    sunday = friday + timedelta(2)
    return friday.strftime("%Y%m%d"), sunday.strftime("%Y%m%d")

def get_hotel_url(city_code: str, checkin: str, checkout: str, adults: int) -> str:
    """Returns the URL for the hotel search, sample URL:
    https://www.obilet.com/oteller/istanbul-250-60649-2/20250319-20250323/2ad

    Arguments:
    city_code {str} -- City code for the search
    checkin {str} -- Check-in date in "YYYYMMDD" format
    checkout {str} -- Check-out date in "YYYYMMDD" format
    adults {int} -- Number of adults
    """
    return f"https://www.obilet.com/oteller/{city_code}-250-60649-2/{checkin}-{checkout}/{adults}ad"

def extract_hotel_data(hotel_element):
    """Extract data from a hotel element
    
    Arguments:
    hotel_element -- Selenium WebElement representing a hotel
    
    Returns:
    dict -- Dictionary containing hotel data
    """
    try:
        # Extract hotel ID
        hotel_id = hotel_element.get_attribute('data-id')
        
        # Extract hotel name
        hotel_name = hotel_element.get_attribute('data-name')
        
        # Extract hotel image URL
        try:
            image_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-item__image')
            image_url = image_element.get_attribute('src')
        except NoSuchElementException:
            image_url = None
        
        # Extract star rating
        try:
            star_elements = hotel_element.find_elements(By.CSS_SELECTOR, '.hotel-item__star .star')
            star_rating = len(star_elements)
        except NoSuchElementException:
            star_rating = None
        
        # Extract location
        try:
            location_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-location__address')
            location = location_element.text.strip()
        except NoSuchElementException:
            location = None
        
        # Extract distance to center
        try:
            distance_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-location__city-center-distance')
            distance = distance_element.text.strip()
        except NoSuchElementException:
            distance = None
        
        # Extract features
        features = []
        try:
            feature_elements = hotel_element.find_elements(By.CSS_SELECTOR, '.hotel-features__item span')
            for feature in feature_elements:
                features.append(feature.text.strip())
        except NoSuchElementException:
            pass
        
        # Extract review score
        try:
            review_score_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-review__badge')
            review_score = review_score_element.text.strip()
        except NoSuchElementException:
            review_score = None
        
        # Extract review text
        try:
            review_text_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-review__text')
            review_text = review_text_element.text.strip()
        except NoSuchElementException:
            review_text = None
        
        # Extract review count
        try:
            review_count_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-review__comment')
            review_count = review_count_element.text.strip()
            # Extract just the number from the parentheses
            import re
            review_count_match = re.search(r'\((\d+)', review_count)
            if review_count_match:
                review_count = review_count_match.group(1)
        except (NoSuchElementException, AttributeError):
            review_count = None
        
        # Extract price
        try:
            price_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-price__amount')
            price = price_element.text.strip()
        except NoSuchElementException:
            price = None
        
        # Extract daily price
        try:
            daily_price_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-price__daily-amount')
            daily_price = daily_price_element.text.strip()
        except NoSuchElementException:
            daily_price = None
        
        # Extract nights
        try:
            nights_element = hotel_element.find_element(By.CSS_SELECTOR, '.hotel-price__night')
            nights = nights_element.text.strip()
        except NoSuchElementException:
            nights = None
        
        return {
            'id': hotel_id,
            'name': hotel_name,
            'image_url': image_url,
            'star_rating': star_rating,
            'location': location,
            'distance_to_center': distance,
            'features': features,
            'review_score': review_score,
            'review_text': review_text,
            'review_count': review_count,
            'price': price,
            'daily_price': daily_price,
            'nights': nights
        }
    except StaleElementReferenceException:
        # If the element becomes stale, return None
        return None

def save_to_json(data, filename):
    """Save data to a JSON file
    
    Arguments:
    data -- List of dictionaries containing hotel data
    filename -- Name of the file to save to
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename):
    """Save data to a CSV file
    
    Arguments:
    data -- List of dictionaries containing hotel data
    filename -- Name of the file to save to
    """
    if not data:
        print("No data to save to CSV")
        return
    
    # Get all possible keys from all dictionaries
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            # Handle features list for CSV
            if 'features' in item and isinstance(item['features'], list):
                item['features'] = ', '.join(item['features'])
            writer.writerow(item)
    print(f"Data saved to {filename}")

def main():
    # Options for the hotel search
    CITY_CODE = "istanbul-250-60649-2"
    CHECKIN, CHECKOUT = find_next_weekend()
    ADULTS = 2
    
    target_url = get_hotel_url(CITY_CODE, CHECKIN, CHECKOUT, ADULTS)
    
    # Initialize the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start with maximized browser
    options.add_experimental_option("detach", True) # Keep the browser open after script ends
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the target URL
        print(f"Navigating to {target_url}")
        driver.get(target_url)
        
        # Wait for the specific hotel element to appear
        print("Waiting for the target hotel element to appear...")
        wait = WebDriverWait(driver, 30)
        target_hotel = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.item.journey.js-hotel-item[data-id="101336"][data-name="Swissôtel The Bosphorus İstanbul"]'))
        )
        print("Target hotel element found!")
        
        # Initialize list to store all hotel data
        all_hotels_data = []
        processed_hotel_ids = set()
        
        # Function to scroll and extract hotels
        def scroll_and_extract():
            nonlocal all_hotels_data, processed_hotel_ids
            
            # Find all hotel elements currently visible
            hotel_elements = driver.find_elements(By.CSS_SELECTOR, 'li.item.journey.js-hotel-item')
            
            # Extract data from each hotel element
            for hotel in hotel_elements:
                try:
                    hotel_id = hotel.get_attribute('data-id')
                    
                    # Skip if we've already processed this hotel
                    if hotel_id in processed_hotel_ids:
                        continue
                    
                    # Extract data and add to our list
                    hotel_data = extract_hotel_data(hotel)
                    if hotel_data:
                        all_hotels_data.append(hotel_data)
                        processed_hotel_ids.add(hotel_id)
                        print(f"Extracted data for hotel: {hotel_data['name']} (ID: {hotel_id})")
                except StaleElementReferenceException:
                    # If the element becomes stale, skip it
                    continue
            
            return len(hotel_elements)
        
        # Perform initial extraction
        num_hotels = scroll_and_extract()
        print(f"Initially found {num_hotels} hotels")
        
        # Scroll and extract until no new hotels are found
        last_count = 0
        max_attempts = 30  # Limit the number of scroll attempts
        attempts = 0
        
        while attempts < max_attempts:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolled to bottom of page")
            
            # Wait for new content to load
            time.sleep(2)
            
            # Extract hotels again
            current_count = scroll_and_extract()
            
            # If we haven't found any new hotels after several attempts, break
            if current_count == last_count:
                attempts += 1
                print(f"No new hotels found. Attempt {attempts}/{max_attempts}")
            else:
                attempts = 0  # Reset attempts if we found new hotels
                
            last_count = current_count
            
            # Print progress
            print(f"Total unique hotels found so far: {len(processed_hotel_ids)}")
        
        print(f"Finished scraping. Found {len(all_hotels_data)} unique hotels.")
        
        # Save data to files
        save_to_json(all_hotels_data, 'hotels_data.json')
        save_to_csv(all_hotels_data, 'hotels_data.csv')
        
    except TimeoutException:
        print("Timed out waiting for the target hotel element to appear")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the browser
        # driver.quit()
        pass

if __name__ == "__main__":

    # Time the script
    start_time = time.time()
    main()
    print(f"Script finished in {time.time() - start_time:.2f} seconds")
