import json
import csv
import re
import os

def extract_numeric_value(price_str):
    """
    Extract numeric value from price string.
    Example: "17.345 TL" -> 17345
    """
    if not price_str or not isinstance(price_str, str):
        return None
    
    # Remove currency symbol and extract numbers
    # This regex finds all digits and dots/commas that might be used as separators
    matches = re.findall(r'[\d.,]+', price_str)
    if not matches:
        return None
    
    # Take the first match (should be the price)
    price_text = matches[0]
    
    # Replace thousand separator (dot in Turkish format) with empty string
    # and decimal separator (comma in Turkish format) with dot
    price_text = price_text.replace('.', '').replace(',', '.')
    
    try:
        return float(price_text)
    except ValueError:
        return None

def calculate_value_ratio(hotel):
    """
    Calculate value ratio (review_score / price) for a hotel.
    Returns a tuple of (hotel_with_ratio, ratio) or (hotel, None) if ratio can't be calculated.
    """
    # Extract review score
    try:
        if not hotel.get('review_score'):
            return hotel, None
        review_score = float(hotel['review_score'])
    except (ValueError, TypeError):
        return hotel, None
    
    # Extract price from daily_price field
    daily_price = hotel.get('daily_price', '')
    price_value = extract_numeric_value(daily_price)
    
    # If daily_price is not available or invalid, try using the regular price
    if not price_value:
        price_value = extract_numeric_value(hotel.get('price', ''))
    
    # If we still don't have a valid price, return None for ratio
    if not price_value or price_value <= 0:
        return hotel, None
    
    # Calculate ratio (review score per 1000 TL)
    ratio = (review_score / price_value) * 1000
    
    # Add ratio to hotel data
    hotel_with_ratio = hotel.copy()
    hotel_with_ratio['value_ratio'] = ratio
    
    return hotel_with_ratio, ratio

def analyze_hotel_value(input_json_path, output_json_path, output_csv_path, top_n=10):
    """
    Analyze hotel value by calculating review_score/price ratio.
    Output top N hotels to JSON and CSV files.
    """
    # Check if input file exists
    if not os.path.exists(input_json_path):
        print(f"Error: Input file {input_json_path} not found.")
        return False
    
    # Read hotel data from JSON file
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            hotels = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from {input_json_path}.")
        return False
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return False
    
    # Calculate value ratio for each hotel
    hotels_with_ratios = []
    for hotel in hotels:
        hotel_with_ratio, ratio = calculate_value_ratio(hotel)
        if ratio is not None:  # Only include hotels with valid ratios
            hotels_with_ratios.append((hotel_with_ratio, ratio))
    
    # Sort hotels by value ratio (descending)
    hotels_with_ratios.sort(key=lambda x: x[1], reverse=True)
    
    # Take top N hotels
    top_hotels = [hotel for hotel, _ in hotels_with_ratios[:top_n]]
    
    # Save top hotels to JSON file
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(top_hotels, f, ensure_ascii=False, indent=4)
        print(f"Top {top_n} hotels by value saved to {output_json_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {str(e)}")
        return False
    
    # Save top hotels to CSV file
    try:
        if not top_hotels:
            print("No hotels with valid ratios found.")
            return False
        
        # Get all possible keys from all dictionaries
        fieldnames = set()
        for hotel in top_hotels:
            fieldnames.update(hotel.keys())
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for hotel in top_hotels:
                # Handle features list for CSV
                hotel_copy = hotel.copy()
                if 'features' in hotel_copy and isinstance(hotel_copy['features'], list):
                    hotel_copy['features'] = ', '.join(hotel_copy['features'])
                writer.writerow(hotel_copy)
        print(f"Top {top_n} hotels by value saved to {output_csv_path}")
    except Exception as e:
        print(f"Error writing to CSV file: {str(e)}")
        return False
    
    return True

def main():
    # File paths
    input_json_path = 'hotels_data.json'
    output_json_path = 'top_value_hotels.json'
    output_csv_path = 'top_value_hotels.csv'
    
    # Number of top hotels to output
    top_n = 100
    
    # Analyze hotel value and output top hotels
    success = analyze_hotel_value(input_json_path, output_json_path, output_csv_path, top_n)
    
    if success:
        print(f"Successfully analyzed hotel value and output top {top_n} hotels.")
        
        # Print a summary of the top hotels
        try:
            with open(output_json_path, 'r', encoding='utf-8') as f:
                top_hotels = json.load(f)
            
            print("\nTop Hotels by Value Ratio:")
            print("-" * 80)
            print(f"{'Rank':<5}{'Hotel Name':<40}{'Review':<8}{'Price':<15}{'Value Ratio':<12}")
            print("-" * 80)
            
            for i, hotel in enumerate(top_hotels, 1):
                name = hotel.get('name', 'N/A')
                review = hotel.get('review_score', 'N/A')
                price = hotel.get('daily_price', hotel.get('price', 'N/A'))
                ratio = hotel.get('value_ratio', 'N/A')
                
                if isinstance(ratio, float):
                    ratio_str = f"{ratio:.4f}"
                else:
                    ratio_str = str(ratio)
                
                print(f"{i:<5}{name[:37] + '...' if len(name) > 37 else name:<40}{review:<8}{price:<15}{ratio_str:<12}")
            
            print("-" * 80)
        except Exception as e:
            print(f"Error displaying summary: {str(e)}")
    else:
        print("Failed to analyze hotel value.")

if __name__ == "__main__":
    main()
